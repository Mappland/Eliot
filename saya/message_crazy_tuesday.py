# 主文件引用
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage, MessageEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import FullMatch, Twilight

# 本文件实现引用
from pathlib import Path
import json
import random

doc_path = Path("data", "doc", "crazy_tuesday.json")
with doc_path.open("r", encoding="UTF-8") as f:
    TEMPLATES = json.loads(f.read())["post"]

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([FullMatch("疯狂星期四")])],))
async def something_scheduled(app: Ariadne, group: Group, event: MessageEvent):
    await app.send_message(
        event.sender.group if isinstance(
            event, GroupMessage) else event.sender,
        MessageChain(random.choice(TEMPLATES)),
    )

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([FullMatch("疯狂星期四_info")])],))
async def something_scheduled(app: Ariadne, group: Group, event: MessageEvent):
    await app.send_message(
        event.sender.group if isinstance(
            event, GroupMessage) else event.sender,
        MessageChain(Plain(f"功能完成时间：\n2023.1.20 23:26文案来源：\nGithub:  Cateon Huo   KafCoppelia\nurl: https://github.com/MinatoAquaCrews/nonebot_plugin_crazy_thursday/blob/beta/nonebot_plugin_crazy_thursday/post.json")),
    )