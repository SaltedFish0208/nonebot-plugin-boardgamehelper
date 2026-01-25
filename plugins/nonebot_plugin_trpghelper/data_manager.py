import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Literal, Optional, TypeVar, Union, overload
from zoneinfo import ZoneInfo

from sqlalchemy import URL, create_engine, update
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

ORM_Model = TypeVar("ORM_Model", bound=Base)
BJ_TZ = ZoneInfo("Asia/Shanghai")
"""
说真的，如果你能帮我重构一下这个部分就太好了
我真不擅长对付ORM

TODO: 迁移至nonebot-plugin-orm
"""

class DataBaseManager:
    """
    该类负责将数据写入数据库或将实例从数据库里读出

    Args:
        db_path("Path"): 指向数据库的path对象
    """
    def __init__(self, db_path: "Path") -> None:
        url = URL.create(drivername="sqlite", database=str(db_path))
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

    @overload
    def select(
        self,
        model: type[ORM_Model],
        filters: dict[Any, Any],
        *,first: Literal[True]
    ) -> Optional[ORM_Model]: ...

    @overload
    def select(
        self,
        model: type[ORM_Model],
        filters: dict[Any, Any],
        *,first: Literal[False] = False
    ) -> list[ORM_Model]: ...

    def select(
            self,
            model: type[ORM_Model],
            filters: dict[Any, Any],
            *,first: bool=False
            )  -> Union[ORM_Model, list[ORM_Model], None]:
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

    def _update_column(
            self,
            model: type[Base],
            new_value: dict
            ) -> None:
        """
        更新表中某一列的所有值

        Args:
            model: ORM模型类
            column_name: 要更新的列名
            new_value: 新值
            get_session: 获取数据库 session 的方法
        """
        with self.get_session() as session:
            stmt = update(model).values(new_value)
            session.execute(stmt)
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
    该类负责使用 pathlib 读写 JSON 文件为字典

    Attr:
        path ("Path"): 指向JSON文件的Path对象
    """
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> dict:
        """
        从 JSON 文件加载数据

        Returns:
            dict: JSON 内容，如果文件不存在返回空字典
        """
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data: dict) -> None:
        """
        将字典保存到 JSON 文件

        Args:
            data (dict): 要保存的数据
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8"
            )
