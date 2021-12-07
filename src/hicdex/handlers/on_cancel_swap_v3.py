from typing import Optional

from dipdup.models import OperationData, Origination, Transaction
from dipdup.context import HandlerContext

import hicdex.models as models

from hicdex.types.hen_swap_v3.parameter.cancel_swap import CancelSwapParameter
from hicdex.types.hen_swap_v3.storage import HenSwapV3Storage


async def on_cancel_swap_v3(
    ctx: HandlerContext,
    cancel_swap: Transaction[CancelSwapParameter, HenSwapV3Storage],
) -> None:
    swap = await models.Swap.filter(id=int(cancel_swap.parameter.__root__),contract_address=cancel_swap.data.target_address).get()
    swap.status = models.SwapStatus.CANCELED
    swap.level = cancel_swap.data.level  # type: ignore
    await swap.save()