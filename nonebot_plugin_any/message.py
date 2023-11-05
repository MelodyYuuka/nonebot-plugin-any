import abc
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, ClassVar, Generic, Literal, NoReturn, TypeVar, Union

from nonebot.adapters import Bot as BaseBot
from nonebot.adapters import Event as BaseEvent
from nonebot.adapters import Message as BaseMsg
from nonebot.exception import FinishedException
from nonebot.matcher import current_bot, current_event
from typing_extensions import Self

from .utils import NotSupportException, Platform, get_current_platform


@dataclass(slots=True)
class AnyMsgSeg:
    """
    说明：

        任意消息 附属任意消息段

    """

    type: Literal["text", "image", "at", "voice"]
    data: Any


TB = TypeVar("TB", bound=BaseBot)
TE = TypeVar("TE", bound=BaseEvent)
TM = TypeVar("TM", bound=BaseMsg)


class AnyMsgHandler(abc.ABC, Generic[TB, TE, TM]):
    """
    说明：

        各平台消息发送处理器基类

    """

    _adapter_map: ClassVar[dict[Platform, type["AnyMsgHandler"]]] = {}
    platform: Platform

    def __init_subclass__(cls) -> None:
        if getattr(cls, "platform", None) is not None:
            cls._adapter_map[cls.platform] = cls
        return super().__init_subclass__()
    
    @classmethod
    def get_handler(cls, platform: Platform) -> type["AnyMsgHandler"]:
        return cls._adapter_map[platform]

    @classmethod
    @abc.abstractmethod
    async def build(cls, msg: list[AnyMsgSeg]) -> list[TM]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    async def send(
        cls,
        bot: TB,
        event: TE,
        msgs: TM,
        at: bool = False,
        reply: bool = False,
    ) -> Any:
        raise NotImplementedError


class AnyMsg:
    """
    说明：

        任意消息 构建器

    """

    def __init__(
        self, msg: Union[str, list[AnyMsgSeg], AnyMsgSeg, "AnyMsg", None] = None
    ) -> None:
        self._msg: list[AnyMsgSeg] = []
        if msg:
            if isinstance(msg, str):
                self.text(msg)
            elif isinstance(msg, list):
                self._msg.extend(msg)
            elif isinstance(msg, AnyMsgSeg):
                self._msg.append(msg)
            else:
                self._msg.extend(msg._msg)

    def __add__(self, other: str | Self) -> Self:
        result = self.copy()
        result += other
        return result

    def __radd__(self, other: str | Self) -> Self:
        result = AnyMsg(other)
        return result + self

    def __iadd__(self, other: str | Self) -> Self:
        if isinstance(other, str):
            return self.text(other)
        elif isinstance(other, AnyMsg):
            self._msg.extend(other._msg)
            return self
        else:
            raise NotSupportException("不支持的操作")

    def copy(self) -> Self:
        """
        说明：

            复制消息

        """
        return AnyMsg(self)

    def image(self, img: str | Path | bytes | BytesIO, is_temp: bool = False) -> Self:
        """
        说明：

            生成图片消息

        参数:

            * ``img``: 图片文件名/网址/路径/二进制数据
                - `文件名`: str
                - `网址`: str
                - `路径`: Path
                - `二进制数据`: bytes | BytesIO
            * ``is_temp``: 是否为缓存文件，当 img 为文件名时才有效

        """
        if isinstance(img, str) and not img.startswith("http"):
            img = Path(img)
        self._msg.append(AnyMsgSeg("image", img))
        return self

    def voice(self, voice: str | Path | bytes | BytesIO, is_temp: bool = False) -> Self:
        """
        说明：

            生成语音消息

        参数:

            * ``voice``: 图片文件名/网址/路径/二进制数据
                - `文件名`: str
                - `网址`: str
                - `路径`: Path
                - `二进制数据`: bytes | BytesIO
            * ``is_temp``: 是否为缓存文件，当 img 为文件名时才有效

        """
        if isinstance(voice, str) and not voice.startswith("http"):
            voice = Path(voice)
        self._msg.append(AnyMsgSeg("voice", voice))
        return self

    def text(self, text: str) -> Self:
        """
        说明：

            生成文本消息

        参数:

            * ``text``: 文本

        """
        if self._msg and self._msg[-1].type == "text":
            self._msg[-1].data += text
        else:
            self._msg.append(AnyMsgSeg("text", text))
        return self

    def at(self, user_id: str) -> Self:
        """
        说明：

            生成 提及他人 消息

        参数:

            * ``user_id``: 用户 id

        """
        self._msg.append(AnyMsgSeg("at", user_id))
        return self

    async def build(
        self, platform: Platform | None = None, bot: BaseBot | None = None
    ) -> list[BaseMsg]:
        """
        说明：

            构建消息

        参数:

            * ``platform``: 平台
            * ``bot``: 所使用的 Bot 对象

        """
        if platform is None:
            platform = get_current_platform(bot)
        return await AnyMsgHandler.get_handler(platform).build(self._msg)

    async def send(
        self, *, bot: BaseBot | None = None, at: bool = False, reply: bool = False
    ):
        """
        说明：

            发送消息

        参数:

            * ``bot``：指定 Bot，默认为 False
            * ``at``: 是否艾特事件主体. 默认为 False.
            * ``reply``: 是否回复消息. 默认为 False.

        """
        bot = bot or current_bot.get()
        event: Any = current_event.get()
        msgs = await self.build(bot=bot)
        platform = get_current_platform(bot)
        for msg in msgs:
            await AnyMsgHandler.get_handler(platform).send(bot, event, msg, at, reply)
            at = False

    async def finish(self, at: bool = False, reply: bool = False) -> NoReturn:
        """
        说明：

            完成消息

        参数:

            * ``at``: 是否艾特事件主体. 默认为 False.
            * ``reply``: 是否回复消息. 默认为 False.

        """
        await self.send(at=at, reply=reply)
        raise FinishedException
