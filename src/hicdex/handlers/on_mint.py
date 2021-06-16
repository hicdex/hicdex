import hicdex.models as models
from dipdup.models import OperationHandlerContext, Transaction
from hicdex.metadata_utils import fix_token_metadata
from hicdex.types.hen_minter.parameter.mint_objkt import MintOBJKTParameter
from hicdex.types.hen_minter.storage import HenMinterStorage
from hicdex.types.hen_objkts.parameter.mint import MintParameter
from hicdex.types.hen_objkts.storage import HenObjktsStorage
from hicdex.utils import fromhex


async def on_mint(
    ctx: OperationHandlerContext,
    mint_objkt: Transaction[MintOBJKTParameter, HenMinterStorage],
    mint: Transaction[MintParameter, HenObjktsStorage],
) -> None:
    holder, _ = await models.Holder.get_or_create(address=mint.parameter.address)

    creator = holder
    if mint.parameter.address != mint_objkt.data.sender_address:
        creator, _ = await models.Holder.get_or_create(address=mint_objkt.data.sender_address)

    if await models.Token.exists(id=mint.parameter.token_id):
        return

    metadata = ''
    if mint_objkt.parameter.metadata:
        metadata = fromhex(mint_objkt.parameter.metadata)

    token = models.Token(
        id=mint.parameter.token_id,
        royalties=mint_objkt.parameter.royalties,
        title='',
        description='',
        artifact_uri='',
        display_uri='',
        thumbnail_uri='',
        metadata=metadata,
        mime='',
        creator=creator,
        supply=mint.parameter.amount,
        level=mint.data.level,
        timestamp=mint.data.timestamp,
    )
    await token.save()

    seller_holding, _ = await models.TokenHolder.get_or_create(token=token, holder=holder, quantity=int(mint.parameter.amount))
    await seller_holding.save()

    await fix_token_metadata(token)
