import hicdex.models as models
from dipdup.models import OperationHandlerContext, TransactionContext
from hicdex.types.fa2_token.storage import Fa2TokenStorage
from hicdex.types.hen_objkts.parameter.transfer import TransferParameter


async def on_transfer(
    ctx: OperationHandlerContext,
    transfer: TransactionContext[TransferParameter, Fa2TokenStorage],
) -> None:
    for t in transfer.parameter.__root__:
        sender, _ = await models.Holder.get_or_create(address=t.from_)
        for tx in t.txs:
            receiver, _ = await models.Holder.get_or_create(address=tx.to_)
            token = await models.Token.filter(id=int(tx.token_id)).get()

            sender_holding, _ = await models.TokenHolder.get_or_create(token=token, holder=sender)
            sender_holding.quantity -= int(tx.amount)  # type: ignore
            await sender_holding.save()
            receiver_holding, _ = await models.TokenHolder.get_or_create(token=token, holder=receiver)
            receiver_holding.quantity += int(tx.amount)  # type: ignore
            await receiver_holding.save()

            if tx.to_ == 'tz1burnburnburnburnburnburnburjAYjjX':
                token.supply -= int(tx.amount)
                await token.save()
