# 主文件引用
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage, MessageEvent
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
import httpx
from config import yaml_data

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[
            Twilight([FullMatch("/APEX"), "action" @ ParamMatch(), "tem" @ WildcardMatch()])],
    )
)
async def apex_check(app: Ariadne, group: Group, action: RegexResult, tem: RegexResult,):
    if action.matched:
        if str(action.result) == "账户查询":
            url1 = "https://api.mozambiquehe.re/bridge?auth="
            chain = yaml_data["Saya"]["APEX_CHECK"]["API"]
            url = url1+chain+"&player="+str(tem.result)+"&platform=PC"
#            print(url)
            async with httpx.AsyncClient() as client:
                r = await client.get(url)
                nickname = r.json()["global"]["name"]
                level = r.json()["global"]["level"]
                rankscore = r.json()["global"]["rank"]["rankScore"]
                rankname = r.json()["global"]["rank"]["rankName"]
                ranklevel = r.json()["global"]["rank"]["rankDiv"]
                arenascore = r.json()["global"]["arena"]["rankScore"]
                arenaname = r.json()["global"]["arena"]["rankName"]
                arenalevel = r.json()["global"]["arena"]["rankDiv"]
                status = r.json()["realtime"]["currentStateAsText"]
                select = r.json()["realtime"]["selectedLegend"]
            await app.send_message(group, MessageChain(
                [Plain(f"昵称：")], nickname,
                [Plain(f"    等级：")], str(level),
                [Plain(f"\n在线状态：")], status,
                [Plain(f"    选择的传奇：")], select,
                [Plain(f"\n排位赛段位：")], rankname, [Plain(f" ")], str(ranklevel),
                [Plain(f"    排位赛积分：")], str(rankscore),
                [Plain(f"\n竞技场段位：")], arenaname, [
                    Plain(f" ")], str(arenalevel),
                [Plain(f"    竞技场积分：")], str(arenascore)
            ))
        elif str(action.result) == "地图轮换":
            url = "https://api.mozambiquehe.re/maprotation?auth=" + \
                str(yaml_data["Saya"]["APEX_CHECK"]["API"])+"&version=1"
            async with httpx.AsyncClient() as client:
                r = await client.get(url)
                battle_royale = r.json()["battle_royale"]["current"]["map"]
                arenas = r.json()["arenas"]["current"]["map"]
                rank = r.json()["ranked"]["current"]["map"]
                arenasrank = r.json()["arenasRanked"]["current"]["map"]
            await app.send_message(group, MessageChain(
                [Plain(f"大逃杀：")], str(battle_royale),
                [Plain(f"   竞技场：")], str(arenas),
                [Plain(f"\n排位赛：")], str(rank),
                [Plain(f"   竞技场排位赛：")], str(arenasrank)
            ))
        elif str(action.result) == "猎杀底分":
            url = "https://api.mozambiquehe.re/predator?auth=" + \
                yaml_data["Saya"]["APEX_CHECK"]["API"]
            async with httpx.AsyncClient() as client:
                r = await client.get(url)
                # PC平台
                rp_pc_rank = r.json()["RP"]["PC"]["foundRank"]
                rp_pc_value = r.json()["RP"]["PC"]["val"]
                rp_pc_master = r.json()["RP"]["PC"]["totalMastersAndPreds"]
                ap_pc_rank = r.json()["AP"]["PC"]["foundRank"]
                ap_pc_value = r.json()["AP"]["PC"]["val"]
                ap_pc_master = r.json()["AP"]["PC"]["totalMastersAndPreds"]
                # PS平台
                rp_ps_rank = r.json()["RP"]["PS4"]["foundRank"]
                rp_ps_value = r.json()["RP"]["PS4"]["val"]
                rp_ps_master = r.json()["RP"]["PS4"]["totalMastersAndPreds"]
                ap_ps_rank = r.json()["AP"]["PS4"]["foundRank"]
                ap_ps_value = r.json()["AP"]["PS4"]["val"]
                ap_ps_master = r.json()["AP"]["PS4"]["totalMastersAndPreds"]
                # switch平台
                rp_sw_rank = r.json()["RP"]["SWITCH"]["foundRank"]
                rp_sw_value = r.json()["RP"]["SWITCH"]["val"]
                rp_sw_master = r.json()["RP"]["SWITCH"]["totalMastersAndPreds"]
                ap_sw_rank = r.json()["AP"]["SWITCH"]["foundRank"]
                ap_sw_value = r.json()["AP"]["SWITCH"]["val"]
                ap_sw_master = r.json()["AP"]["SWITCH"]["totalMastersAndPreds"]
                # xbox平台
                rp_xb_rank = r.json()["RP"]["X1"]["foundRank"]
                rp_xb_value = r.json()["RP"]["X1"]["val"]
                rp_xb_master = r.json()["RP"]["X1"]["totalMastersAndPreds"]
                ap_xb_rank = r.json()["AP"]["X1"]["foundRank"]
                ap_xb_value = r.json()["AP"]["X1"]["val"]
                ap_xb_master = r.json()["AP"]["X1"]["totalMastersAndPreds"]
            await app.send_message(group, MessageChain(
                # PC
                [Plain(f"PC：\n大逃杀\n最低排名：")], str(rp_pc_rank),
                [Plain(f"   猎杀底分：")], str(rp_pc_value),
                [Plain(f"   大师总数：")], str(rp_pc_master),
                [Plain(f"\n竞技场\n猎杀最低排名：")], str(ap_pc_rank),
                [Plain(f"   猎杀底分：")], str(ap_pc_value),
                [Plain(f"   大师总数：")], str(ap_pc_master),
                # PS
                [Plain(f"\nPS：\n大逃杀\n最低排名：")], str(rp_ps_rank),
                [Plain(f"   猎杀底分：")], str(rp_ps_value),
                [Plain(f"   大师总数：")], str(rp_ps_master),
                [Plain(f"\n竞技场\n猎杀最低排名：")], str(ap_ps_rank),
                [Plain(f"   猎杀底分：")], str(ap_ps_value),
                [Plain(f"   大师总数：")], str(ap_ps_master),
                # XBOX
                [Plain(f"\nXbox：\n大逃杀\n最低排名：")], str(rp_xb_rank),
                [Plain(f"   猎杀底分：")], str(rp_xb_value),
                [Plain(f"   大师总数：")], str(rp_xb_master),
                [Plain(f"\n竞技场\n猎杀最低排名：")], str(ap_xb_rank),
                [Plain(f"   猎杀底分：")], str(ap_xb_value),
                [Plain(f"   大师总数：")], str(ap_xb_master),
                # switch
                [Plain(f"\nswitch：\n大逃杀\n最低排名：")], str(rp_sw_rank),
                [Plain(f"   猎杀底分：")], str(rp_sw_value),
                [Plain(f"   大师总数：")], str(rp_sw_master),
                [Plain(f"\n竞技场\n猎杀最低排名：")], str(ap_sw_rank),
                [Plain(f"   猎杀底分：")], str(ap_sw_value),
                [Plain(f"   大师总数：")], str(ap_sw_master)
            ))


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([FullMatch("APEX_info")])],))
async def something_scheduled(app: Ariadne, group: Group, event: MessageEvent):
    await app.send_message(
        event.sender.group if isinstance(
            event, GroupMessage) else event.sender,
        MessageChain(Plain(f"功能完成时间：\n2023.1.20 23:07 API: https://portal.apexlegendsapi.com/")),
    )
