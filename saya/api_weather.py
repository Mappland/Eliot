# 主文件引用
from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.element import Plain
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import (
    Twilight,
    FullMatch,
    RegexResult,
    WildcardMatch
)
# 本文件实现引用
import httpx
from config import yaml_data
from saya.api_translate import translate_get
channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[
            Twilight([FullMatch("/天气"), "city_zh" @ WildcardMatch()])],
    )
)

async def weather(app: Ariadne, group: Group, city_zh: RegexResult):
    if city_zh.matched:
        # 地名中转英
        tem = translate_get(str("en"),str(city_zh.result))
        async with httpx.AsyncClient() as client:
            recive_tran = await client.get(tem)
            city_en = recive_tran.json()["trans_result"][0]["dst"]
            city_en = str(city_en)
        
        # 获得城市ID
        url_city_id = "https://geoapi.qweather.com/v2/city/lookup?location="+city_en+"&key="+str(yaml_data["Saya"]["Weather"]["KEY"])
        async with httpx.AsyncClient() as client:
            r = await client.get(url_city_id)
            if r.json()["code"] == "404":
                await app.send_message(group, MessageChain([Plain(f"暂未找到该地方，请尝试取消尾部的区，市等，外国地名或考虑用英文地名查询")]))
                return
            city_id = r.json()["location"][0]["id"]
            country = r.json()["location"][0]["country"]+' '
            adm1 = r.json()["location"][0]["adm1"]+' '
            #print(len(r.json()["location"]))
            adm2 = r.json()["location"][0]["adm2"]+' '
            city_name = r.json()["location"][0]["name"]+' '
        

        # 获得城市天气
        url_weather = str("https://devapi.qweather.com/v7/weather/3d?")+str("location=")+str(city_id)+str("&key=")+str(yaml_data["Saya"]["Weather"]["KEY"])
        async with httpx.AsyncClient() as client:
            r = await client.get(url_weather)
            url_send = r.json()["fxLink"]
            today_tem_max = r.json()["daily"][0]["tempMax"]
            today_tem_min = r.json()["daily"][0]["tempMin"]
            today_day_weather = r.json()["daily"][0]["textDay"]
            today_night_weather=r.json()["daily"][0]["textNight"]
            nexday_tem_max = r.json()["daily"][1]["tempMax"]
            nexday_tem_min = r.json()["daily"][1]["tempMin"]
            nexday_day_weather = r.json()["daily"][1]["textDay"]
            nexday_night_weather=r.json()["daily"][0]["textNight"]
        await app.send_message(group, MessageChain(
            country, adm1, adm2, city_name,
            [Plain(f"\n白天天气为: ")],
            today_day_weather,
            [Plain(f"\n夜晚天气为: ")],
            today_night_weather,
            [Plain(f"\n温度区间在：")],
            today_tem_min,
            [Plain(f"~")],
            today_tem_max,
            [Plain(f"\n\n次日白天天气为: ")],
            nexday_day_weather,
            [Plain(f"\n次日夜晚天气为: ")],
            nexday_night_weather,
            [Plain(f"\n温度区间在：")],
            nexday_tem_min,
            [Plain(f"~")],
            nexday_tem_max,
            [Plain(f"\n天气来源：和风天气，详情消息请访问\n")],
            url_send
        )
        )
