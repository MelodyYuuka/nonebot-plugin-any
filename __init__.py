from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="Nonebot2 Any 多平台服务",
    description="Nonebot2 多平台统一事件与消息统一构造发送",
    usage="提供多平台统一的事件接口与统一的消息构造发送",
    type="library",
    homepage="https://github.com/MelodyYuuka/nonebot_plugin_any",
    supported_adapters={"~onebot.v11", "~qqguild", "~kaiheila"},
)


from . import patch as patch
from .event import AnyEvent as AnyEvent
from .event import AnyGroupEvent as AnyGroupEvent
from .event import AnyGroupMsgEvent as AnyGroupMsgEvent
from .event import AnyMsgEvent as AnyMsgEvent
from .utils import Platform as Platform
from .message import AnyMsg as AnyMsg
