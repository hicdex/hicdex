import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.types.objktbid_dutch.parameter.create_auction import CreateAuctionParameter
from hicdex.types.objktbid_dutch.storage import ObjktbidDutchStorage

CONTRACT_VERSION = {
    'KT1ET45vnyEFMLS9wX1dYHEs9aCN3twDEiQw': 1,
    'KT1W8PqJsZcpcAgDQH9SKQSZKvjVbpjUk8Sc': 2,
    'KT1QJ71jypKGgyTNtXjkCAYJZNhCKWiHuT2r': 3,
}


async def on_create_dutch(
    ctx: HandlerContext,
    create_auction: Transaction[CreateAuctionParameter, ObjktbidDutchStorage],
) -> None:
    version = CONTRACT_VERSION.get(create_auction.data.target_address, -1)  # type: ignore
    fa2, _ = await models.FA2.get_or_create(contract=create_auction.parameter.fa2)
    creator, _ = await models.Holder.get_or_create(address=create_auction.data.sender_address)
    artist = creator
    if create_auction.data.sender_address != create_auction.parameter.artist:
        artist, _ = await models.Holder.get_or_create(address=create_auction.parameter.artist)

    auction_model = models.DutchAuction(
        id=int(create_auction.storage.auction_id) - 1,  # type: ignore
        fa2=fa2,
        status=models.AuctionStatus.ACTIVE,
        objkt_id=create_auction.parameter.objkt_id,
        creator=creator,
        artist=artist,
        royalties=create_auction.parameter.royalties,
        start_time=create_auction.parameter.start_time,
        end_time=create_auction.parameter.end_time,
        start_price=create_auction.parameter.start_price,
        end_price=create_auction.parameter.end_price,
        contract_version=version,
        timestamp=create_auction.data.timestamp,
        level=create_auction.data.level,
    )
    await auction_model.save()
