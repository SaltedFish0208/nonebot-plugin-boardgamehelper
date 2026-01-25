from datetime import datetime
from typing import TYPE_CHECKING

import shortuuid
from nonebot_plugin_alconna import Text, UniMessage

if TYPE_CHECKING:
    from .models import PostsModel

alphabet = "abcdefghigklmnopqrstuvwxyz0123456789"
class Post:
    """
    一个招募标准类

    attr:
        recruitment_code: 招募信息的标识id
        publisher_user_id: 发起招募信息者的id
        publisher_name: 发起招募信息者的昵称
        content: 招募信息内容
        end_time: 招募结束时间
    """
    def __init__(
            self, user_id: str,
            user_name: str,
            content: str,
            rule: str,
            end_time: datetime
            ) -> None:
        self.recruitment_code: str = shortuuid.ShortUUID(alphabet=alphabet).random(4)
        self.publisher_user_id = user_id
        self.publisher_name = user_name
        self.content = content
        self.end_time = end_time
        self.rule = rule

    def to_dict(self) -> dict:
        """
        该方法用于将招募类转换为字典
        """
        return{
            "recruitment_code": self.recruitment_code,
            "publisher_user_id": self.publisher_user_id,
            "publisher_name": self.publisher_name,
            "content": self.content,
            "end_time": self.end_time,
            "rule": self.rule
        }
    @classmethod
    def from_orm_class(cls, data: "PostsModel") -> "Post":
        """
        该方法用于从orm模板类恢复为Post实例
        """
        post = cls(
            user_id = data.publisher_user_id,
            user_name = data.publisher_name,
            content = data.content,
            end_time = data.end_time,
            rule = data.rule
        )
        post.recruitment_code = data.recruitment_code
        return post

    def to_unimessage(self) -> UniMessage:
        """
        该方法用于将Post实例转换为UniMessage类
        """
        return UniMessage([
            Text(f"[车车ID]{self.recruitment_code}"),
            Text("\n"),
            Text(f"[发车人]{self.publisher_name}({self.publisher_user_id})"),
            Text("\n"),
            Text(self.content),
            Text("\n"),
            Text(f"[结束时间]{self.end_time.strftime('%Y-%m-%d %H:%M')}")
        ])
