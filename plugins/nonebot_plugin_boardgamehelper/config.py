from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    boardgamehelper_database_url: str = "sqlite:///./data/BoardGameHelper/database.db"
    boardgamehelper_json_path: str = "./data/BoardGameHelper/json/"
