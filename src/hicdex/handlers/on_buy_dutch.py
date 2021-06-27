from typing import Optional

from dipdup.models import OperationData, Origination, Transaction
from dipdup.context import HandlerContext

import hicdex.models as models

from hicdex.types.objktbid_dutch.parameter.buy import BuyParameter
from hicdex.types.objktbid_dutch.storage import ObjktbidDutchStorage

async def on_buy_dutch(
    ctx: HandlerContext,
    buy: Transaction[BuyParameter, ObjktbidDutchStorage],
) -> None:
    auction_model = await models.DutchAuction.filter(id=int(buy.parameter.__root__)).get()
    buyer, _ = await models.Holder.get_or_create(address=buy.data.sender_address)

    auction_model.buyer = buyer

    assert buy.data.amount is not None
    auction_model.buy_price = buy.data.amount

    auction_model.status=models.AuctionStatus.CONCLUDED
    await auction_model.save()
