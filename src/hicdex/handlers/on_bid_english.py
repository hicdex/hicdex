from dipdup.models import OperationData, Transaction, Origination, BigMapDiff, BigMapData, BigMapAction
from dipdup.context import HandlerContext, RollbackHandlerContext
from typing import Optional


import hicdex.models as models

from hicdex.types.objktbid_english.parameter.bid import BidParameter
from hicdex.types.objktbid_english.storage import ObjktbidEnglishStorage


async def on_bid_english(
    ctx: HandlerContext,
    bid: Transaction[BidParameter, ObjktbidEnglishStorage],
) -> None:
    auction_model = await models.EnglishAuction.filter(id=int(bid.parameter.__root__)).get()
    auction_model.highest_bid = bid.data.amount
    auction_model.highest_bidder = bid.data.sender_address
    await auction_model.save()