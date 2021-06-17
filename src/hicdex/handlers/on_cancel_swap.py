import hicdex.models as models
from hicdex.types.hen_minter.parameter.cancel_swap import CancelSwapParameter
from hicdex.types.hen_minter.storage import HenMinterStorage
from dipdup.context import HandlerContext
from dipdup.models import Transaction


async def on_cancel_swap(
    ctx: HandlerContext,
    cancel_swap: Transaction[CancelSwapParameter, HenMinterStorage],
) -> None:
    swap = await models.Swap.filter(id=int(cancel_swap.parameter.__root__)).get()
    swap.status = models.SwapStatus.CANCELED
    await swap.save()
