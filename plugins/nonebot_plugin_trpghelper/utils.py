
from typing import TYPE_CHECKING

from .data_manager import JsonIO

if TYPE_CHECKING:
    from pathlib import Path


def reply_generator(path: "Path") -> None:
    json_file = JsonIO(path)
    reply = {
        "already_publish": "您已经发起了一个团",
        "publish_tip": "接下来请输入开团信息，例：\n[游戏规则] 老派要典\n[跑团方式] 面团-语音团-文字团\n[平台] QQ+白板-枭熊-FVTT等\n[模组] 橡树洞\n[人数] 1=3\n[导引剧情] 很久很久以前\n[GM名称与联系方式] XX-Q号或加Q群号 \n请提前准备好录入信息粘贴，1分后超时后您需要重新发车\n规则+跑团方式+平台为必填项目，剩下的组成部分可以自行更改",  # noqa: E501
        "time_tip": "接下来请输入自动封团的时间，如\n18:00\n2025-07-21 19:19\n当您仅输入时间时，默认为当天",  # noqa: E501
        "publish_missing_sth": "您的发团信息缺少条目：",
        "please_check": "请检查后重新发团",
        "date_missing_sth": "您的结束时间有以下问题：",
        "published": "您的发车信息已经存入数据库并广播至其他群",
        "no_recruitments": "现在还没有团",
        "recruitments_now": "以下为今日停止招募的团",
        "recruitments_after": "以下为长时间招募的团",
        "close_recruitment_success": "封团完成",
        "close_recruitment_failed": "封团失败：\n团库里没有您发的团呢",
        "ask_for_uuid": "请输入想要封团的团ID",
        "delete_recruitment_success": "强制封团成功",
        "delete_recruitment_failed": "强制封团失败，车库里没有该编号的团",
        "broadcast_exists": "本群已经开启过了全群广播",
        "open_broadcast_success": "本群开启了全群广播",
        "broadcast_not_exists": "本群尚未开启全群广播，无法关闭",
        "close_broadcast_success": "本群关闭了全群广播",
        "wrong_recruitment_code": "您并非此ID的团的发车人，请确认后重新封车",
        "not_input_recruitment_code": "占位符：打了个空字符串进去"
    }
    json_file.save(reply)

def faq_generator(path: "Path") -> None:
    json_file = JsonIO(path)
    reply = {}
    json_file.save(reply)
