import json

import hicdex.models as models
from dipdup.utils import http_request

METADATA_PATH = '/home/dipdup/metadata/tokens'


async def fix_token_metadata(token):
    metadata = await get_metadata(str(token.id))
    token.title = get_title(metadata)
    token.description = get_description(metadata)
    token.artifact_uri = get_artifact_uri(metadata)
    token.display_uri = get_display_uri(metadata)
    token.thumbnail_uri = get_thumbnail_uri(metadata)
    token.mime = get_mime(metadata)
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


async def get_metadata(token_id: str):
    failed_attempt = 0
    try:
        with open(file_path(token_id)) as json_file:
            metadata = json.load(json_file)
            failed_attempt = metadata.get('__failed_attempt')
            if failed_attempt and failed_attempt > 10:
                return {}
            if not failed_attempt:
                return metadata
    except FileNotFoundError:
        pass
    data = await fetch_metadata(token_id, failed_attempt)
    return data


async def fetch_metadata(token_id, failed_attempt=0):
    data = await http_request(
        'get',
        url=f'https://api.better-call.dev/v1/tokens/mainnet/metadata?contract:KT1Hkg5qeNhfwpKW4fXvq7HGZB9z2EnmCCA9&token_id={token_id}',
    )

    data = [
        obj for obj in data if 'symbol' in obj and (obj['symbol'] == 'OBJKT' or obj['contract'] == 'KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton')
    ]
    try:
        if data and not isinstance(data[0], list):
            with open(file_path(token_id), 'w') as write_file:
                json.dump(data[0], write_file)
            return data[0]
        else:
            with open(file_path(token_id), 'w') as write_file:
                json.dump({'__failed_attempt': failed_attempt + 1}, write_file)
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
    return clean(metadata.get('name', ''))


def get_description(metadata):
    return clean(metadata.get('description', ''))


def get_artifact_uri(metadata):
    return metadata.get('artifact_uri', '')


def get_display_uri(metadata):
    return metadata.get('display_uri', '')


def get_thumbnail_uri(metadata):
    return metadata.get('thumbnail_uri', '')


def clean(string):
    return ''.join(string.split('\x00'))


def file_path(token_id: str):
    subfolder = int(token_id) % 10
    return f'{METADATA_PATH}/{subfolder}/{token_id}.json'
