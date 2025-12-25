from datetime import datetime, timedelta
from typing import cast
from zoneinfo import ZoneInfo

from nonebot import get_plugin_config, logger, on_command, require
from nonebot.adapters.onebot.v11 import (
    GROUP_ADMIN,
    GROUP_OWNER,
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    exception,
)
from nonebot.params import ArgPlainText, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot_plugin_alconna import CustomNode, SupportScope, Target, UniMessage
from nonebot_plugin_apscheduler import scheduler

from .config import Config
from .data_manager import DataBaseManager, JsonIO
from .models import BroadcastModel, PostsModel
from .post_func import Post
from .utils import sqlite_file_exists
from .validator import (
    ContentCheckResult,
    DateCheckResult,
    validate_content,
    validate_datetime,
)

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_boardgamehelper",
    description="一个 NoneBot2 桌游约车助手插件，提供桌游群招募、发车、封车等功能。",
    usage="",
    type="application",
    homepage="https://github.com/SaltedFish0208/nonebot-plugin-boardgamehelper",
    config=Config,
    supported_adapters={"~onebot.v11"}
)

require("nonebot_plugin_alconna")
require("nonebot_plugin_apscheduler")

config = get_plugin_config(Config)

db_path = config.boardgamehelper_database_url
reply_path = config.boardgamehelper_json_path
BJ_TZ = ZoneInfo("Asia/Shanghai")


exists = sqlite_file_exists(config.boardgamehelper_database_url)

if not exists[0] and not exists[1]:
    logger.critical("哦不！你的boardgamehelper_database_url选项填错了，SQLite Url的格式应该形如'sqlite://path'")
    raise ValueError("SQLite URL格式无效")  # noqa: TRY003
elif not exists[0] and exists[1]:
    file_path = exists[1]
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)
db = DataBaseManager(db_path)
reply = JsonIO(reply_path).load("reply.json")

publish_recruitment = on_command("发车", aliases={"桌游发车", "开车"})
@publish_recruitment.handle()
async def _(event: MessageEvent, state: T_State):
    if db.select(
        PostsModel,
        {
            "publisher_user_id": event.user_id
        },
        first=True
        ) is not None:
        await UniMessage.text(reply["already_publish"]).finish()
    await UniMessage.text(reply["publish_tip"]).send()
    state["publisher_user_id"] = event.user_id
    state["publisher_name"] = event.sender.nickname

@publish_recruitment.got("recruitment_content")
async def _(state: T_State, message: str = ArgPlainText("recruitment_content")):
    result = validate_content(message)
    if ContentCheckResult.OK not in result[0]:
        error_list = [r.value for r in result[0]]
        error_list = cast("str", error_list)
        missing = "\n".join(error_list)
        await UniMessage.text(reply["publish_missing_sth"]).text("\n").text(missing).text("\n").text(reply["please_check"]).finish()  # noqa: E501
    state["recruitment_content"] = result[1]
    await UniMessage.text(reply["time_tip"]).send()

@publish_recruitment.got("end_time")
async def _(state:T_State, message: str = ArgPlainText("end_time")):
    result = validate_datetime(message)
    if DateCheckResult.OK not in result[0]:
        error_list = [r.value for r in result[0]]
        error_list = cast("str", error_list)
        missing = "\n".join(error_list)
        await UniMessage.text(reply["date_missing_sth"]).text("\n").text(missing).text("\n").text(reply["please_check"]).finish()  # noqa: E501
    time = cast("datetime", result[1])
    post = Post(
        user_id=state["publisher_user_id"],
        user_name=state["publisher_name"],
        content=state["recruitment_content"],
        end_time=time
    )
    broadcast_groups = db.select(BroadcastModel, {}, first=False)
    broadcast_groups = cast("list[BroadcastModel]", broadcast_groups)
    ids = [group.group_id for group in broadcast_groups]
    if ids:
        for group_id in ids:
            target = Target(group_id, scope=SupportScope.qq_client)
            try:
                await post.to_unimessage().send(target=target)
            except exception.ActionFailed:
                db.delete(BroadcastModel, {"group_id": group_id})
    packaged = post.to_dict()
    db.upsert(PostsModel, packaged)
    await UniMessage.text(reply["published"]).finish()

