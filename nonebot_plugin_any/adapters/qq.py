from pathlib import Path
from typing import Any, cast

from nonebot.adapters.qq import Adapter, Bot
from nonebot.adapters.qq import Message as GuildMsg
from nonebot.adapters.qq import MessageSegment as GuildMsgSeg
from nonebot.adapters.qq.event import (
    GroupAtMessageCreateEvent,
    GuildMessageEvent,
    MessageCreateEvent,
    MessageEvent,
)
from nonebot.adapters.qq.models.guild import Message as MsgModel
from nonebot.matcher import current_bot
from typing_extensions import override

from .. import AnyGroupMsgEvent, AnyMsgEvent
from ..message import AnyMsgHandler, AnyMsgSeg
from ..models import Group, User
from ..utils import Platform, register_platform

register_platform(Platform.QQ, Bot, Adapter)


class MsgEvent(AnyMsgEvent[MessageEvent]):
    platform = Platform.QQ

    @property
    @override
    def user_id(self) -> str:
        return self.event.get_user_id()

    @property
    @override
    def name(self) -> str:
        if isinstance(self.event, GuildMessageEvent):
            return self.event.author.username or ""
        return ""

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
        if isinstance(self.event, GuildMessageEvent):
            return User(
                self.event.author.id,
                self.event.author.username or "",
                self.event.author.avatar,
            )
        else:
            return User(self.event.get_user_id())

    @override
    async def get_avatar_url(self) -> str | None:
        if isinstance(self.event, GuildMessageEvent):
            return self.event.author.avatar
        else:
            return None

    @property
    @override
    def reply(self) -> MsgModel | None:
        return self.event.reply


class GroupMsgEvent(AnyGroupMsgEvent[GroupAtMessageCreateEvent], MsgEvent):  # type: ignore
    @property
    @override
    def group_id(self) -> str:
        return self.event.group_id

    @property
    @override
    def channel_id(self) -> str:
        return self.event.group_id

    @override
    async def get_group_info(self) -> Group:
        return Group(self.group_id)

    async def get_channel_info(self) -> Group:
        return await self.get_group_info()

    @override
    async def get_group_name(self) -> str:
        return ""

    @override
    async def get_channel_name(self) -> str:
        return ""


class GuildMsgEvent(AnyGroupMsgEvent[MessageCreateEvent], MsgEvent):  # type: ignore
    @property
    @override
    def group_id(self) -> str:
        return self.event.guild_id

    @property
    @override
    def channel_id(self) -> str:
        return self.event.channel_id

    @override
    async def get_group_info(self) -> Group:
        if not self._group_info:
            bot = cast(Bot, current_bot.get())
            info = await bot.get_guild(guild_id=self.group_id)
            self._group_info = Group(
                info.id,
                info.name,
                info.icon,
                info.owner_id,
                info.member_count,
                info.max_members,
            )
        return self._group_info

    async def get_channel_info(self) -> Group:
        if not self._channel_info:
            bot = cast(Bot, current_bot.get())
            info = await bot.get_channel(channel_id=self.channel_id)
            self._channel_info = Group(
                info.id, info.name, None, info.owner_id, None, None
            )
        return self._channel_info

    @override
    async def get_group_name(self) -> str:
        return (await self.get_group_info()).name

    @override
    async def get_channel_name(self) -> str:
        return (await self.get_channel_info()).name


class MsgHandler(AnyMsgHandler[Bot, MessageEvent, GuildMsg]):
    platform = Platform.QQ

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
