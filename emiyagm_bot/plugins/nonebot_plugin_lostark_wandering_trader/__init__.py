from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot import on_keyword, require, get_bot, get_bots
from httpx import Response, AsyncClient
import datetime

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

@scheduler.scheduled_job("cron", minute="*/1", id="check_trader", args=[1], kwargs={"arg2": 2})
async def check_trader(arg1, arg2):
    bot = get_bot(str(2692607936))
    now = datetime.datetime.now()

    hour = str(now.hour)

    date = datetime.datetime.now().date().isoformat()
    time_start = datetime.datetime.strptime( date + ' ' + hour + ':30:00', '%Y-%m-%d %H:%M:%S')
    time_one = datetime.datetime.strptime( date + ' ' + hour + ':35:00', '%Y-%m-%d %H:%M:%S')
    time_two = datetime.datetime.strptime( date + ' ' + hour + ':55:00', '%Y-%m-%d %H:%M:%S')

    response = ''

    if now < time_two and now > time_one:
        result = await get_detail(int(time_start.timestamp()))
        if len(result) != 0:
            for item in enumerate(result):
                card = item.get('_card', {})
                rarity = card.get('rarity', '')
                if rarity == 'Rare':
                    response = response + '出卡牌了！'
                    await bot.call_api('send_private_msg', **{
                        'user_id': 464723943,
                        'message': response
                    })
            

trader = on_keyword({"商人"}, priority=1)

async def get_detail(displayAt):
     async with AsyncClient() as client:
        headers = {
        'X-Ajax': '1',
        'Cookie': 'acw_tc=707c9fc716906220300653664e550e283e11113d450a6e9e21bb7af38e99ab; UBtd_671d_saltkey=l3nfa1If; UBtd_671d_lastvisit=1690618430; UBtd_671d_sid=w61IJF; UBtd_671d_lastact=1690623811%09plugin.php%09; UBtd_671d_sid=O3zbk8; UBtd_671d_lastact=1690799529%09plugin.php%09',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.emrpg.com',
        'Connection': 'keep-alive'
        }
        res = await client.get(f"https://www.emrpg.com/plugin.php?displayAt={displayAt}&fromServer=lostarkcn&serverId=14&uri=merchants/active&_pipes=withCard,withRapport,withLocation,withMember&id=tj_emrpg", headers=headers)
        result = res.json().get('data' , [])
        return result

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
        if args == "下一个商人":
            result = await get_data()
            if len(result) != 0:
                response = ''
                for index,item in enumerate(result):
                    now = datetime.datetime.now()
                    # now_str = now.strftime('%H:%M:%S')
                    times = item.get('times', [])
                    for time in times:
                        date = datetime.datetime.now().date().isoformat()
                        time_obj = datetime.datetime.strptime( date + ' ' + time, '%Y-%m-%d %H:%M:%S')
                        if now.__lt__(time_obj):
                            response = response + item.get('region', '未知地区') + '的' + item.get('name', '未知商人') + '，即将在 ' + time_obj.strftime('%H:%M:%S')  + ' 时出现' + '\n'
                            break
                    # if index != len(result) - 1:
                    #     response = response + item.get('region', '未知地区') + '的' + item.get('name', '未知商人') + '\n'
                    # else:
                    #     response = response + item.get('region', '未知地区') + '的' + item.get('name', '未知商人')
                response = response + 'by: EmiyaGm'
                await trader.finish(response)
            else:
                await trader.finish("暂无数据")

