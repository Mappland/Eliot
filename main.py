from config import yaml_data, save_config, saya_config
import pkgutil
from pathlib import Path
from loguru import logger
from creart import create
from graia.saya import Saya
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import HttpClientConfig, WebsocketClientConfig, config

log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

#日志文件写入
LOGPATH = Path("./log")
LOGPATH.mkdir(exist_ok=True)
logger.add(
    LOGPATH.joinpath("lastest.log"),
    encoding="utf-8",
    backtrace=True,
    diagnose=True,
    rotation="00:00",
    retention="3 years",
    compression="tar.xz",
    colorize=True,

)
logger.info("eliot starting")


saya = create(Saya)
app = Ariadne(
    connection=config(
        yaml_data["Basic"]["Mah"]["BotNum"],
        yaml_data["Basic"]["Mah"]["VerifyKey"],
        HttpClientConfig(host=yaml_data["Basic"]["Mah"]["Http"]),
        WebsocketClientConfig(host=yaml_data["Basic"]["Mah"]["WebSocker"])
    )
)

with saya.module_context():
    for module_info in pkgutil.iter_modules(["saya"]):
        try:
            if saya_config['Saya'][module_info.name]['Disabled']:
                continue
        except KeyError:
            logger.error(module_info,"加载失败")
        saya.require(f"saya.{module_info.name}")
    logger.info("saya文件加载完成")

app.launch_blocking()
