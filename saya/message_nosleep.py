#发音频的
from graiax import silkcoder
#找多媒体文件的,以main.py为根目录
from pathlib import Path
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.ariadne.message.element import Voice
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def voice(app: Ariadne, group: Group, message: MessageChain):
    if message.display.strip() != "你怎么睡得着的":
        return
    voice_bytes = await silkcoder.async_encode(Path("data", "voices", "no_sleep.wav"))
    await app.send_message(group, MessageChain(Voice(data_bytes=voice_bytes)))