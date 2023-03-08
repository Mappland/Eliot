# 主文件引用
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import (
    Twilight,
    FullMatch,
    RegexResult,
    WildcardMatch,
    ParamMatch
)

# 本文件实现引用
import random


channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight(
            [FullMatch("/骰子"), "range1" @ ParamMatch(), "range2" @ ParamMatch(), "num" @ ParamMatch(), "dice_event" @ WildcardMatch()])],))
async def dice(app: Ariadne, group: Group, range1: RegexResult, range2: RegexResult, num: RegexResult, dice_event: RegexResult):
    print(range1.result,"\t",range2.result,"\t",num.result,"\t",dice_event.result)
    if range1.matched and str(range1.result) == "he":
        await app.send_group_message(group,MessageChain(
            [Plain(f"用法：/骰子 数值起始范围 数值结束范围 骰子数量 事件\n")],
            [Plain(f"如： /骰子 1 100 5 我抽卡出金的概率是\n")],
            [Plain(f"回复： 我抽卡出金的概率是：\n2  87  98  10 7")]
        ))
    elif range1.matched and range2.matched and num.matched and dice_event.matched:
        str_send = str(dice_event.result)+":\n"
        for x in range(1, int(str(num.result))+1):
            str_send += str(random.choice(range(int(str(range1.result)), int(str(range2.result))+1)))
            str_send += "  "
            str_send =str(str_send)
        await app.send_group_message(group,MessageChain(str_send))
    elif range1.matched and str(range1.result)=="in":
        await app.send_group_message(group,MessageChain(
            [Plain(f"骰子应用 完成于2023.2.27 22:35\n")]
        ))