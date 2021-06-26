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
    ...