query_recruitment = on_command("查车", aliases={"桌游查车"})
@query_recruitment.handle()
async def _(bot: Bot):
    all_recruitments = db.select(PostsModel, {}, first=False)
    all_recruitments = cast("list[PostsModel]", all_recruitments)
    recruitments_now = []
    recruitments_after = []
    now = datetime.now(BJ_TZ)
    if not all_recruitments:
        await UniMessage.text(reply["no_recruitments"]).finish()
    for recruitment in all_recruitments:
        post = Post.from_orm_class(recruitment)
        recruitment.end_time = recruitment.end_time.replace(tzinfo=BJ_TZ)
        if abs(now - recruitment.end_time) <= timedelta(days=1):
            recruitments_now.append(post.to_unimessage())
        else:
            recruitments_after.append(post.to_unimessage())
    recruitments_now.insert(0, UniMessage.text(reply["recruitments_now"]))
    recruitments_after.insert(0, UniMessage.text(reply["recruitments_after"]))
    seq = recruitments_now + recruitments_after
    await UniMessage.reference(*[
            CustomNode(uid=bot.self_id, name="Amadeus", content=msg)
            for msg in seq
        ]
    ).finish()

close_recruitment = on_command("封车", aliases={"桌游封车"})
@close_recruitment.handle()
async def _(event: MessageEvent):
    target = db.select(PostsModel, {"publisher_user_id": event.user_id}, first=True)
    if target is None:
        await UniMessage.text(reply["close_recruitment_failed"]).finish()
    db.delete(PostsModel, {"publisher_user_id": event.user_id})
    await UniMessage.text(reply["close_recruitment_success"]).finish()

delete_recruitment = on_command("强制封车", permission=SUPERUSER)
@delete_recruitment.handle()
async def _(msg: Message = CommandArg()):
    msg_str = msg.extract_plain_text().strip()
    if not msg:
        await UniMessage.text(reply["ask_for_uuid"]).send()
    elif db.select(PostsModel, {"recruitment_code": msg_str}, first=True) is None:
        await UniMessage.text(reply["delete_recruitment_failed"]).finish()
    else:
        db.delete(PostsModel, {"recruitment_code": msg_str})
        await UniMessage.text(reply["delete_recruitment_success"]).finish()

@delete_recruitment.got("recruitment_code")
async def _(msg: Message = CommandArg()):
    msg_str = msg.extract_plain_text().strip()
    if db.select(PostsModel, {"recruitment_code": msg_str}, first=True) is None:
        await UniMessage.text(reply["delete_recruitment_failed"]).finish()
    else:
        db.delete(PostsModel, {"recruitment_code": msg_str})
        await UniMessage.text(reply["delete_recruitment_success"]).finish()

open_broadcast = on_command(
    "开启全群广播",
    permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER
    )
@open_broadcast.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if db.select(BroadcastModel, {"group_id": event.group_id}, first=True) is not None:
        await UniMessage.text(reply["broadcast_exists"]).finish()
    group_info = await bot.call_api("get_group_info", group_id=event.group_id)
    db.upsert(
        BroadcastModel,
        {
            "group_id": event.group_id,
            "group_name": group_info["group_name"]
        })
    await UniMessage.text(reply["open_broadcast_success"]).finish()

close_broadcast = on_command(
    "关闭全群广播",
    permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER
    )
@close_broadcast.handle()
async def _(event: GroupMessageEvent):
    if db.select(BroadcastModel, {"group_id": event.group_id}, first=True) is None:
        await UniMessage.text(reply["broadcast_not_exists"]).finish()
    db.delete(BroadcastModel, {"group_id": event.group_id})
    await UniMessage.text(reply["close_broadcast_success"]).finish()

@scheduler.scheduled_job("interval", minutes=1)
async def _():
    count = db.cleanup_expired(PostsModel, PostsModel.end_time, 0)
    logger.info(f"清理了 {count} 条过时信息")
