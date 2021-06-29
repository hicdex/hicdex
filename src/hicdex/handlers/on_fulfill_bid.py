from typing import Optional

from dipdup.models import OperationData, Origination, Transaction
from dipdup.context import HandlerContext

import hicdex.models as models

from hicdex.types.objktbid_marketplace.parameter.fulfill_bid import FulfillBidParameter
from hicdex.types.objktbid_marketplace.storage import ObjktbidMarketplaceStorage


async def on_fulfill_bid(
    ctx: HandlerContext,
    fulfill_bid: Transaction[FulfillBidParameter, ObjktbidMarketplaceStorage],
) -> None:
    bid = await models.Bid.filter(id=fulfill_bid.parameter.__root__).get()
    seller, _ = await models.Holder.get_or_create(address=fulfill_bid.data.sender_address)

    bid.seller = seller
    bid.status = models.AuctionStatus.CONCLUDED
    await bid.save()