import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.metadata_utils import fix_other_metadata, fix_token_metadata
from hicdex.types.hen_minter.parameter.swap import SwapParameter
from hicdex.types.hen_minter.storage import HenMinterStorage


async def on_swap(
    ctx: HandlerContext,
    swap: Transaction[SwapParameter, HenMinterStorage],
) -> None:
    holder, _ = await models.Holder.get_or_create(address=swap.data.sender_address)
    token = await models.Token.filter(id=int(swap.parameter.objkt_id)).get()
    swap_model = models.Swap(
        id=int(swap.storage.swap_id) - 1,  # type: ignore
        creator=holder,
        token=token,
        price=swap.parameter.xtz_per_objkt,
        amount=swap.parameter.objkt_amount,
        amount_left=swap.parameter.objkt_amount,
        status=models.SwapStatus.ACTIVE,
        level=swap.data.level,
        timestamp=swap.data.timestamp,
    )
    await swap_model.save()

    if not token.artifact_uri and not token.title:
        await fix_token_metadata(token)
        await fix_other_metadata()
