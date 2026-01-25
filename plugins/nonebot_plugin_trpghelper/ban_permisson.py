from nonebot import get_driver
from nonebot.adapters import Event
from nonebot.permission import Permission

driver = get_driver()
config = driver.config

overwatchs = set(map(str, getattr(config, "overwatch", [])))

def is_publisher(event: Event) -> bool:
    user_id = str(event.get_user_id())
    return user_id in overwatchs

OVERWATCH = Permission(is_publisher)
