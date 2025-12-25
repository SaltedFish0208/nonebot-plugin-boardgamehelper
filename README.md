<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-boardgamehelper/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-boardgamehelper/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-boardgamehelper

_✨ NoneBot 桌游约车助手 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/SaltedFish0208/nonebot-plugin-boardgamehelper.svg" alt="license">
</a>
<!--
<a href="https://pypi.python.org/pypi/nonebot-plugin-boardgamehelper">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-boardgamehelper.svg" alt="pypi">
</a>
-->
<img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="python">

</div>


## 📖 介绍

该插件是一个 NoneBot2 桌游约车助手插件，提供桌游群招募、发车、封车等功能。

## 💿 安装
<!--
<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-boardgamehelper

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-boardgamehelper
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-boardgamehelper
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-boardgamehelper
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-boardgamehelper
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_boardgamehelper"]

</details>
-->
目前仅能通过源代码安装
之后会传到pypi上的

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|               配置项               |  必填 |                       默认值                      | 说明                      |
| :-----------------------------: | :-: | :--------------------------------------------: | :---------------------- |
| `BOARDGAMEHELPER_DATABASE_PATH` |  否  | `sqlite:///./data/BoardGameHelper/database.db` | 插件数据库路径，应使用 SQLite URI |
|   `BOARDGAMEHELPER_JSON_PATH`   |  否  |         `./data/BoardGameHelper/json/`         | JSON 数据存储路径，用于保存配置文件 |


## 🎉 使用
### 指令表
|    指令   |      权限     | 需要@ |   范围  |        说明       |
| :-----: | :---------: | :-: | :---: | :-------------: |
|   发车   |      用户     |  否  | 私聊/群聊 |   发布一条新的桌游招募信息  |
|   封车   |      用户     |  否  | 私聊/群聊 |    关闭自己的桌游招募    |
|   查车   |      用户     |  否  |   群聊  | 查看当前正在公开的桌游招募信息 |
| 开启全群广播 | 超级用户/群主/管理员 |  否  |   群聊  |     开启桌游招募广播    |
| 关闭全群广播 | 超级用户/群主/管理员 |  否  |   群聊  |     关闭桌游招募广播    |
|  强制封车  |     超级用户    |  否  |   群聊  |    强制关闭一条桌游招募   |
