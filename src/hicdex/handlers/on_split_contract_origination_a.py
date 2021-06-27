import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Origination
from hicdex.types.split_contract_a.storage import SplitContractAStorage


async def on_split_contract_origination_a(
    ctx: HandlerContext,
    split_contract_a_origination: Origination[SplitContractAStorage],
) -> None:
    if split_contract_a_origination.data.sender_address == 'KT1DfdhNm8NEy158dqnfg5cfCjsrMeB6jdHW':
        contract_address = split_contract_a_origination.data.originated_contract_address
        shares = split_contract_a_origination.storage.shares
        administrator = split_contract_a_origination.storage.administrator
        total_shares = split_contract_a_origination.storage.totalShares
        core_participants = split_contract_a_origination.storage.coreParticipants

        holder, _ = await models.Holder.get_or_create(address=contract_address)
        holder.is_split = True  # type: ignore
        await holder.save()
        contract, _ = await models.SplitContract.get_or_create(contract=holder, administrator=administrator, total_shares=total_shares)

        for address, share in shares.items():
            holder, _ = await models.Holder.get_or_create(address=address)
            holder_type = models.ShareholderStatus.benefactor
            if address in core_participants:
                holder_type = models.ShareholderStatus.core_participant
            await models.Shareholder.get_or_create(split_contract=contract, holder=holder, shares=int(share), holder_type=holder_type)
