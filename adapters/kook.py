from typing import Any, cast

from nonebot.adapters.kaiheila import Bot, Event, Adapter
from nonebot.adapters.kaiheila import Message as KookMsg
from nonebot.adapters.kaiheila import MessageSegment as KookMsgSeg
from nonebot.adapters.kaiheila.api import Channel, Guild
from nonebot.adapters.kaiheila.event import ChannelMessageEvent, MessageEvent
from nonebot.matcher import current_bot
from typing_extensions import override

from .. import AnyGroupMsgEvent, AnyMsgEvent
from ..message import AnyMsgHandler, AnyMsgSeg
from ..utils import Platform, get_platform_bot, register_platform
from ..utils.requests import Requests


register_platform(Platform.KOOK, Bot, Adapter)


class MsgEvent(AnyMsgEvent[MessageEvent]):
    platform = Platform.KOOK

    @property
    @override
    def user_id(self) -> str:
        return self.event.user_id

    @property
    @override
    def name(self) -> str:
        return self.event.extra.author.username  # type: ignore

    @property
    @override
    def message(self) -> KookMsg:
        return self.event.message

    @property
    @override
    def image(self) -> list[str]:
        return [
            seg.data["file_key"]
            for seg in self.message
            if (seg.type == "image") and ("file_key" in seg.data)
        ]

    @override
    async def get_user_info(self):
        if not self._user_info:
            bot = cast(Bot, current_bot.get())
            self._user_info = await bot.user_view(user_id=self.user_id)
        return self._user_info

    @override
    async def get_avatar_url(self) -> str:
        return cast(str, (await self.get_user_info()).avatar)

    @property
    @override
    def reply(self) -> None:
        return None


class GroupMsgEvent(AnyGroupMsgEvent[ChannelMessageEvent], MsgEvent):  # type: ignore
    @property
    @override
    def group_id(self) -> str:
        return cast(str, self.event.extra.guild_id)

    @property
    @override
    def channel_id(self) -> str:
        return self.event.group_id

    @override
    async def get_group_info(self) -> Guild:
        if not self._group_info:
            bot = cast(Bot, current_bot.get())
            self._group_info = await bot.guild_view(
                guild_id=cast(str, self.event.extra.guild_id)
            )
        return self._group_info

    @override
    async def get_channel_info(self) -> Channel:
        if not self._channel_info:
            bot = cast(Bot, current_bot.get())
            self._channel_info = await bot.channel_view(target_id=self.channel_id)
        return self._channel_info

    @override
    async def get_group_name(self) -> str:
        return cast(str, (await self.get_group_info()).name)

    @override
    async def get_channel_name(self) -> str:
        return cast(str, self.event.extra.channel_name)


class MsgHandler(AnyMsgHandler[Bot, Event, KookMsg]):
    platform = Platform.KOOK

    @override
    @classmethod
    async def build(cls, msg: list[AnyMsgSeg]) -> list[KookMsg]:
        msgs: list[KookMsg] = []
        result = KookMsg()
        bot = None
        for seg in msg:
            match seg.type:
                case "at":
                    result.append(KookMsgSeg.at(seg.data))
                case "text":
                    if result and result[-1].type == "text":
                        result[-1].data["content"] += seg.data
                    else:
                        result.append(KookMsgSeg.text(seg.data))
                case "image" | "voice":
                    if not isinstance(bot, Bot):
                        bot = cast(Bot, get_platform_bot(Platform.KOOK))
                    data = seg.data
                    if isinstance(data, str) and data.startswith("http"):
                        data = (await Requests.get(data)).content
                    file_key = await bot.upload_file(data)
                    result.append(
                        KookMsgSeg.image(file_key)
                        if seg.type == "image"
                        else KookMsgSeg.file(file_key)
                    )
        if result:
            msgs.append(result)
        return msgs

    @override
    @classmethod
    async def send(
        cls,
        bot: Bot,
        event: Event,
        msg: KookMsg,
        at: bool = False,
        reply: bool = False,
    ) -> Any:
        if at:
            msg = KookMsgSeg.at(event.user_id) + msg
        await bot.send(event, msg, reply_sender=reply)
