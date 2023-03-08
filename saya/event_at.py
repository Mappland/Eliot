#主文件引用
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage
from graia.saya.builtins.broadcast import ListenerSchema
from graia.ariadne.message.chain import MessageChain,Image

#本文件实现引用
from pathlib import Path
from graia.ariadne.message.element import At
channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def get_at_nudge_message(app: Ariadne, group: Group, event: GroupMessage):
    if At(app.account) in event.message_chain:
        await app.send_message(group, MessageChain(Image(path=Path("data", "imgs", "no_dog_beat.jpg"))))