from typing import List

import hicdex.models as models
from dipdup.models import BigMapAction, BigMapContext, BigMapHandlerContext
from hicdex.types.hen_objkts.big_map.operators_key import OperatorsKey
from hicdex.types.hen_objkts.big_map.operators_value import OperatorsValue


async def on_operator_update(
    ctx: BigMapHandlerContext,
    operators: List[BigMapContext[OperatorsKey, OperatorsValue]],
) -> None:
    operations = []
    for operation in operators:
        if not isinstance(operation, BigMapContext):
            continue

        if operation.action == BigMapAction.ADD:
            operations.append(operation)

        if operation.action == BigMapAction.REMOVE:
            if operations:
                last_operation = operations.pop()
                if (
                    last_operation.action != BigMapAction.ADD
                    or operation.key.operator != last_operation.key.operator
                    or operation.key.owner != last_operation.key.owner
                    or operation.key.token_id != last_operation.key.token_id
                ):
                    # this REMOVE action does not revert the last ADD
                    operations.append(last_operation)

            operations.append(operation)

    for operation in operations:
        token = await models.Token.filter(id=int(operation.key.token_id)).get()
        owner, _ = await models.Holder.get_or_create(address=operation.key.owner)
        operator = operation.key.operator

        if operation.action == BigMapAction.ADD:
            token_operator = await models.TokenOperator.create(token=token, owner=owner, operator=operator)

        if operation.action == BigMapAction.REMOVE:
            token_operator = await models.TokenOperator.filter(token=token, owner=owner, operator=operator).get()
            await token_operator.delete()
