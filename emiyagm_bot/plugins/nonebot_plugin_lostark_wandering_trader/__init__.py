from nonebot import on_keyword
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from httpx import Response, AsyncClient


trader = on_keyword({"商人"}, priority=1)

async def get_data():
    async with AsyncClient() as client:
        res = await client.get("https://www.emrpg.com/plugin.php?fromServer=lostarkcn&serverId=14&uri=merchants/list&id=tj_emrpg")
        print(res.status_code)
        return res.status_code


@trader.handle()
async def _(matcher: Matcher, event: MessageEvent):

    if args := event.get_plaintext():
        if args == "商人":
            # await get_data()
            await trader.finish("收到了")

