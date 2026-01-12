import re
from datetime import datetime
from enum import Enum, auto
from typing import Optional
from zoneinfo import ZoneInfo


class DateCheckResult(Enum):
    OK = auto()
    INVALID_FORMAT = "输入格式不合规"
    INVALID_SEQUENCE = "早于当前时间"
    INVALID_DATETIME = "不存在的日期或时间"
    ONLY_DATE = "只提供日期，未提供时间"

class ContentCheckResult(Enum):
    OK = auto()
    MISSING_RULE = "缺少[游戏规则]"
    MISSING_METHOD = "缺少[跑团方式]"
    MISSING_PLATFORM = "缺少[平台]"

# 北京时间 UTC+8
BJ_TZ = ZoneInfo("Asia/Shanghai")
_NEWLINE_PATTERN = re.compile(r"\r\n|\r|\n|\v|\f|\x85|\u2028|\u2029")

def _normalize_newlines(text: str) -> str:
    return _NEWLINE_PATTERN.sub("\n", text)

def _need_insert_newlines(text: str) -> bool:
    max_square_brackets = 2
    """
    判断是否存在“同一行多个字段头”的情况
    """
    return any(line.count("[") >= max_square_brackets for line in text.splitlines())

def validate_datetime(
        input_str: str
        ) -> tuple[list["DateCheckResult"], Optional[datetime]]:
    """
    时间校验器

    Args:
        input_str (str): 用户输入的日期时间字符串

    Returns:
        tuple:
            - list[DateCheckResult]: 不符合的检查项，如果符合返回空列表
            - datetime | None: 合规的时间，或 None
    """
    input_str = input_str.strip().replace("：", ":")
    now = datetime.now(BJ_TZ)
    dt: Optional[datetime] = None
    errors: list["DateCheckResult"] = []

    # 尝试仅时间 → 补今天日期
    try:
        tmp_time = datetime.strptime(input_str, "%H:%M").time()  # noqa: DTZ007 可以肯定用户输入的均为北京时间
        if tmp_time.hour >= 24 or tmp_time.minute >= 60:  # noqa: PLR2004 时间校验没必要写变量了吧...
            errors.append(DateCheckResult.INVALID_DATETIME)
        else:
            today = now.date()
            tmp_dt = datetime.combine(today, tmp_time, tzinfo=BJ_TZ)
            if tmp_dt < now:
                errors.append(DateCheckResult.INVALID_SEQUENCE)
            else:
                dt = tmp_dt
                return [DateCheckResult.OK], dt
    except ValueError:
        pass

    # 尝试仅日期
    if dt is None:
        try:
            # .date()如果匹配了，就代表输入仅有年月日，所以到这里应该出现ValueError
            datetime.strptime(input_str, "%Y-%m-%d").date()  # noqa: DTZ007 可以肯定用户输入的均为北京时间，时区赋值已在下一行实现
            errors.append(DateCheckResult.ONLY_DATE)
        except ValueError:
            pass

    # 尝试完整日期时间
    if dt is None:
        try:
            tmp = datetime.strptime(input_str, "%Y-%m-%d %H:%M")  # noqa: DTZ007 可以肯定用户输入的均为北京时间，时区赋值已在下一行实现
            tmp = tmp.astimezone(BJ_TZ)
            if tmp.hour >= 24 or tmp.minute >= 60:  # noqa: PLR2004 时间校验没必要写变量了吧...
                errors.append(DateCheckResult.INVALID_DATETIME)
            elif tmp < now:
                errors.append(DateCheckResult.INVALID_SEQUENCE)
            else:
                dt = tmp
                return [DateCheckResult.OK], dt
        except ValueError:
            errors.append(DateCheckResult.INVALID_FORMAT)


    return errors, dt

def _pre_process(input_str: str) -> str:
    input_str = input_str.replace("【", "[").replace("】", "]")
    patterns = [
        re.escape("接下来请输入发车信息，例："),
        re.escape("请在一分钟内内完成输入，超时后您需要重新发车")
    ]
    combined_pattern = "|".join(patterns)
    before_content = r"^[^\[]+"
    input_str = re.sub(combined_pattern, "", input_str).strip()
    input_str = re.sub(before_content, "", input_str).strip()
    input_str = _normalize_newlines(input_str)
    return input_str  # noqa: RET504 shut fuck up 如果之后有其他正则匹配需求怎么办

def validate_content(input_str: str) -> tuple[list[ContentCheckResult], str]:
    """
    校验招募文本是否包含必要字段
    当有任意一项校验未通过时，返回空字符串

    returns:
        tuple(list[enum, str])
    """
    normalized = _pre_process(input_str)
    # 定义检测规则
    checks = {
        ContentCheckResult.MISSING_RULE: r"\[游戏规则\](.*?)\n",
        ContentCheckResult.MISSING_METHOD: r"\[跑团方式\](.*?)\n",
        ContentCheckResult.MISSING_PLATFORM: r"\[平台\](.*?)\n",
    }

    # 自动补换行
    if _need_insert_newlines(normalized):
        normalized = re.sub(r"(?<!^)\[", "\n[", normalized)

    missing: list[ContentCheckResult] = []

    for enum_key, pattern in checks.items():
        if not re.search(pattern, normalized):
            missing.append(enum_key)

    # 有缺失则不返回字符串，返回所有丢失值的枚举
    if missing:
        return (missing, "")

    # 全部存在后返回枚举值OK和格式化好的字符串
    return ([ContentCheckResult.OK], normalized)


def get_rules(input_str: str) -> str:
    rule = re.search(r"(?<=\[游戏规则\]).+", input_str)
    if rule:
        return rule.group()
    return ""
