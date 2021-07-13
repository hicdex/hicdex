from hashids import Hashids

import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.objktbid_english.parameter.create_auction import CreateAuctionParameter
from hicdex.types.objktbid_english.storage import ObjktbidEnglishStorage

hashids = Hashids(salt='objkt.bid!', min_length=8)

CONTRACT_VERSION = {
    'KT1Wvk8fon9SgNEPQKewoSL2ziGGuCQebqZc': 1,
    'KT1XjcRq5MLAzMKQ3UHsrue2SeU2NbxUrzmU': 2,
}


async def on_create_english(
    ctx: HandlerContext,
    create_auction: Transaction[CreateAuctionParameter, ObjktbidEnglishStorage],
) -> None:
    auction_id = int(create_auction.storage.auction_id) - 1
    version = CONTRACT_VERSION.get(create_auction.data.target_address, -1)  # type: ignore
    fa2, _ = await models.FA2.get_or_create(contract=create_auction.parameter.fa2)
    creator, _ = await models.Holder.get_or_create(address=create_auction.data.sender_address)

    artist = creator
    if create_auction.data.sender_address != create_auction.parameter.artist:
        artist, _ = await models.Holder.get_or_create(address=create_auction.parameter.artist)

    auction_model = models.EnglishAuction(
        id=auction_id,  # type: ignore
        hash=hashids.encode(auction_id),
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
        contract_version=version,
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
