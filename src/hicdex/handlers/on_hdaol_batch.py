import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.hdao_ledger.parameter.h_dao_batch import HDAOBatchParameter
from hicdex.types.hdao_ledger.storage import HdaoLedgerStorage


async def on_hdaol_batch(
    ctx: HandlerContext,
    h_dao_batch: Transaction[HDAOBatchParameter, HdaoLedgerStorage],
) -> None:
    for t in h_dao_batch.parameter.__root__:
        receiver, _ = await models.Holder.get_or_create(address=t.to_)
        receiver.hdao_balance += int(t.amount)  # type: ignore
        await receiver.save()
