import importlib
from functools import cmp_to_key
from pathlib import Path

from nonebot.log import logger
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="Nonebot2 Any 多平台服务",
    description="Nonebot2 多平台统一事件与消息统一构造发送",
    usage="提供多平台统一的事件接口与统一的消息构造发送",
    type="library",
    homepage="https://github.com/MelodyYuuka/nonebot-plugin-any",
    supported_adapters={
        "~onebot.v11",
        # "~qqguild",
        "~kaiheila",
    },
)


from .event import AnyEvent as AnyEvent
from .event import AnyGroupEvent as AnyGroupEvent
from .event import AnyGroupMsgEvent as AnyGroupMsgEvent
from .event import AnyMsgEvent as AnyMsgEvent
from .message import AnyMsg as AnyMsg
from .models import Group as Group
from .models import User as User
from .utils import Platform as Platform
from .utils import class_cmp

for module_path in (Path(__file__).parent / "adapters").iterdir():
    try:
        if module_path.is_dir():
            continue
        importlib.import_module(f"{__package__}.adapters.{module_path.stem}")
        logger.opt(colors=True).success(
            f"Successfully loaded AnyAdapter <y>{module_path.stem}</y>"
        )
    except ImportError:
        pass

for anycls, map in AnyEvent._event_map.items():
    sublist = list(map.keys())
    sublist.sort(key=cmp_to_key(class_cmp))
    AnyEvent._subevent_list[anycls] = sublist


__all__ = (
    "AnyEvent",
    "AnyGroupEvent",
    "AnyGroupMsgEvent",
    "AnyMsgEvent",
    "AnyMsg",
    "Platform",
)

# 给 nb 打补丁
from . import patch as patch
