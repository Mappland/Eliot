# 主文件引用
from config import yaml_data
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Friend
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.element import Plain
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import (
    Twilight,
    FullMatch,
    RegexResult,
    WildcardMatch,
)
channel = Channel.current()

# 本文件实现引用
import time
master = yaml_data["Basic"]["Master"]


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        inline_dispatchers=[Twilight(
            [FullMatch("公告"), "tem" @ WildcardMatch()])],
    ))
async def note(app: Ariadne, friend: Friend, tem: RegexResult):
    if (friend.id == master) and tem.matched:
        starttime = time.time()
        groupList = (await app.get_group_list())
        for group in groupList:
            try:
                await app.send_group_message(group, MessageChain(
                    [Plain("这里有一个公告：\n")], str(tem.result)
                ))
            except Exception as err:
                await app.send_friend_message(master, MessageChain(
                    [Plain(f"{group.id} 的公告发送失败\n{err}")]
                ))
        allTime = time.time() - starttime
        await app.send_friend_message(
            master,
            MessageChain(f"公告已发送完毕，共用时 {int(allTime)} 秒"),
        )
    else:
        await app.send_friend_message(friend.id, MessageChain(
            [Plain(f"你没有权限捏")]
        ))
