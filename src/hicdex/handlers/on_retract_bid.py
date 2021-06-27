from typing import Optional

from dipdup.models import OperationData, Origination, Transaction
from dipdup.context import HandlerContext

import hicdex.models as models

from hicdex.types.objktbid_bid.parameter.retract_bid import RetractBidParameter
from hicdex.types.objktbid_bid.storage import ObjktbidBidStorage


async def on_retract_bid(
    ctx: HandlerContext,
    retract_bid: Transaction[RetractBidParameter, ObjktbidBidStorage],
) -> None:
    bid = await models.Bid.filter(id=int(retract_bid.parameter.__root__)).get()
    bid.status = models.AuctionStatus.CANCELED
    await bid.save()
