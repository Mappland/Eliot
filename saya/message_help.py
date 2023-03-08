#主文件引用
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import FullMatch, Twilight

channel = Channel.current()

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([FullMatch("菜单")])],))
async def help(app: Ariadne,group:Group):
    await app.send_message(group, MessageChain(
        [Plain(f"目前功能列表如下，如需获得相应功能的帮助，请发送：“关键字 帮助”，如“/翻译 帮助”\n")],
        [Plain(f"1.APEX查询 关键字/APEX\n")],
        [Plain(f"2.新闻发送\n   此功能为每天早上8:30分向群内发送\n")],
        [Plain(f"3.翻译 关键字/翻译\n")],
        [Plain(f"4.天气 关键字/天气\n")],
        [Plain(f"5.对于艾特本人的回复\n")],
        [Plain(f"6.对于“疯狂星期四”的回复 关键字 疯狂星期四 \n")],
        [Plain(f"7.对于“不许狗叫”的回复 关键字 不许狗叫 \n")],
        [Plain(f"8.对于“你怎么睡得着的”的回复 关键字 你怎么睡得着的\n")],
        [Plain(f"9.随机发送一张无h图片 关键字 来一张图\nP.S. 一次只发一张，不用尝试把一替换成亿了")],
        [Plain(f"\nPowered by Graia\nCreater: Mappland")],
        ))