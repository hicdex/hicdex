from typing import Optional

from dipdup.models import OperationData, Origination, Transaction
from dipdup.context import HandlerContext

import hicdex.models as models

from hicdex.types.objktbid_bid.parameter.swap import SwapParameter
from hicdex.types.objktbid_bid.storage import ObjktbidBidStorage


async def on_swap_bid(
    ctx: HandlerContext,
    swap: Transaction[SwapParameter, ObjktbidBidStorage],
) -> None:
    bid = await models.Bid.filter(id=swap.parameter.__root__).get()
    seller, _ = await models.Holder.get_or_create(address=swap.data.sender_address)

    bid.seller = seller
    bid.status = models.AuctionStatus.CONCLUDED
    await bid.save()
