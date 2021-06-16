import hicdex.models as models
from dipdup.models import OperationHandlerContext, OriginationContext
from hicdex.types.split_contract_a.storage import SplitContractAStorage


async def on_split_contract_origination_a(
    ctx: OperationHandlerContext,
    split_originated_a_origination: OriginationContext[SplitContractAStorage],
) -> None:
    if split_originated_a_origination.data.sender_address == 'KT1UmgaFQgHrqEb4kPK4GoeHyu7YBfGu3rd4':
        contract_address = split_originated_a_origination.data.originated_contract_address
        shares = split_originated_a_origination.storage.shares
        administrator = split_originated_a_origination.storage.administrator
        total_shares = split_originated_a_origination.storage.totalShares

        holder, _ = await models.Holder.get_or_create(address=contract_address)
        holder.is_split = True  # type: ignore
        await holder.save()
        contract = await models.SplitContract.create(contract=holder, administrator=administrator, total_shares=total_shares)
        for address, share in shares.items():
            holder, _ = await models.Holder.get_or_create(address=address)
            await models.Shareholder.create(split_contract=contract, holder=holder, shares=int(share))
