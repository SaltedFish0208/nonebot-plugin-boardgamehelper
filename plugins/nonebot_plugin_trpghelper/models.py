from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class PostsModel(Base):
    __tablename__ = "recruitment_posts"

    recruitment_code: Mapped[str] = mapped_column(String, primary_key=True)
    publisher_user_id: Mapped[str] = mapped_column(String)
    publisher_name: Mapped[str] = mapped_column(String)
    rule: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    end_time: Mapped[datetime] = mapped_column(DateTime)

class BroadcastModel(Base):
    __tablename__ = "broadcast_groups"

    group_id: Mapped[str] = mapped_column(String, primary_key=True)
    group_name: Mapped[str] = mapped_column(String)

class PictpackMode(Base):
    __tablename__ = "picture_packs"

    pack_code: Mapped[str] = mapped_column(String, primary_key = True)
    pack_name: Mapped[str] = mapped_column(String)
    copyright_info: Mapped[str] = mapped_column(String)
    pack_like: Mapped[str] = mapped_column(String)
    pack_unlike: Mapped[str] = mapped_column(String)
    pack_download_link: Mapped[str] = mapped_column(String)
    pack_fast_download: Mapped[str] = mapped_column(String)
    pack_info: Mapped[str] = mapped_column(String)
