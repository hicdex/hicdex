import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.metadata_utils import fix_other_metadata, fix_token_metadata
from hicdex.types.hen_swap_v2.parameter.swap import SwapParameter
from hicdex.types.hen_swap_v2.storage import HenSwapV2Storage


async def on_swap_v2(
    ctx: HandlerContext,
    swap: Transaction[SwapParameter, HenSwapV2Storage],
) -> None:
    holder, _ = await models.Holder.get_or_create(address=swap.data.sender_address)
    token = await models.Token.filter(id=int(swap.parameter.objkt_id)).get()
    swap_id = int(swap.storage.counter) - 1
    swap_model = models.Swap(
        id=swap_id,  # type: ignore
        creator=holder,
        token=token,
        price=swap.parameter.xtz_per_objkt,
        amount=swap.parameter.objkt_amount,
        amount_left=swap.parameter.objkt_amount,
        status=models.SwapStatus.ACTIVE,
        level=swap.data.level,
        timestamp=swap.data.timestamp,
        royalties=swap.parameter.royalties,
        contract_version=2,
    )
    await swap_model.save()

    await fix_other_metadata()
    if not token.artifact_uri and not token.title:
        await fix_token_metadata(token)
