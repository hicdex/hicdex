import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.objktbid_marketplace.parameter.fulfill_ask import FulfillAskParameter
from hicdex.types.objktbid_marketplace.storage import ObjktbidMarketplaceStorage


async def on_fulfill_ask(
    ctx: HandlerContext,
    fulfill_ask: Transaction[FulfillAskParameter, ObjktbidMarketplaceStorage],
) -> None:
    ask = await models.Ask.filter(id=fulfill_ask.parameter.__root__).get()
    seller = await ask.creator
    buyer, _ = await models.Holder.get_or_create(address=fulfill_ask.data.sender_address)

    fulfilled_ask = models.FulfilledAsk(
        ask=ask,
        seller=seller,
        buyer=buyer,
        objkt_id=ask.objkt_id,
        amount=1,
        level=fulfill_ask.data.level,
        timestamp=fulfill_ask.data.timestamp,
    )
    await fulfilled_ask.save()

    ask.amount_left -= 1  # type: ignore
    if ask.amount_left == 0:
        ask.status = models.AuctionStatus.CONCLUDED
        ask.update_level = fulfill_ask.data.level
        ask.update_timestamp = fulfill_ask.data.timestamp
    await ask.save()
