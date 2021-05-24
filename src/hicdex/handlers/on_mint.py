import json

import hicdex.models as models
from hicdex.types.hen_minter.parameter.mint_objkt import MintOBJKTParameter
from hicdex.types.hen_minter.storage import HenMinterStorage
from hicdex.types.hen_objkts.parameter.mint import MintParameter
from hicdex.types.hen_objkts.storage import HenObjktsStorage
from dipdup.models import OperationHandlerContext, TransactionContext
from dipdup.utils import http_request

METADATA_PATH = '/home/dipdup/metadata/tokens'


async def on_mint(
    ctx: OperationHandlerContext,
    mint_objkt: TransactionContext[MintOBJKTParameter, HenMinterStorage],
    mint: TransactionContext[MintParameter, HenObjktsStorage],
) -> None:
    holder, _ = await models.Holder.get_or_create(address=mint.parameter.address)
    metadata = await get_metadata(mint.parameter.token_id)

    token = models.Token(
        id=mint.parameter.token_id,
        royalties=mint_objkt.parameter.royalties,
        title=clean(get_title(metadata)),
        description=clean(get_description(metadata)),
        artifact_uri=get_artifact_uri(metadata),
        thumbnail_uri=get_thumbnail_uri(metadata),
        mime=get_mime(metadata),
        creator=holder,
        supply=mint.parameter.amount,
        level=mint.data.level,
        timestamp=mint.data.timestamp,
    )
    await token.save()

    # seller_holding, _ = await models.TokenHolder.get_or_create(token=token, holder=holder, quantity=int(mint.parameter.amount))
    # await seller_holding.save()

    await add_tags(token, metadata)
    await fix_metadata()


async def fix_metadata():
    tokens = await models.Token.filter(artifact_uri='').all()
    for token in tokens:
        metadata = await get_metadata(str(token.id))
        token.title = clean(get_title(metadata))
        token.description = clean(get_description(metadata))
        token.artifact_uri = get_artifact_uri(metadata)
        token.thumbnail_uri = get_thumbnail_uri(metadata)
        token.mime = get_mime(metadata)
        await token.save()


async def add_tags(token, metadata):
    tags = [await get_or_create_tag(tag) for tag in get_tags(metadata)]
    for tag in tags:
        token_tag = await models.TokenTag(token=token, tag=tag)
        await token_tag.save()


async def get_or_create_tag(tag):
    tag, _ = await models.Tag.get_or_create(tag=tag)
    return tag


async def get_metadata(token_id: str):
    try:
        with open(f'{METADATA_PATH}/{token_id}.json') as json_file:
            print("FOUND")
            return json.load(json_file)
    except FileNotFoundError:
        data = await fetch_metadata(token_id)
        return data


async def fetch_metadata(token_id):
    data = await http_request(
        'get',
        url=f'https://api.better-call.dev/v1/tokens/mainnet/metadata?contract:KT1Hkg5qeNhfwpKW4fXvq7HGZB9z2EnmCCA9&token_id={token_id}',
    )

    data = [
        obj for obj in data if 'symbol' in obj and (obj['symbol'] == 'OBJKT' or obj['contract'] == 'KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton')
    ]
    try:
        if data and not isinstance(data[0], list):
            with open(f'{METADATA_PATH}/{token_id}.json', 'w') as write_file:
                json.dump(data[0], write_file)
            return data[0]
        with open(f'{METADATA_PATH}/{token_id}.json', 'w') as write_file:
            json.dump({}, write_file)
    except FileNotFoundError:
        pass
    return {}


def get_mime(metadata):
    if ('formats' in metadata) and metadata['formats'] and ('mimeType' in metadata['formats'][0]):
        return metadata['formats'][0]['mimeType']
    return ''


def get_tags(metadata):
    unique_tags = list(set(metadata.get('tags', [])))
    return [clean(tag) for tag in unique_tags if len(tag) < 255]


def get_title(metadata):
    return metadata.get('name', '')


def get_description(metadata):
    return metadata.get('description', '')


def get_artifact_uri(metadata):
    return metadata.get('artifact_uri', '')


def get_thumbnail_uri(metadata):
    return metadata.get('thumbnail_uri', '')


def clean(str):
    return ''.join(str.split('\x00'))
