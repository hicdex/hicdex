from typing import Optional

from dipdup.models import OperationData, Origination, Transaction
from dipdup.context import HandlerContext

import hicdex.models as models

from hicdex.types.hen_swap_v3.parameter.swap import SwapParameter
from hicdex.types.hen_swap_v3.storage import HenSwapV3Storage


async def on_swap_v3(
    ctx: HandlerContext,
    swap: Transaction[SwapParameter, HenSwapV3Storage],
) -> None:
    holder, _ = await models.Holder.get_or_create(address=swap.data.sender_address)
    token, _ = await models.Token.get_or_create(id=int(swap.parameter.objkt_id))
    swap_id = int(swap.storage.counter) - 1
    fa2, _ = await models.FA2.get_or_create(contract=swap.parameter.fa2)

    is_valid = swap.parameter.creator == token.creator_id and int(swap.parameter.royalties) == int(token.royalties)  # type: ignore

    swap_model = models.Swap(
        id=swap_id,  # type: ignore
        creator=holder,
        token=token,
        price=swap.parameter.xtz_per_objkt,
        amount=swap.parameter.objkt_amount,
        amount_left=swap.parameter.objkt_amount,
        status=models.SwapStatus.ACTIVE,
        opid=swap.data.id,
        ophash=swap.data.hash,
        level=swap.data.level,
        timestamp=swap.data.timestamp,
        royalties=swap.parameter.royalties,
        fa2=fa2,
        contract_address=swap.data.target_address,
        contract_version=3,
        is_valid=is_valid,
    )
    await swap_model.save()

    await fix_other_metadata()
    if not token.artifact_uri and not token.title:
        await fix_token_metadata(token)