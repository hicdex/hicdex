from typing import Optional

from dipdup.models import OperationData, Origination, Transaction
from dipdup.context import HandlerContext

import hicdex.models as models

from hicdex.types.objktbid_bid.parameter.bid import BidParameter
from hicdex.types.objktbid_bid.storage import ObjktbidBidStorage


async def on_create_bid(
    ctx: HandlerContext,
    bid: Transaction[BidParameter, ObjktbidBidStorage],
) -> None:
    bid_model = models.Bid(
        id=int(bid.storage.swap_id) - 1,  # type: ignore
        creator=bid.data.sender_address,
        objkt_id=bid.parameter.objkt_id,
        fa2=bid.parameter.fa2,
        price=bid.data.amount,
        status=models.AuctionStatus.ACTIVE,
        level=bid.data.level,
        timestamp=bid.data.timestamp,
    )
    await bid_model.save()

