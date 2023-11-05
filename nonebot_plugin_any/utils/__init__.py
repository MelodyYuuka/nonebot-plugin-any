import asyncio
from enum import Enum, auto
from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

import nonebot
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.adapters import Bot as BaseBot
from nonebot.matcher import current_bot

Param = ParamSpec("Param")
Return = TypeVar("Return", bound=Any)


class Platform(Enum):
    """
    说明：

        平台类型枚举

    """

    OneBotV11 = auto()
    KOOK = auto()
    QQGuild = auto()


def class_cmp(cls1: type, cls2: type):
    """
    说明：

        按照 子类 > 父类的排序比较函数，可搭配 `functools.cmp_to_key` 使用

    参数:

        * ``cls1``: 类 1
        * ``cls2``: 类 2

    """
    if issubclass(cls1, cls2):
        return -1
    elif issubclass(cls2, cls1):
        return 1
    else:
        return 0


bot2platform: dict[type[BaseBot], Platform] = {}
platform2bot: dict[Platform, type[BaseBot]] = {}
platform2adapter: dict[Platform, type[BaseAdapter]] = {}


def register_platform(
    platform: Platform, bot: type[BaseBot], adapter: type[BaseAdapter]
):
    bot2platform[bot] = platform
    platform2bot[platform] = bot
    platform2adapter[platform] = adapter


def get_platform_adapter(platform: Platform) -> type[BaseAdapter]:
    """
    说明：

        获取该平台的 Adapter

    参数:

        * ``platform``: 平台

    """
    try:
        return platform2adapter[platform]
    except KeyError:
        raise NotSupportException("不支持的平台") from None


def get_current_platform(bot: BaseBot | None = None) -> Platform:
    """
    说明：

        获取当前平台

    """
    bot = bot or current_bot.get()
    try:
        return bot2platform[type(bot)]
    except KeyError:
        raise NotSupportException("不支持的平台") from None


def get_platform_bot_cls(platform: Platform) -> type[BaseBot]:
    """
    说明：

        获取该平台的 Bot 类

    参数:

        * ``platform``: 平台

    """
    try:
        return platform2bot[platform]
    except KeyError:
        raise NotSupportException("不支持的平台") from None


def get_platform_bot(platform: Platform) -> BaseBot:
    """
    说明：

        获取该平台的 Bot 对象

    参数:

        * ``platform``: 平台

    """
    bot = current_bot.get()
    if not isinstance(bot, get_platform_bot_cls(platform)):
        bot = next(
            iter(nonebot.get_adapter(get_platform_adapter(platform)).bots.values())
        )
    return bot


class NotSupportException(Exception):
    """
    说明：

        不支持的操作 异常

    """


def async_retry(
    exceptions: type[Exception] | tuple[type[Exception], ...] = Exception,
    max_tries: int = -1,
    delay: int = 0,
):
    """
    说明：

        异步重试装饰器

    参数:

        * ``exceptions``: 捕获异常类型
        * ``max_tries``: 最多重试次数, 为-1则无限
        * ``delay``: 每次重试延迟

    """

    def wrap(
        func: Callable[Param, Coroutine[None, None, Return]]
    ) -> Callable[Param, Coroutine[None, None, Return]]:
        @wraps(func)
        async def _wrapper(*args: Param.args, **kwargs: Param.kwargs) -> Return:
            i = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    i += 1
                    if max_tries != -1 and i >= max_tries:
                        raise e
                if delay:
                    await asyncio.sleep(delay)

        return _wrapper

    return wrap


from .requests import Requests as Requests
