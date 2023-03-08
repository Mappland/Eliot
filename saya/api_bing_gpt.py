import pathlib,re, asyncio,json
 
from graia.saya.channel import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
 
from graia.ariadne import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.twilight import Twilight,UnionMatch,WildcardMatch,RegexResult,ArgumentMatch,ArgResult
from graia.ariadne.model import Group,Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At
 
from EdgeGPT import Chatbot
 
from loguru import logger
 
# 依赖EdgeGPT库。需要有new bing的资格。
 
help_str = ".bing [--reset: 重置对话] [--ref: 对话显示引用] [text]"
 
channel = Channel.current()
channel.name("在线EdgeGPT")
channel.author("节雨竹")
channel.description(f"触发词 {help_str}")
 
botList = {}
 
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight(UnionMatch(".bing"),"reset" @ ArgumentMatch("--reset",action="store_true",optional=True),
        "ref" @ ArgumentMatch("--ref",action="store_true",optional=True),"text" @ WildcardMatch(optional=True))]
    )
)
async def 在线EdgeGPT(app:Ariadne, group:Group,member:Member,message:GroupMessage,text: RegexResult, reset: ArgResult,ref: ArgResult):
    if group.id not in botList.keys():
        # 需要Cookies.json
        botList[group.id] = [Chatbot(cookiePath=pathlib.Path(__file__).parent/"cookies.json"),asyncio.Lock()]
    logger.debug(botList)
    bot:Chatbot = botList[group.id][0]
    lock:asyncio.Lock = botList[group.id][1]
 
    if reset.matched:
        logger.info(f'重置[{group.name}{group.id}]的bot')
        await bot.close()
        if lock.locked():
            lock.release()
        await app.send_message(group,MessageChain("对话已重置"))
        return
 
    logger.info(text.result.display)
    if text.result.display == "":
        await app.send_message(group,MessageChain(help_str,f'\n当前状态: {"进程被锁" if lock.locked() else "进程自由"}'))
        return
 
    if lock.locked():
        await app.send_message(group,MessageChain(At(member)," 正在处理上一条消息, 请稍等"))
        return
    async with lock:
        resp = await bot.ask(prompt=text.result.display)
 
    try:
        resp_text:str = resp["item"]["messages"][-1]["text"]
        resp_refs:set[dict] = [r for r in resp["item"]["messages"][-1]["sourceAttributions"]] # ["seeMoreUrl"] 或 ["providerDisplayName"]
        resp_choices:set[str] = [c["text"] for c in resp["item"]["messages"][-1]["suggestedResponses"]]
    except Exception:
        await app.send_message(group,MessageChain(At(member)," 似乎出现了错误"))
        with open(pathlib.Path(__file__).parent/"log.txt",mode="a") as f:
            f.write("\n\n\n")
            f.write(json.dumps(resp))
        return
    logger.debug(resp_text)
    logger.debug(resp_choices)
    logger.debug(resp_refs)
    pattern = r"\[\^(\d+)\^\]"
    msg = re.sub(pattern, lambda m: "[" + m.group(1) + "]", resp_text)
    if ref.matched:
        if len(resp_refs) != 0:
            msg += "\n\n相关链接:"
            i = 1
            for ref in resp_refs:
                msg += "\n" + f'[{i}] {ref["seeMoreUrl"]} {ref["providerDisplayName"]}'
                i+=1
    if len(resp_choices) != 0:
        msg += "\n\n推荐回复:"
        i = 1
        for choice in resp_choices:
            msg += "\n" + f'{i}. {choice}'
            i += 1
    await app.send_message(group,MessageChain(At(member)," ",msg))