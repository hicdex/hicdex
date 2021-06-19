import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.hdao_ledger.parameter.transfer import TransferParameter
from hicdex.types.hdao_ledger.storage import HdaoLedgerStorage


async def on_hdaol_transfer(
    ctx: HandlerContext,
    transfer: Transaction[TransferParameter, HdaoLedgerStorage],
) -> None:
    for t in transfer.parameter.__root__:
        sender, _ = await models.Holder.get_or_create(address=t.from_)
        for tx in t.txs:
            receiver, _ = await models.Holder.get_or_create(address=tx.to_)
            sender.hdao_balance -= int(tx.amount)  # type: ignore
            receiver.hdao_balance += int(tx.amount)  # type: ignore
            await receiver.save()
        await sender.save()
