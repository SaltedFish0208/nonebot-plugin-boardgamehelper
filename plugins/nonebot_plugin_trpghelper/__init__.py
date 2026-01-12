from datetime import datetime, timedelta
from typing import cast
from zoneinfo import ZoneInfo

from nonebot import get_plugin_config, logger, on_command, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_apscheduler")
require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as storage
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
from .fuzzy_query import the_chosen_one
from .models import BroadcastModel, PostsModel
from .post_func import Post
from .utils import faq_generator, reply_generator, rules_aliases_generator
from .validator import (
    ContentCheckResult,
    DateCheckResult,
    get_rules,
    validate_content,
    validate_datetime,
)

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_trpghelper",
    description="一个 NoneBot2 TRPG(桌面角色扮演游戏)约车助手插件，提供跑团群招募、发车、封车等功能。",  # noqa: E501
    usage="",
    type="application",
    homepage="https://github.com/SaltedFish0208/nonebot-plugin-boardgamehelper",
    config=Config,
    supported_adapters={"~onebot.v11"}
)


config = get_plugin_config(Config)
BJ_TZ = ZoneInfo("Asia/Shanghai")


db_path = storage.get_plugin_data_file("database.db")
reply_path = storage.get_plugin_config_file("reply.json")
rule_aliases_path = storage.get_plugin_config_file("rule_aliases.json")
faq_path = storage.get_plugin_data_file("faq.json")

db_path.touch(exist_ok=True)
if not reply_path.exists():
    reply_generator(reply_path)

if not faq_path.exists():
    faq_generator(faq_path)

if not rule_aliases_path.exists():
    rules_aliases_generator(rule_aliases_path)

db = DataBaseManager(db_path)
reply = JsonIO(reply_path).load()
faq = JsonIO(faq_path).load()
rule_aliases = JsonIO(rule_aliases_path).load()

publish_recruitment = on_command("发车")
@publish_recruitment.handle()
async def _(event: MessageEvent, state: T_State):
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
    raw_rule = get_rules(state["recruitment_content"]).strip()
    try:
        packaged["rule"] = rule_aliases[raw_rule]
    except KeyError:
        packaged["rule"] = "Unknown"
    db.upsert(PostsModel, packaged)
    await UniMessage.text(reply["published"]).finish()

query_recruitment = on_command("查车")
@query_recruitment.handle()
async def _(bot: Bot, msg: Message = CommandArg()):
    msg_str = msg.extract_plain_text().strip()
    rule = "所有规则"
    if msg_str:
        try:
            rule = rule_aliases[msg_str.lower()]
        except KeyError:
            await UniMessage.text(reply["no_rules"]).finish()
        all_recruitments = db.select(
            PostsModel,
            {"rule": rule},
            first=False)
    else:
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
    seq.insert(0, UniMessage.text(f'{reply["what_rule_you_search"]}{rule}'))
    await UniMessage.reference(*[
            CustomNode(uid=bot.self_id, name="Amadeus", content=msg)
            for msg in seq
        ]
    ).finish()

close_recruitment = on_command("封车")
@close_recruitment.handle()
async def _(event: MessageEvent, state: T_State, msg: Message = CommandArg()):
    msg_str = msg.extract_plain_text().strip()
    targets = db.select(PostsModel, {"publisher_user_id": event.user_id})
    if not targets:
        await UniMessage.text(reply["close_recruitment_failed"]).finish()
    if len(targets) == 1:
        db.delete(PostsModel, {"publisher_user_id": event.user_id})
        await UniMessage.text(reply["close_recruitment_success"]).finish()
    if msg_str and any(t.recruitment_code == msg_str for t in targets):
        db.delete(
            PostsModel,{
                "publisher_user_id": event.user_id,
                "recruitment_code": msg_str
            })
        await UniMessage.text(reply["close_recruitment_success"]).finish()
    elif msg_str:
        await UniMessage.text(reply["wrong_recruitment_code"]).finish()
    state["records"] = targets
    await UniMessage.text(reply["ask_for_uuid"]).send()

@close_recruitment.got("recruitment_code")
async def _(
    state: T_State,
    event: MessageEvent,
    msg: str = ArgPlainText("recruitment_code")
    ):
    recruitment_code = msg.strip()
    if recruitment_code and any(t.recruitment_code == recruitment_code for t in state["records"]):  # noqa: E501
        db.delete(
                PostsModel,{
                    "publisher_user_id": event.user_id,
                    "recruitment_code": recruitment_code
                })
        await UniMessage.text(reply["close_recruitment_success"]).finish()
    elif recruitment_code:
        await UniMessage.text(reply["wrong_recruitment_code"]).finish()
    await UniMessage.text(reply["not_input_recruitment_code"]).finish()

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
    "开启广播",
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
    "关闭广播",
    permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER
    )
@close_broadcast.handle()
async def _(event: GroupMessageEvent):
    if db.select(BroadcastModel, {"group_id": event.group_id}, first=True) is None:
        await UniMessage.text(reply["broadcast_not_exists"]).finish()
    db.delete(BroadcastModel, {"group_id": event.group_id})
    await UniMessage.text(reply["close_broadcast_success"]).finish()

reload_json = on_command("重载json")
@reload_json.handle()
async def _():
    global reply  # noqa: PLW0603 重载方法
    global faq  # noqa: PLW0603 重载方法
    global rule_aliases  # noqa: PLW0603
    reply = JsonIO(reply_path).load()
    faq = JsonIO(faq_path).load()
    rule_aliases = JsonIO(rule_aliases_path).load()
    await UniMessage.text("success").finish()

faqer = on_command("faq")
@faqer.handle()
async def _(msg: Message = CommandArg()):
    msg_str = msg.extract_plain_text().strip()
    target = the_chosen_one(msg_str, faq)[0]
    answer = faq[target]["content"]
    await UniMessage.text(answer).finish()

@scheduler.scheduled_job("interval", minutes=1)
async def _():
    count = db.cleanup_expired(PostsModel, PostsModel.end_time, 0)
    logger.debug(f"清理了 {count} 条过时信息")
