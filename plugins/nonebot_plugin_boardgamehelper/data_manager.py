import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Union
from zoneinfo import ZoneInfo

from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

BJ_TZ = ZoneInfo("Asia/Shanghai")
"""
说真的，如果你能帮我重构一下这个部分就太好了
我真不擅长对付ORM
"""

class DataBaseManager:
    """
    该类负责将数据写入数据库或将实例从数据库里读出

    Args:
        url(str): 数据库URL
    """
    def __init__(self, url: str) -> None:
        self.engine = create_engine(url, echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def insert(self, model: type[Base], data: dict) -> None:
        """
        在数据库增加条目
        说真的，你有多想不开要用这些增改删查方法，直接用upsert好了

        Args:
            model(type[Base]): ORM模型，接受所有继承于models里的Base基类的类
            data(dict): 要写入的数据
        """
        with self.get_session() as session:
            obj = model(**data)
            session.add(obj)
            session.commit()

    def update(self, model: type[Base], filters: dict, values: dict) -> None:
        """
        在数据库增加条目
        说真的，你有多想不开要用这些增改删查方法，直接用upsert好了

        Args:
            model(type[Base]): ORM模型，接受所有继承于models里的Base基类的类
            filters(dict): WHERE 条件
            values(dict): 要更新的字段
        """
        with self.get_session() as session:
            session.query(model).filter_by(**filters).update(values)
            session.commit()

    def delete(self, model: type[Base], filters: dict) -> None:
        """
        在数据库删除条目
        说真的，你有多想不开要用这些增改删查方法，直接用upsert好了
        不对，这个不能用upsert

        Args:
            model(type[Base]): ORM模型，接受所有继承于models里的Base基类的类
            filters(dict): WHERE 条件
        """
        with self.get_session() as session:
            session.query(model).filter_by(**filters).delete()
            session.commit()

    def select(
            self,
            model: type[Base],
            filters: dict,
            *,first: bool=False
            )  -> Union[Base, list[Base], None]:
        """
        在数据库查询条目
        说真的，你有多想不开要用这些增改删查方法，直接用upsert好了
        不对，这个不能用upsert

        Args:
            model(type[Base]): ORM模型，接受所有继承于models里的Base基类的类
            filters(dict): WHERE 条件
            first(boolean): 是否只返回第一条 default=False
        """
        with self.get_session() as session:
            query = session.query(model)
            if filters:
                query = query.filter_by(**filters)
            return query.first() if first else query.all()

    def upsert(self, model: type[Base], data: dict) -> None:
        """
        在数据库插入或者更新条目
        SQLite 专用 UPSERT
        SQLite3.24最伟大的发明

        Args:
            model(type[Base]): ORM模型，接受所有继承于models里的Base基类的类
            data(dict): 要写入的数据
        """
        with self.get_session() as session:
            stmt = insert(model).values(**data)
            primary_keys = [c.name for c in model.__table__.primary_key]
            update_data = {k: v for k, v in data.items() if k not in primary_keys}
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=primary_keys,
                set_=update_data
            )
            session.execute(upsert_stmt)
            session.commit()

    def cleanup_expired(
        self,
        model: type[Base],
        time_field: Any,
        minutes: int = 1
    ) -> int:
        """
        清理数据库中指定时间字段超时的条目

        Args:
            model(type[Base]): ORM 模型
            time_field(Any): 数据库模型中的datetime字段，如RecruitmentPosts.end_time
            minutes(int): 超时时间，单位分钟，默认1分钟

        Returns:
            int: 被删除的条目数量
        """
        now = datetime.now(BJ_TZ)  # 如果字段带时区可改成 datetime.now(BJ_TZ)
        threshold = now - timedelta(minutes=minutes)
        threshold = threshold.replace(microsecond=0)
        with self.get_session() as session:
            query = session.query(model).filter(time_field < threshold)
            count = query.count()
            query.delete(synchronize_session=False)
            session.commit()
            return count

class JsonIO:
    """
    该类负责读写json为字典

    Attr:
        base_dir(str): 存放json的目录
    """
    def __init__(self, base_dir: str) -> None:
        self.base_dir = Path(base_dir)

    def _full_path(self, filename: str) -> Path:
        """
        返回完整的 JSON 文件路径
        """
        path = self.base_dir / filename
        if path.suffix.lower() != ".json":
            path = path.with_suffix(".json")
        return path

    def load(self, filename: str) -> dict:
        """
        从指定文件名加载 JSON 数据

        Args:
            filename (str): JSON 文件名

        Returns:
            dict: JSON 内容
        """
        path = self._full_path(filename)
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, filename: str, data: dict) -> None:
        """
        将 dict 保存到指定文件名的 JSON 文件

        Args:
            filename (str): 文件名
            data (dict): 数据
        """
        path = self._full_path(filename)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
