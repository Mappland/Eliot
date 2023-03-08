#主文件引用
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Friend
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.message.chain import MessageChain,Image
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import FullMatch, Twilight

#本文件实现引用
import time
import httpx
from config import yaml_data
from graia.scheduler.timers import crontabify
from graia.scheduler.saya.schema import SchedulerSchema
channel = Channel.current()

master=yaml_data["Basic"]["Master"]
#8点定时发送
@channel.use(SchedulerSchema(crontabify("35 8 * * *")))
async def news_scheduled(app: Ariadne):
    await send(app)

#关键词触发发送
@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        inline_dispatchers=[Twilight([FullMatch("群发日报")])],))
async def news_keyword(app: Ariadne,friend:Friend):
    if(friend.id==master):
        await send(app)

#私人要日报
@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        inline_dispatchers=[Twilight([FullMatch("发送日报")])],))
async def news_person(app: Ariadne,friend:Friend):
    async with httpx.AsyncClient() as client:
        r = await client.get("http://api.2xb.cn/zaob")
        paperurl = r.json()["imageUrl"]
        r2 = await client.get(paperurl)
        paperimg = r2.content
    await app.send_friend_message(friend,MessageChain([Image(data_bytes=paperimg)]))

#群发日报
async def send(app: Ariadne):
    #应用开始事件
    starttime = time.time()
    #获取群列表
    groupList = (await app.get_group_list())
    #获取群数量
    groupNum = len(groupList)

    #向本人发送消息
    await app.send_friend_message(
        master,
        MessageChain([Plain(f"正在开始发送每日日报，当前共有 {groupNum} 个群")]),
    )

    #开始发送
    async with httpx.AsyncClient() as client:
        r = await client.get("http://api.2xb.cn/zaob")
        paperurl = r.json()["imageUrl"]
        r2 = await client.get(paperurl)
        paperimg = r2.content
    
    await app.send_friend_message(master,MessageChain([Image(data_bytes=paperimg)]))

    for group in groupList:
        try:
            await app.send_group_message(group, MessageChain([Image(data_bytes=paperimg)]))
        except Exception as err:
            await app.send_friend_message(
                master,
                MessageChain([Plain(f"{group.id} 的日报发送失败\n{err}")]),
            )

    #收尾
    allTime = time.time() - starttime
    await app.send_friend_message(
        master,
        MessageChain(f"每日日报已发送完毕，共用时 {int(allTime)} 秒"),
    )