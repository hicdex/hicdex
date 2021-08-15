import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.split_sign.parameter.sign import SignParameter
from hicdex.types.split_sign.storage import SplitSignStorage


async def on_split_sign(
    ctx: HandlerContext,
    sign: Transaction[SignParameter, SplitSignStorage],
) -> None:
    try:
        sender = sign.data.sender_address
        objkt_id = sign.parameter.__root__

        token = await models.Token.filter(id=int(objkt_id)).get()
        contract = await models.SplitContract.filter(contract_id=token.creator_id).get()  # type: ignore

        signature = models.Signatures(holder_id=sender, token_id=token.id)
        await signature.save()

        core_participants = await models.Shareholder.filter(
            split_contract=contract, holder_type=models.ShareholderStatus.core_participant
        ).all()
        sig_required = {shareholder.holder_id for shareholder in core_participants}  # type: ignore
        signers = await models.Signatures.filter(token=token).all()
        sig_created = {signer.holder_id for signer in signers}  # type: ignore

        if sig_required.issubset(sig_created):
            token.is_signed = True  # type: ignore
            await token.save()
    except:
        return
