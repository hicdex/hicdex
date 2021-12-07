import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.hen_swap_v2.parameter.cancel_swap import CancelSwapParameter
from hicdex.types.hen_swap_v2.storage import HenSwapV2Storage


async def on_cancel_swap_v2(
    ctx: HandlerContext,
    cancel_swap: Transaction[CancelSwapParameter, HenSwapV2Storage],
) -> None:
    swap = await models.Swap.filter(id=int(cancel_swap.parameter.__root__),contract_address=cancel_swap.data.target_address).get()
    swap.status = models.SwapStatus.CANCELED
    swap.level = cancel_swap.data.level  # type: ignore
    await swap.save()
