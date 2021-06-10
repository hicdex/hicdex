from pprint import pprint
from typing import Optional

from dipdup.models import OperationData, OperationHandlerContext, OriginationContext, TransactionContext

import hicdex.models as models

from hicdex.types.hdao_curation.parameter.curate import CurateParameter
from hicdex.types.hdao_curation.storage import HdaoCurationStorage


async def on_hdaoc_curate(
    ctx: OperationHandlerContext,
    curate: TransactionContext[CurateParameter, HdaoCurationStorage],
) -> None:
    token = await models.Token.filter(id=int(curate.parameter.objkt_id)).get()
    token.hdao_balance += int(curate.parameter.hDAO_amount)  # type: ignore
    await token.save()
