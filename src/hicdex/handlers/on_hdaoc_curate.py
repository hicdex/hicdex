from pprint import pprint
from typing import Optional

import hicdex.models as models
from hicdex.types.hdao_curation.parameter.curate import CurateParameter
from hicdex.types.hdao_curation.storage import HdaoCurationStorage
from dipdup.context import OperationHandlerContext
from dipdup.models import Transaction,


async def on_hdaoc_curate(
    ctx: OperationHandlerContext,
    curate: Transaction[CurateParameter, HdaoCurationStorage],
) -> None:
    token = await models.Token.filter(id=int(curate.parameter.objkt_id)).get()
    token.hdao_balance += int(curate.parameter.hDAO_amount)  # type: ignore
    await token.save()
