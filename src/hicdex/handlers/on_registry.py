import logging

import aiohttp

import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from dipdup.utils import http_request
from hicdex.types.hen_subjkt.parameter.registry import RegistryParameter
from hicdex.types.hen_subjkt.storage import HenSubjktStorage
from hicdex.utils import fromhex

_logger = logging.getLogger(__name__)


async def on_registry(
    ctx: HandlerContext,
    registry: Transaction[RegistryParameter, HenSubjktStorage],
) -> None:
    addr = registry.data.sender_address
    holder, _ = await models.Holder.get_or_create(address=addr)

    name = fromhex(registry.parameter.subjkt)
    metadata_file = fromhex(registry.parameter.metadata)
    metadata = {}

    if metadata_file.startswith('ipfs://'):
        _logger.info("Fetching IPFS metadata")
        try:
            session = aiohttp.ClientSession()
            addr = metadata_file.replace('ipfs://', '')
            metadata = await http_request(
                session,
                'get',
                url=f'https://cloudflare-ipfs.com/ipfs/{addr}',
            )
        except Exception as e:
            _logger.error(f"Failed to fetch IPFS metadata: {e}")
            pass

    holder.name = name  # type: ignore
    holder.metadata_file = metadata_file  # type: ignore
    holder.metadata = metadata  # type: ignore
    await holder.save()
