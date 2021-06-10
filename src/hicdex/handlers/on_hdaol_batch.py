from pprint import pprint
from typing import Optional

from dipdup.models import OperationData, OperationHandlerContext, OriginationContext, TransactionContext

import hicdex.models as models

from hicdex.types.hdao_ledger.parameter.h_dao_batch import HDAOBatchParameter
from hicdex.types.hdao_ledger.storage import HdaoLedgerStorage


async def on_hdaol_batch(
    ctx: OperationHandlerContext,
    h_dao_batch: TransactionContext[HDAOBatchParameter, HdaoLedgerStorage],
) -> None:
    for t in h_dao_batch.parameter.__root__:
        receiver, _ = await models.Holder.get_or_create(address=t.to_)
        receiver.hdao_balance += int(t.amount)  # type: ignore
        await receiver.save()
