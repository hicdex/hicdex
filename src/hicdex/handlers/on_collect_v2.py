import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.hen_swap_v2.parameter.collect import CollectParameter
from hicdex.types.hen_swap_v2.storage import HenSwapV2Storage


async def on_collect_v2(
    ctx: HandlerContext,
    collect: Transaction[CollectParameter, HenSwapV2Storage],
) -> None:
    swap = await models.Swap.filter(id=int(collect.parameter.__root__)).get()
    seller = await swap.creator
    buyer, _ = await models.Holder.get_or_create(address=collect.data.sender_address)
    token = await swap.token.get()  # type: ignore

    trade = models.Trade(
        swap=swap,
        seller=seller,
        buyer=buyer,
        token=token,
        amount=1,
        level=collect.data.level,
        timestamp=collect.data.timestamp,
    )
    await trade.save()

    swap.amount_left -= 1  # type: ignore
    if swap.amount_left == 0:
        swap.status = models.SwapStatus.FINISHED
    await swap.save()
