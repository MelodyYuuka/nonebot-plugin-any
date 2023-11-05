<!-- markdownlint-disable MD041 -->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">
  
# nonebot-plugin-any

🐝 [Nonebot2](https://github.com/nonebot/nonebot2) 多平台统一事件与统一消息构造发送 🐝
  
</div>

<p align="center">
  
  <a href="https://raw.githubusercontent.com/MelodyYuuka/nonebot_plugin_any/master/LICENSE">
    <img src="https://img.shields.io/github/license/MelodyYuuka/nonebot_plugin_any" alt="license">
  </a>

  <a href="https://pypi.python.org/pypi/nonebot-plugin-any">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/nonebot-plugin-any">
  </a>

  <a href="https://pypi.python.org/pypi/nonebot_plugin_any">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_any" alt="pypi">
  </a>
  
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.1.0+-green">
  </a>
  
  <a href="">
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
  </a>
  
</p>

## 介绍

本插件提供了 **统一事件接口** 与 **统一消息构造发送接口** ，方便您的插件在多个平台接收事件与发送消息。

本插件将各平台的 `事件`（`消息事件`， `群消息事件`）抽象出一个统一的 `AnyEvent`（`AnyMsgEvent`，`AnyGroupMsgEvent`），节约了开发者在适配多平台时所需要的额外时间。

同时也提供了 `AnyMsg`，来提供一套接口即可发送跨平台消息的能力，只需构建一次 `AnyMsg`使您的插件结构更为清晰优雅。

## 安装载入

- 通过 pip 或 nb-cli 安装

```shell
pip install nonebot-plugin-any
```

```shell
nb plugin install nonebot-plugin-any
```

- 并在您的bot.py中载入插件

```python
nonebot.load_plugin("nonebot_plugin_any")
```

## 目前支持

## 使用

```python

from nonebot import on_command, require
from nonebot.adapter import Bot as BaseBot

# 导入依赖
require("nonebot_plugin_any")

from plugins.nonebot_plugin_any import AnyMsgEvent, AnyGroupMsgEvent, AnyMsg, Platform

test = on_command("/ping", priority=1000)


@test.handle()
async def _(event: AnyMsgEvent):  # 接收多平台消息事件
    await AnyMsg("AnyMsgEvent pong!").send(at=True, reply=True) # 原生适配发送时 at 和 reply

@test.handle()
async def _(bot: BaseBot, event: AnyMsgEvent):
    msg = AnyMsg("prefix").image(Path("pong.png")).text("suffix") # 支持链式构造
    qqmsg = msg.build(platform=Platform.QQ)     # 构造 QQ 消息
    kookmsg = msg.build(platform=Platform.KOOK)     # 构造 KOOK 消息
    botmsg = msg.build(bot=bot)     # 根据 Bot 的类型构造对应消息
    await msg.send()      # 支持一个 AnyMsg 无限复用！

@test.handle()
async def _(event: AnyGroupMsgEvent): # 接收多平台群消息事件
    print(event.user_id)  # 各平台统一一个接口
    print(event.image)  # 便捷获取消息内图片链接
    await AnyMsg("AnyGroupMsgEvent pong!").finish() # 与 matcher.finish(xxx) 行为一致

```

```python
# 可以这样连接
AnyMsg("12345") + AnyMsg("67890")

# 也可以这样连接
AnyMsg("12345").text("67890")

# 还可以这样连接
AnyMsg("12345") + "67890"

# 这样连接也是完全没问题！
"12345" + AnyMsg("67890")
```

## 完善

- 本插件原本是 [`YuukaBot`](https://github.com/MelodyYuuka/YuukaBot-docs) 的功能之一，经魔法修改适配 `NoneBot2` 后在 `NoneBot2` 平台上作为插件。

- 本插件仍处于开发阶段，若有需要的特性，欢迎提 issue 与 pr

## 开源许可

- 本插件使用 `MIT` 许可证开源。
