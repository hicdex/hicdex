from dipdup.models import OperationData, Transaction, Origination, BigMapDiff, BigMapData, BigMapAction
from dipdup.context import HandlerContext, RollbackHandlerContext
from typing import Optional


import hicdex.models as models

from hicdex.types.objktbid_english.parameter.cancel_auction import CancelAuctionParameter
from hicdex.types.objktbid_english.storage import ObjktbidEnglishStorage


async def on_cancel_english(
    ctx: HandlerContext,
    cancel_auction: Transaction[CancelAuctionParameter, ObjktbidEnglishStorage],
) -> None:
    auction_model = await models.EnglishAuction.filter(id=int(cancel_auction.parameter.__root__)).get()
    auction_model.status = models.AuctionStatus.CANCELED
    await auction_model.save()
