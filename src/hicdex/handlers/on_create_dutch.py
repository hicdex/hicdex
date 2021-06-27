from typing import Optional

from dipdup.models import OperationData, Origination, Transaction
from dipdup.context import HandlerContext

import hicdex.models as models

from hicdex.types.objktbid_dutch.parameter.create_auction import CreateAuctionParameter
from hicdex.types.objktbid_dutch.storage import ObjktbidDutchStorage


async def on_create_dutch(
    ctx: HandlerContext,
    create_auction: Transaction[CreateAuctionParameter, ObjktbidDutchStorage],
) -> None:
    auction_model = models.DutchAuction(
        id=int(create_auction.storage.auction_id) - 1,  # type: ignore
        fa2=create_auction.parameter.fa2,
        status=models.AuctionStatus.ACTIVE,
        objkt_id=create_auction.parameter.objkt_id,
        creator=create_auction.data.sender_address,
        start_time=create_auction.parameter.start_time,
        end_time=create_auction.parameter.end_time,
        start_price=create_auction.parameter.start_price,
        end_price=create_auction.parameter.end_price,

        timestamp=create_auction.data.timestamp,
        level=create_auction.data.level,
    )
    await auction_model.save()
