from typing import Any, Literal, cast

from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, Adapter
from nonebot.adapters.onebot.v11 import Message as QQMsg
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as QQMsgSeg
from nonebot.adapters.onebot.v11.event import Reply
from nonebot.matcher import current_bot
from typing_extensions import override

from .. import AnyGroupMsgEvent, AnyMsgEvent
from ..message import AnyMsgHandler, AnyMsgSeg
from ..utils import Platform, register_platform


register_platform(Platform.OneBotV11, Bot, Adapter)


class MsgEvent(AnyMsgEvent[MessageEvent]):
    platform = Platform.OneBotV11

    @property
    @override
    def user_id(self) -> str:
        return str(self.event.user_id)

    @property
    @override
    def name(self) -> str:
        return self.event.sender.nickname or ""

    @property
    def sex(self) -> Literal["男", "女", None]:
        sex = self.event.sender.sex
        if sex == "male":
            return "男"
        elif sex == "female":
            return "女"
        else:
            return None

    @property
    def age(self) -> int:
        return self.event.sender.age or 0

    @property
    @override
    def message(self) -> QQMsg:
        return self.event.message

    @property
    @override
    def image(self) -> list[str]:
        return [
            seg.data["url"]
            for seg in self.message
            if (seg.type == "image") and ("url" in seg.data)
        ]

    @override
    async def get_user_info(self):
        return self.event.sender

    @override
    async def get_avatar_url(self) -> str:
        return f"http://q1.qlogo.cn/g?b=qq&nk={self.user_id}&s=640"

    @property
    def self_id(self) -> int:
        return self.event.self_id

    @property
    @override
    def reply(self) -> Reply | None:
        return self.event.reply


class GroupMsgEvent(AnyGroupMsgEvent[GroupMessageEvent], MsgEvent):  # type: ignore
    @property
    @override
    def group_id(self) -> str:
        return str(self.event.group_id)

    @property
    @override
    def channel_id(self) -> str:
        return str(self.event.group_id)

    @override
    async def get_group_info(self) -> dict[str, Any]:
        if not self._group_info:
            bot = cast(Bot, current_bot.get())
            self._group_info = self._channel_info = await bot.get_group_info(
                group_id=self.event.group_id
            )
        return self._group_info

    @override
    async def get_channel_info(self) -> dict[str, Any]:
        if not self._channel_info:
            bot = cast(Bot, current_bot.get())
            self._group_info = self._channel_info = await bot.get_group_info(
                group_id=self.event.group_id
            )
        return self._channel_info

    @override
    async def get_group_name(self) -> str:
        return (await self.get_group_info())["group_name"]

    @override
    async def get_channel_name(self) -> str:
        return (await self.get_group_info())["group_name"]


class MsgHandler(AnyMsgHandler[Bot, Event, QQMsg]):
    platform = Platform.OneBotV11
    
    @override
    @classmethod
    async def build(cls, msg: list[AnyMsgSeg]) -> list[QQMsg]:
        msgs: list[QQMsg] = []
        result = QQMsg()
        for seg in msg:
            match seg.type:
                case "at":
                    result.append(QQMsgSeg.at(seg.data))
                case "text":
                    if result and result[-1].type == "text":
                        result[-1].data["text"] += seg.data
                    else:
                        result.append(QQMsgSeg.text(seg.data))
                case "image":
                    result.append(QQMsgSeg.image(seg.data))
                case "voice":
                    if result:
                        msgs.append(result)
                        result = QQMsg()
                    msgs.append(QQMsg(QQMsgSeg.record(seg.data)))
        if result:
            msgs.append(result)
        return msgs

    @override
    @classmethod
    async def send(
        cls,
        bot: Bot,
        event: Event,
        msg: QQMsg,
        at: bool = False,
        reply: bool = False,
    ) -> Any:
        await bot.send(event, msg, at_sender=at, reply_message=reply)
