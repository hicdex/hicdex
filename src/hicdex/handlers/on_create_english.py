import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.objktbid_english.parameter.create_auction import CreateAuctionParameter
from hicdex.types.objktbid_english.storage import ObjktbidEnglishStorage


async def on_create_english(
    ctx: HandlerContext,
    create_auction: Transaction[CreateAuctionParameter, ObjktbidEnglishStorage],
) -> None:
    fa2, _ = await models.FA2Token.get_or_create(address=create_auction.parameter.fa2)
    creator, _ = await models.Holder.get_or_create(address=create_auction.data.sender_address)
    artist, _ = await models.Holder.get_or_create(address=create_auction.parameter.artist)

    auction_model = models.EnglishAuction(
        id=int(create_auction.storage.auction_id) - 1,  # type: ignore
        fa2=fa2,
        status=models.AuctionStatus.ACTIVE,
        objkt_id=create_auction.parameter.objkt_id,
        creator=creator,
        artist=artist,
        royalties=create_auction.parameter.royalties,
        start_time=create_auction.parameter.start_time,
        end_time=create_auction.parameter.end_time,
        price_increment=create_auction.parameter.price_increment,
        extension_time=create_auction.parameter.extension_time,
        reserve=create_auction.parameter.reserve,
        timestamp=create_auction.data.timestamp,
        level=create_auction.data.level,
    )
    await auction_model.save()

    bid = models.EnglishBid(
        bidder=creator,
        amount=0,
        auction=auction_model,
        timestamp=create_auction.data.timestamp,
        level=create_auction.data.level,
    )
    await bid.save()
