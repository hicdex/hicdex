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
    ...