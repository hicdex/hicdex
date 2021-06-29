from typing import Optional

from dipdup.models import OperationData, Origination, Transaction
from dipdup.context import HandlerContext

import hicdex.models as models

from hicdex.types.objktbid_marketplace.parameter.fulfill_ask import FulfillAskParameter
from hicdex.types.objktbid_marketplace.storage import ObjktbidMarketplaceStorage


async def on_fulfill_ask(
    ctx: HandlerContext,
    fulfill_ask: Transaction[FulfillAskParameter, ObjktbidMarketplaceStorage],
) -> None:
    ask = await models.Ask.filter(id=fulfill_ask.parameter.__root__).get()
    buyer, _ = await models.Holder.get_or_create(address=fulfill_ask.data.sender_address)

    ask.buyer = buyer
    ask.status = models.AuctionStatus.CONCLUDED
    await ask.save()