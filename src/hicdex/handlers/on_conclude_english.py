import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.objktbid_english.parameter.conclude_auction import ConcludeAuctionParameter
from hicdex.types.objktbid_english.storage import ObjktbidEnglishStorage


async def on_conclude_english(
    ctx: HandlerContext,
    conclude_auction: Transaction[ConcludeAuctionParameter, ObjktbidEnglishStorage],
) -> None:
    auction_model = await models.EnglishAuction.filter(id=int(conclude_auction.parameter.__root__)).get()
    auction_model.status = models.AuctionStatus.CONCLUDED

    auction_model.update_level = conclude_auction.data.level  # type: ignore
    auction_model.update_timestamp = conclude_auction.data.timestamp  # type: ignore

    await auction_model.save()
