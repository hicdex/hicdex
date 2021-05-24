import hicdex.models as models
from hicdex.types.hen_minter.parameter.mint_objkt import MintOBJKTParameter
from hicdex.types.hen_minter.storage import HenMinterStorage
from hicdex.types.hen_objkts.parameter.mint import MintParameter
from hicdex.types.hen_objkts.storage import HenObjktsStorage
from dipdup.models import OperationHandlerContext, TransactionContext


async def on_mint(
    ctx: OperationHandlerContext,
    mint_objkt: TransactionContext[MintOBJKTParameter, HenMinterStorage],
    mint: TransactionContext[MintParameter, HenObjktsStorage],
) -> None:
    holder, _ = await models.Holder.get_or_create(address=mint.parameter.address)

    token = models.Token(
        id=mint.parameter.token_id,
        royalties=mint_objkt.parameter.royalties,
        title='',
        description='',
        artifact_uri='',
        thumbnail_uri='',
        mime='',
        creator=holder,
        supply=mint.parameter.amount,
        level=mint.data.level,
        timestamp=mint.data.timestamp,
    )
    await token.save()

    # seller_holding, _ = await models.TokenHolder.get_or_create(token=token, holder=holder, quantity=int(mint.parameter.amount))
    # await seller_holding.save()
