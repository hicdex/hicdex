import json

import aiohttp

import hicdex.models as models
from dipdup.utils import http_request
from hicdex.utils import clean_null_bytes

METADATA_PATH = '/home/dipdup/metadata/tokens'


async def fix_token_metadata(token):
    metadata = await get_metadata(token)
    token.title = get_name(metadata)
    token.description = get_description(metadata)
    token.artifact_uri = get_artifact_uri(metadata)
    token.display_uri = get_display_uri(metadata)
    token.thumbnail_uri = get_thumbnail_uri(metadata)
    token.mime = get_mime(metadata)
    token.extra = metadata.get('extra', {})
    await add_tags(token, metadata)
    await token.save()
    return metadata != {}


async def fix_other_metadata():
    tokens = await models.Token.filter(artifact_uri='').all().order_by('id').limit(30)
    for token in tokens:
        fixed = await fix_token_metadata(token)
        if fixed:
            print(f'fixed metadata for {token.id}')
        else:
            print(f'failed to fix metadata for {token.id}')


async def add_tags(token, metadata):
    tags = [await get_or_create_tag(tag) for tag in get_tags(metadata)]
    for tag in tags:
        token_tag = await models.TokenTag(token=token, tag=tag)
        await token_tag.save()


async def get_or_create_tag(tag):
    tag, _ = await models.Tag.get_or_create(tag=tag)
    return tag


async def get_metadata(token):
    failed_attempt = 0
    try:
        with open(file_path(token.id)) as json_file:
            metadata = json.load(json_file)
            failed_attempt = metadata.get('__failed_attempt')
            if failed_attempt and failed_attempt > 10:
                return {}
            if not failed_attempt:
                return metadata
    except Exception:
        pass

    data = await fetch_metadata_cf_ipfs(token, failed_attempt)
    if data != {}:
        print(f'metadata for {token.id} from IPFS')
    else:
        data = await fetch_metadata_bcd(token, failed_attempt)
        if data != {}:
            print(f'metadata for {token.id} from BCD')

    return data


def normalize_metadata(token, metadata):
    n = {
        '__version': 1,
        'token_id': token.id,
        'symbol': metadata.get('symbol', 'OBJKT'),
        'name': get_name(metadata),
        'description': get_description(metadata),
        'artifact_uri': get_artifact_uri(metadata),
        'display_uri': get_display_uri(metadata),
        'thumbnail_uri': get_thumbnail_uri(metadata),
        'formats': get_formats(metadata),
        'creators': get_creators(metadata),
        # not cleaned / not lowercased, store as-is
        'tags': metadata.get('tags', []),
        'extra': {},
    }

    return n


def write_metadata_file(token, metadata):
    with open(file_path(token.id), 'w') as write_file:
        json.dump(normalize_metadata(token, metadata), write_file)


async def fetch_metadata_bcd(token, failed_attempt=0):
    session = aiohttp.ClientSession()
    data = await http_request(
        session,
        'get',
        url=f'https://api.better-call.dev/v1/tokens/mainnet/metadata?contract:KT1Hkg5qeNhfwpKW4fXvq7HGZB9z2EnmCCA9&token_id={token.id}',
    )

    data = [
        obj for obj in data if 'symbol' in obj and (obj['symbol'] == 'OBJKT' or obj['contract'] == 'KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton')
    ]
    try:
        if data and not isinstance(data[0], list):
            write_metadata_file(token, data[0])
            return data[0]
        with open(file_path(token.id), 'w') as write_file:
            json.dump({'__failed_attempt': failed_attempt + 1}, write_file)
    except FileNotFoundError:
        pass
    return {}


async def fetch_metadata_cf_ipfs(token, failed_attempt=0):
    addr = token.metadata.replace('ipfs://', '')

    try:
        data = await http_request(
            'get',
            url=f'https://cloudflare-ipfs.com/ipfs/{addr}',
        )
        if data and not isinstance(data, list):
            write_metadata_file(token, data)
            return data
        with open(file_path(token.id), 'w') as write_file:
            json.dump({'__failed_attempt': failed_attempt + 1}, write_file)
    except Exception:
        pass
    return {}


def get_mime(metadata):
    if ('formats' in metadata) and metadata['formats'] and ('mimeType' in metadata['formats'][0]):
        return metadata['formats'][0]['mimeType']
    return ''


def get_tags(metadata):
    tags = metadata.get('tags', [])
    cleaned = [clean_null_bytes(tag) for tag in tags]
    lowercased = [tag.lower() for tag in cleaned]
    uniqued = list(set(lowercased))
    return [tag for tag in uniqued if len(tag) < 255]


def get_name(metadata):
    return clean_null_bytes(metadata.get('name', ''))


def get_description(metadata):
    return clean_null_bytes(metadata.get('description', ''))


def get_artifact_uri(metadata):
    return clean_null_bytes(metadata.get('artifact_uri', '') or metadata.get('artifactUri', ''))


def get_display_uri(metadata):
    return clean_null_bytes(metadata.get('display_uri', '') or metadata.get('displayUri', ''))


def get_thumbnail_uri(metadata):
    return clean_null_bytes(metadata.get('thumbnail_uri', '') or metadata.get('thumbnailUri', ''))


def get_formats(metadata):
    return [clean_null_bytes(x) for x in metadata.get('formats', [])]


def get_creators(metadata):
    return [clean_null_bytes(x) for x in metadata.get('creators', [])]


def get_creator(metadata):
    return [clean_null_bytes(x) for x in metadata.get('creator', [])]


def file_path(token_id: str):
    token_id_int = int(token_id)
    lvl2 = token_id_int % 10
    lvl1 = int((token_id_int % 100 - lvl2) / 10)
    return f'{METADATA_PATH}/{lvl1}/{lvl2}/{token_id}.json'
