#ariadne主程序
from graia.ariadne.app import Ariadne
#消息监听列表
from graia.ariadne.event.message import GroupMessage
#messageChain创立
from graia.ariadne.message.chain import MessageChain
#消息发送列表
from graia.ariadne.model import Group
#channel导入
from graia.saya import Channel
#监听器导入
from graia.saya.builtins.broadcast.schema import ListenerSchema
#messagechain图片选项
from graia.ariadne.message.element import Image
#图片储存库寻址，以main.py为根目录
from pathlib import Path

channel = Channel.current()
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def img(app: Ariadne, group: Group, message: MessageChain):
    if message.display.strip() != "不许狗叫":
        return
    await app.send_message(group, MessageChain(Image(path=Path("data", "imgs", "no_dog_beat.jpg"))))