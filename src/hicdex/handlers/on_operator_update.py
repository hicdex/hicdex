import logging

from tortoise.exceptions import DoesNotExist

import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import BigMapAction, BigMapDiff
from hicdex.types.hen_objkts.big_map.operators_key import OperatorsKey
from hicdex.types.hen_objkts.big_map.operators_value import OperatorsValue

_logger = logging.getLogger(__name__)


async def on_operator_update(
    ctx: HandlerContext,
    operation: BigMapDiff[OperatorsKey, OperatorsValue],
) -> None:
    try:
        token = await models.Token.filter(id=int(operation.key.token_id)).get()
    except DoesNotExist:
        _logger.info(f'token {operation.key.token_id} does not exist for operator update')
        return
    owner, _ = await models.Holder.get_or_create(address=operation.key.owner)
    operator = operation.key.operator

    if operation.action == BigMapAction.ADD:
        token_operator = await models.TokenOperator.create(token=token, owner=owner, operator=operator)

    if operation.action == BigMapAction.REMOVE:
        try:
            token_operator = await models.TokenOperator.filter(token=token, owner=owner, operator=operator).get()
            await token_operator.delete()
        except:
            _logger.info(f'failed to remove {token.id} {owner.address} {operator}')
