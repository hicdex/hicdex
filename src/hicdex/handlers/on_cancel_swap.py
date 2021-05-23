import hicdex.models as models
from hicdex.types.hen_minter.parameter.cancel_swap import CancelSwapParameter
from hicdex.types.hen_minter.storage import HenMinterStorage
from dipdup.models import OperationHandlerContext, TransactionContext


async def on_cancel_swap(
    ctx: OperationHandlerContext,
    cancel_swap: TransactionContext[CancelSwapParameter, HenMinterStorage],
) -> None:
    swap = await models.Swap.filter(id=int(cancel_swap.parameter.__root__)).get()
    swap.status = models.SwapStatus.CANCELED
    await swap.save()
