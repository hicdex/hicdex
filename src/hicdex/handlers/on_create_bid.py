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
    ...