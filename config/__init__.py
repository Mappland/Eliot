import yaml
import json
from pathlib import Path
from loguru import logger


#应该是保持原来的yaml文件格式，忽略别名
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

CONFIG_PATH=Path("./config")


""" 将此路径与一个或多个参数组合，并返回表示子路径（如果所有参数都是相对路径）
    或完全不同路径（如果其中一个参数被锚定）的新路径。"""
#如果配置文件不存在且示例文件存在
if( not CONFIG_PATH.joinpath("config.yaml").exists()
    and CONFIG_PATH.joinpath("config_exp.yaml").exists()
):
    for i in range(1,3):
        logger.error("请添加config.yaml,例示在./config/config_exp.yaml")
    exit()
#配置文件和例示文件双双不存在
elif(
    not CONFIG_PATH.joinpath("config.yaml").exists()
    and CONFIG_PATH.joinpath("config_exp.yaml").exists()
):
    logger.error("敢不敢写一下配置文件")
    exit()
#载入配置文件
else:
    with CONFIG_PATH.joinpath("config.yaml").open("r",encoding="utf-8") as f:
        config_data=f.read()
    yaml_data=yaml.load(config_data,Loader=yaml.FullLoader)
    #载入菜单文件
    with CONFIG_PATH.joinpath("menu.yaml").open("r",encoding="utf-8") as f:
        menu_yaml_data=f.read()
    menu_data=yaml.load(menu_yaml_data,Loader=yaml.FullLoader)





#读取/创建群列表文件（黑名单和白名单）
if CONFIG_PATH.joinpath("grouplist.json").exists():
    with CONFIG_PATH.joinpath("grouplist.json").open("r", encoding="utf-8") as f:
        group_list = json.load(f)
else:
    with CONFIG_PATH.joinpath("grouplist.json").open("w", encoding="utf-8") as f:
        group_list = {"white": [], "black": []}
        json.dump(group_list, f, indent=2)
#读取/创建群配置文件
if CONFIG_PATH.joinpath("group_data.json").exists():
    with CONFIG_PATH.joinpath("group_data.json").open("r",encoding="utf-8") as f:
        group_data = json.load(f)
else:
    with CONFIG_PATH.joinpath("group_data.json").open("w",encoding="utf-8") as f:
        group_data={}
        json.dump(group_data,f,indent=2)



#读取/创建用户配置文件
if CONFIG_PATH.joinpath("userlist.json").exists():
    with CONFIG_PATH.joinpath("userlist.json").open("r", encoding="utf-8") as f:
        user_list = json.load(f)
else:
    with CONFIG_PATH.joinpath("userlist.json").open("w", encoding="utf-8") as f:
        user_list = {"black": []}
        json.dump(user_list, f, indent=2)



#读取saya配置文件
if(not CONFIG_PATH.joinpath("saya.yaml").exists()):
    logger.error("运行./config/action_saya_config.py以初始化saya配置文件")
    exit()
else:
    with CONFIG_PATH.joinpath("saya.yaml").open("r",encoding="utf-8") as f:
        saya_data=f.read()
    saya_config=yaml.load(saya_data,Loader=yaml.FullLoader)



#若文件并未完成配置
if not bool(yaml_data["Final"]):
    logger.error("并未完成配置文件并将文末的Final下改为true")
    exit()


def save_config():
    logger.info("正在保存配置文件")
    with CONFIG_PATH.joinpath("config.yaml").open("w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, Dumper=NoAliasDumper)
    with CONFIG_PATH.joinpath("groupdata.json").open("w", encoding="utf-8") as f:
        json.dump(group_data, f, indent=2, ensure_ascii=False)
    with CONFIG_PATH.joinpath("grouplist.json").open("w", encoding="utf-8") as f:
        json.dump(group_list, f, indent=2, ensure_ascii=False)
    with CONFIG_PATH.joinpath("userlist.json").open("w", encoding="utf-8") as f:
        json.dump(user_list, f, indent=2, ensure_ascii=False)


#COIN_NAME = yaml_data["Basic"]["CoinName"]
save_config()