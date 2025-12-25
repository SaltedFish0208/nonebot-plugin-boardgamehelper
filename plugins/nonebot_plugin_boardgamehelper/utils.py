from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def sqlite_file_exists(url: str) -> tuple[bool, Optional[Path]]:
    """
    判断 SQLite URL 对应的文件是否存在。
    返回：
    - 如果文件存在：返回True，None
    - 如果文件不存在：返回False，路径不合法的话返回None，合法的话返回对应的 Path 对象
    """
    if not url.startswith("sqlite://"):
        return False, None
    parsed = urlparse(url)
    path_str = parsed.path
    # 处理 /./ 前缀，将 sqlite:///./data/... 转为 ./data/...
    if path_str.startswith("/./"):
        path_str = path_str[1:]  # 去掉第一个 /
    # 转为 Path 对象
    path = Path(path_str)
    # 判断是否存在
    if path.exists():
        return True, None
    return False, path  # 返回 Path 对象（可能是相对路径）

