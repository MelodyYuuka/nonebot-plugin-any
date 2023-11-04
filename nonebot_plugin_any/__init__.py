from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="Nonebot2 Any 多平台服务",
    description="Nonebot2 多平台统一事件与消息统一构造发送",
    usage="提供多平台统一的事件接口与统一的消息构造发送",
    type="library",
    homepage="https://github.com/MelodyYuuka/nonebot-plugin-any",
    supported_adapters={"~onebot.v11", "~qqguild", "~kaiheila"},
)


from .event import AnyEvent as AnyEvent
from .event import AnyGroupEvent as AnyGroupEvent
from .event import AnyGroupMsgEvent as AnyGroupMsgEvent
from .event import AnyMsgEvent as AnyMsgEvent
from .message import AnyMsg as AnyMsg
from .utils import Platform as Platform

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
