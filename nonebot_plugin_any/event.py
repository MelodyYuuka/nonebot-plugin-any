import abc
import importlib
import inspect
from collections import defaultdict
from functools import cmp_to_key
from pathlib import Path
from types import GenericAlias
from typing import Any, ClassVar, Generic, TypeVar, get_args, get_origin

from nonebot import logger
from nonebot.adapters import Event, Message, MessageSegment

from .utils import Platform, class_cmp

TE = TypeVar("TE", bound=Event)


class AnyEvent(abc.ABC, Generic[TE]):
    """
    说明：

        任意事件 基类

    """

    _event_map: ClassVar[
        defaultdict[type["AnyEvent"], dict[type[Event], type["AnyEvent"]]]
    ] = defaultdict(dict)
    _subevent_list: ClassVar[dict[type["AnyEvent"], list[type[Event]]]] = {}

    event: TE
    platform: Platform

    def __init_subclass__(cls) -> None:
        orig_bases: tuple[GenericAlias, ...] | None = getattr(
            cls, "__orig_bases__", None
        )
        if orig_bases is None:
            raise RuntimeError("这么虎啊，不写泛型")
        orig = orig_bases[0]
        if not issubclass(get_origin(orig), AnyEvent):
            raise RuntimeError("首个父类不是 AnyEvent 或其子类")
        args = get_args(orig)[0]
        if not isinstance(args, TypeVar):
            event: type[TE] = args
            classes = inspect.getmro(cls)
            for base in classes:
                if base is object:
                    continue
                if event in AnyEvent._event_map[base].keys():
                    logger.warning(
                        f"{base=} {event=} 的 Anymap={AnyEvent._event_map[base][event]} 被 {cls} 覆盖"
                    )
                AnyEvent._event_map[base][event] = cls
        return super().__init_subclass__()

    def __init__(self, event: TE) -> None:
        self.event = event
        self._user_info = None
        super().__init__()

    @classmethod
    def solve(cls, event: Event):
        if anycls := cls._event_map[cls].get(type(event)):
            return anycls(event)
        for anyevent in cls._subevent_list[cls]:
            if isinstance(event, anyevent):
                return cls._event_map[cls][anyevent](event)
        return None

    @property
    def to_me(self) -> bool:
        "获取事件是否与机器人有关的方法。"
        return self.event.is_tome()


class AnyMsgEvent(AnyEvent[TE]):
    """
    说明：

        任意消息事件 基类

    """

    @property
    @abc.abstractmethod
    def message(self) -> Message[MessageSegment]:
        "用户消息"
        raise NotImplementedError

    @property
    def plaintext(self) -> str:
        "用户消息纯文本内容"
        return self.event.get_plaintext()

    text = plaintext
    "用户消息纯文本内容"

    @property
    @abc.abstractmethod
    def image(self) -> list[str]:
        "用户消息所有图片的链接"
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def user_id(self) -> str:
        "用户 id"
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        "用户昵称"
        raise NotImplementedError

    @abc.abstractmethod
    async def get_user_info(self) -> Any:
        "用户信息，各平台实现不同"
        raise NotImplementedError

    @abc.abstractmethod
    async def get_avatar_url(self) -> str:
        "用户头像链接"
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def reply(self) -> Any | None:
        "回复"
        raise NotImplementedError
    
    @property
    def user_rich_id(self) -> str:
        "含平台名的用户 id"
        return f"{self.platform.name}-{self.user_id}"


class AnyGroupEvent(AnyEvent[TE]):
    """
    说明：

        任意群聊事件 基类

    """

    def __init__(self, event: TE) -> None:
        self._group_info = None
        self._channel_info = None
        super().__init__(event)

    @abc.abstractmethod
    async def get_group_info(self) -> Any:
        "群聊信息，各平台实现不同"
        raise NotImplementedError

    @abc.abstractmethod
    async def get_channel_info(self) -> Any:
        "子频道信息，各平台实现不同"
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def group_id(self) -> str:
        "一级群聊 id"
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def channel_id(self) -> str:
        "二级群聊 id，若无二级群聊则为一级群聊 id"
        raise NotImplementedError

    @abc.abstractmethod
    async def get_group_name(self) -> str:
        "一级群聊名"
        raise NotImplementedError

    @abc.abstractmethod
    async def get_channel_name(self) -> str:
        "二级群聊名，若无二级群聊则为一级群聊名"
        raise NotImplementedError

    @property
    def group_rich_id(self) -> str:
        "含平台名的一级群聊 id"
        return f"{self.platform.name}-{self.group_id}"

    @property
    def channel_rich_id(self) -> str:
        "含平台名的二级群聊 id"
        return f"{self.platform.name}-{self.channel_id}"


class AnyGroupMsgEvent(AnyMsgEvent[TE], AnyGroupEvent[TE]):
    """
    说明：

        任意群聊消息事件 基类

    """


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
