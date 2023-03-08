# 主文件引用
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.message.chain import MessageChain, Image
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import (
    Twilight,
    FullMatch,
    RegexResult,
    WildcardMatch,
    ParamMatch
)
# 本文件实现引用
import httpx
import hashlib
from pathlib import Path
from config import yaml_data

channel = Channel.current()


def translate_get(lan,tem):
    q = str(tem)
    api_url = f"https://fanyi-api.baidu.com/api/trans/vip/translate?"
    api_id = yaml_data["Saya"]["Translate"]["APP_ID"]
    api_chain = yaml_data["Saya"]["Translate"]["APP_CHAIN"]
    chain1 = str(api_id)+str(q)+str(1435660288)+str(api_chain)
    sign = hashlib.md5(chain1.encode('utf8')).hexdigest()
    ask = str(api_url)+"q="+str(q)+"&from=auto&to="+str(lan) + \
         "&appid="+str(api_id)+"&salt=1435660288&sign="+str(sign)
    return ask

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight(
            [FullMatch("/翻译"), "lang" @ ParamMatch(), "anything" @ WildcardMatch()])],
    )
)
async def translate(app: Ariadne, group: Group, lang: RegexResult, anything: RegexResult):
    if str(lang.result)=="帮助":
        await app.send_message(group, MessageChain(
            [Image(path=Path("data", "imgs", "tom_cat.jpg"))],
            [Plain(f"\n用法：\n/翻译 目标语言(英语en;日语jp;韩语kor;中文zh,若不输入此项，则默认为汉译英) 你要翻译的东西\n")],
            [Plain(f"如：/翻译 en 你好")],
            [Plain(f"如：/翻译 你说的对，但是")]
        ))

    elif str(lang.result)=="语言":
        await app.send_message(group, MessageChain(
            [Image(path=Path("data", "imgs", "other_lan.jpg"))]
        ))

    elif lang.matched and anything.matched:
        ask=translate_get(str(lang.result),str(anything.result))
        async with httpx.AsyncClient() as client:
            r = await client.get(ask)
            result = r.json()["trans_result"][0]["dst"]
        await app.send_message(group, MessageChain(
            [Plain(f"翻译为：")],
            result)
        )
    elif lang.matched:
        ask=translate_get(str("en"),str(lang.result))
        async with httpx.AsyncClient() as client:
            r=await client.get(ask)
            result = r.json()["trans_result"][0]["dst"]
        await app.send_message(group,MessageChain([Plain(f"翻译为：{result}")]))