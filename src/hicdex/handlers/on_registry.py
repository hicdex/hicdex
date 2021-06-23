import logging
from typing import Dict

import hicdex.models as models
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from hicdex.metadata_utils import get_subjkt_metadata
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
    metadata: Dict[str, str] = {}

    holder.name = name  # type: ignore
    holder.metadata_file = metadata_file  # type: ignore
    holder.metadata = metadata  # type: ignore

    try:
        if metadata_file.startswith('ipfs://'):
            _logger.info("Fetching IPFS metadata")
            holder.metadata = await get_subjkt_metadata(holder)
    except:
        pass

    await holder.save()
