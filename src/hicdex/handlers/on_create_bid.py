import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.objktbid_marketplace.parameter.bid import BidParameter
from hicdex.types.objktbid_marketplace.storage import ObjktbidMarketplaceStorage


async def on_create_bid(
    ctx: HandlerContext,
    bid: Transaction[BidParameter, ObjktbidMarketplaceStorage],
) -> None:
    fa2, _ = await models.FA2.get_or_create(contract=bid.parameter.fa2)
    creator, _ = await models.Holder.get_or_create(address=bid.data.sender_address)

    artist = creator
    if bid.parameter.artist != bid.data.sender_address:
        artist, _ = await models.Holder.get_or_create(address=bid.parameter.artist)

    bid_model = models.Bid(
        id=int(bid.storage.bid_id) - 1,  # type: ignore
        creator=creator,
        objkt_id=bid.parameter.objkt_id,
        fa2=fa2,
        price=bid.data.amount,
        status=models.AuctionStatus.ACTIVE,
        level=bid.data.level,
        timestamp=bid.data.timestamp,
        artist=artist,
        royalties=bid.parameter.royalties,
    )
    await bid_model.save()
