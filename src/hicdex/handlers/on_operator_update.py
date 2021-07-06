import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.hen_objkts.parameter.update_operators import (
    UpdateOperatorsParameter,
    UpdateOperatorsParameterItem,
    UpdateOperatorsParameterItem1,
)
from hicdex.types.hen_objkts.storage import HenObjktsStorage

# from pprint import pformat
# ctx.logger.warning(pformat(op.remove_operator))


async def on_operator_update(
    ctx: HandlerContext,
    update_operators: Transaction[UpdateOperatorsParameter, HenObjktsStorage],
) -> None:
    for op in update_operators.parameter.__root__:
        try:
            if isinstance(op, UpdateOperatorsParameterItem):
                data_add = op.add_operator
                token, _ = await models.Token.get_or_create(id=int(data_add.token_id))
                owner, _ = await models.Holder.get_or_create(address=data_add.owner)
                operator = data_add.operator
                token_operator = await models.TokenOperator.create(
                    token=token, owner=owner, operator=operator, level=update_operators.data.level
                )
            if isinstance(op, UpdateOperatorsParameterItem1):
                data_remove = op.remove_operator
                token, _ = await models.Token.get_or_create(id=int(data_remove.token_id))
                owner, _ = await models.Holder.get_or_create(address=data_remove.owner)
                operator = data_remove.operator
                token_operator = await models.TokenOperator.filter(token=token, owner=owner, operator=operator).get()
                await token_operator.delete()
        except:
            pass
