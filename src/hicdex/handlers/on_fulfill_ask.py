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
    ask = await models.Ask.filter(id=fulfill_ask.parameter.ask_id).get()
    seller = await ask.creator
    buyer, _ = await models.Holder.get_or_create(address=fulfill_ask.data.sender_address)

    fulfilled_ask = models.FulfilledAsk(
        ask=ask,
        seller=seller,
        buyer=buyer,
        objkt_id=ask.objkt_id,
        amount=int(fulfill_ask.parameter.objkt_amount),
        level=fulfill_ask.data.level,
        timestamp=fulfill_ask.data.timestamp,
    )
    await fulfilled_ask.save()

    ask.amount_left -= int(collect.parameter.objkt_amount)  # type: ignore
    if ask.amount_left == 0:
        ask.status = models.AuctionStatus.CONCLUDED
    await ask.save()
