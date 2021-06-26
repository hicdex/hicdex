from dipdup.models import OperationData, Transaction, Origination, BigMapDiff, BigMapData, BigMapAction
from dipdup.context import HandlerContext, RollbackHandlerContext
from typing import Optional


import hicdex.models as models

from hicdex.types.objktbid_english.parameter.conclude_auction import ConcludeAuctionParameter
from hicdex.types.objktbid_english.storage import ObjktbidEnglishStorage


async def on_conclude_english(
    ctx: HandlerContext,
    conclude_auction: Transaction[ConcludeAuctionParameter, ObjktbidEnglishStorage],
) -> None:
    auction_model = await models.EnglishAuction.filter(id=int(conclude_auction.parameter)).get()
    auction_model.status=2
    await auction_model.save()
