import aiohttp
import time
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.message.element import Plain
from graia.saya.builtins.broadcast import ListenerSchema
from graia.ariadne.message.chain import MessageChain, Image
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.twilight import FullMatch, Twilight
channel = Channel.current()

signal: int = 0


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([FullMatch("来一张图")])],))
async def sendnews(app: Ariadne, group: Group):
    if globals()["signal"] >= 2:
        await app.send_message(group, MessageChain([Plain("队列已满，等会再说")]))
        return
    if globals()["signal"] < 2:
        pic_url = "https://iw233.cn/API/Random.php"
        async with aiohttp.ClientSession() as session:
            async with session.get(pic_url) as r:
                pic = await r.read()
        time.sleep(4)
        await app.send_message(group, MessageChain(Image(data_bytes=pic)))
