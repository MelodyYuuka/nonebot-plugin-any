from pathlib import Path
from typing import Any, cast

from nonebot.adapters.qqguild import Bot, Adapter
from nonebot.adapters.qqguild import Message as GuildMsg
from nonebot.adapters.qqguild import MessageSegment as GuildMsgSeg
from nonebot.adapters.qqguild.api import Channel, Guild, MessageGet, User
from nonebot.adapters.qqguild.event import MessageCreateEvent, MessageEvent
from nonebot.matcher import current_bot
from typing_extensions import override

from .. import AnyGroupMsgEvent, AnyMsgEvent
from ..message import AnyMsgHandler, AnyMsgSeg
from ..utils import Platform, register_platform


register_platform(Platform.QQGuild, Bot, Adapter)


class MsgEvent(AnyMsgEvent[MessageEvent]):
    platform = Platform.QQGuild

    @property
    @override
    def user_id(self) -> str:
        return self.event.author.id  # type: ignore

    @property
    @override
    def name(self) -> str:
        return self.event.author.username  # type: ignore

    @property
    @override
    def message(self) -> GuildMsg:
        return self.event.get_message()

    @property
    @override
    def image(self) -> list[str]:
        return [
            "http://" + seg.data["url"]
            for seg in self.message
            if (seg.type == "attachment") and ("url" in seg.data)
        ]

    @override
    async def get_user_info(self) -> User:
        return self.event.author  # type: ignore

    @override
    async def get_avatar_url(self) -> str:
        return self.event.author.avatar  # type: ignore

    @property
    @override
    def reply(self) -> MessageGet | None:
        return self.event.reply


class GroupMsgEvent(AnyGroupMsgEvent[MessageCreateEvent], MsgEvent):  # type: ignore
    @property
    @override
    def group_id(self) -> str:
        return self.event.guild_id  # type: ignore

    @property
    @override
    def channel_id(self) -> str:
        return self.event.channel_id  # type: ignore

    @override
    async def get_group_info(self) -> Guild:
        if not self._group_info:
            bot = cast(Bot, current_bot.get())
            self._group_info = await bot.get_guild(guild_id=int(self.group_id))
        return self._group_info

    async def get_channel_info(self) -> Channel:
        if not self._channel_info:
            bot = cast(Bot, current_bot.get())
            self._channel_info = await bot.get_channel(channel_id=int(self.channel_id))
        return self._channel_info

    @override
    async def get_group_name(self) -> str:
        return (await self.get_group_info()).name or ""

    @override
    async def get_channel_name(self) -> str:
        return (await self.get_channel_info()).name or ""


class MsgHandler(AnyMsgHandler[Bot, MessageEvent, GuildMsg]):
    platform = Platform.QQGuild

    @override
    @classmethod
    async def build(cls, msg: list[AnyMsgSeg]) -> list[GuildMsg]:
        result = GuildMsg()
        for seg in msg:
            match seg.type:
                case "at":
                    result.append(GuildMsgSeg.mention_user(seg.data))
                case "text":
                    data = seg.data
                    if result and result[-1].type == "text":
                        result[-1].data["text"] += data
                    else:
                        result.append(GuildMsgSeg.text(data))
                case "image":
                    data = seg.data
                    if isinstance(data, str):
                        if data.startswith("http"):
                            result.append(GuildMsgSeg.image(data))
                        else:
                            result.append(GuildMsgSeg.file_image(Path(data)))
                    else:
                        result.append(GuildMsgSeg.file_image(data))
                case "voice":
                    result.append(GuildMsgSeg.text("[QQ频道不让我发语音]"))
        return [result]

    @override
    @classmethod
    async def send(
        cls,
        bot: Bot,
        event: MessageEvent,
        msg: GuildMsg,
        at: bool = False,
        reply: bool = False,
    ) -> Any:
        if at:
            msg = GuildMsgSeg.mention_user(int(event.author.id)) + msg  # type: ignore
        if reply:
            msg = GuildMsgSeg.reference(event.id) + msg  # type: ignore
        await bot.send(event, msg)
