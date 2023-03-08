# 主文件引用
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group, Member
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.element import Forward, ForwardNode, Image, Plain
from graia.ariadne.message.chain import MessageChain, Image
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import (
    Twilight,
    FullMatch,
    RegexResult,
    WildcardMatch,
)
# 本文件实现引用
import httpx
import random
import asyncio
import contextlib
from datetime import datetime
from config import yaml_data
channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight(
            [FullMatch("/涩图"), "tag"@WildcardMatch()]
        )],
    )
)
async def api_a60_pic(app: Ariadne, member: Member, group: Group, tag: RegexResult):

    if yaml_data["Saya"]["api_a60_pic"]["san"] == "r18":
        san = 6
    elif yaml_data["Saya"]["api_a60_pic"]["san"] == "r16":
        san = 4
    else:
        san = 2

    if tag.matched:
        if str(tag.result) == "info":
            await app.send_message(group, MessageChain([Plain("api:A60提供：api.a60.one\n完成日期2023.2.19 2:36")]))
            return
        tag_t = tag.result
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://api.a60.one:8443/get/tags/{tag_t}?num=3&san={san}")
            res = r.json()
        if res.get("code", False) == 200:
            # 构建合并消息
            forwardnode = [
                ForwardNode(
                    senderId=member.id,
                    time=datetime.now(),
                    senderName=member.name,
                    messagechain=MessageChain([Plain(f"如下：")]),
                )
            ]
            group_members = await app.get_member_list(group)
            # 发送所得请求的所有图片
            for pic in res["data"]["imgs"]:
                member_choiced = random.choice(group_members)
                forwardnode.append(
                    ForwardNode(
                        senderId=member_choiced.id,
                        time=datetime.now(),
                        senderName=member_choiced.name,
                        messageChain=MessageChain(
                            [
                                Plain(f"ID:{pic['pic']}\n"),
                                Plain(f"name:{pic['name']}\n"),
                                Plain(f"userid:{pic['userid']}\n"),
                            ]
                        )
                    )
                )
                forwardnode.append(
                    ForwardNode(
                        senderId=member_choiced.id,
                        time=datetime.now(),
                        senderName=member_choiced.name,
                        messageChain=MessageChain(
                            [
                                Image(url=pic['url']),
                            ]
                        )
                    )
                )
            message_send = MessageChain(Forward(nodeList=forwardnode))
        msg = await app.send_message(group, message_send)

        if yaml_data["Saya"]["api_a60_pic"]["Recall"]:
            await asyncio.sleep(min(yaml_data["Saya"]["Pixiv"]["Interval"], 110))
            with contextlib.suppress(Exception):
                await app.recallMessage(msg)
        elif san == 6:
            await asyncio.sleep(min(yaml_data["Saya"]["Pixiv"]["Interval"], 110))
            with contextlib.suppress(Exception):
                await app.recallMessage(msg)
    else:
        await app.send_message(group, MessageChain(Plain("慢一点别冲啦")))
