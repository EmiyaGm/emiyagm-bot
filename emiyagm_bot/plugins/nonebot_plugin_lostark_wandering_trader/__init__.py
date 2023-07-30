from nonebot import on_keyword
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from httpx import Response, AsyncClient
import datetime


trader = on_keyword({"商人"}, priority=1)

async def get_data():
    async with AsyncClient() as client:
        headers = {
        'X-Ajax': '1',
        'Cookie': 'acw_tc=707c9fc716906220300653664e550e283e11113d450a6e9e21bb7af38e99ab; UBtd_671d_saltkey=l3nfa1If; UBtd_671d_lastvisit=1690618430; UBtd_671d_sid=Z6bM50; UBtd_671d_sendmail=1; UBtd_671d_lastact=1690622038%09plugin.php%09; UBtd_671d_saltkey=AMcqaqQh; UBtd_671d_lastvisit=1690616006; UBtd_671d_sid=PeEjTE; UBtd_671d_lastact=1690622255%09plugin.php%09; acw_tc=76b20f6b16906221102315601e4147a5e05cf53f9b496a18f9a8670e71ca6d',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.emrpg.com',
        'Connection': 'keep-alive'
        }
        res = await client.get("https://www.emrpg.com/plugin.php?fromServer=lostarkcn&serverId=14&uri=merchants/list&id=tj_emrpg", headers=headers)
        result = res.json().get('data' , [])
        return result


@trader.handle()
async def _(matcher: Matcher, event: MessageEvent):

    if args := event.get_plaintext():
        if args == "商人":
            result = await get_data()
            if len(result) != 0:
                response = ''
                for index,item in enumerate(result):
                    now = datetime.datetime.now()
                    # now_str = now.strftime('%H:%M:%S')
                    times = item.get('times', [])
                    for time in times:
                        time_obj = datetime.datetime.strptime(time, '%H:%M:%S')
                        logger.info(time)
                        if now.__lt__(time_obj):
                            logger.info(time)
                            break
                    if index != len(result) - 1:
                        response = response + item.get('region', '未知地区') + '的' + item.get('name', '未知商人') + '\n'
                    else:
                        response = response + item.get('region', '未知地区') + '的' + item.get('name', '未知商人')
                    
                await trader.finish(response)
            else:
                await trader.finish("暂无数据")

