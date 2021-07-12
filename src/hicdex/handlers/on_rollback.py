import os

import requests

from dipdup.context import RollbackHandlerContext


def send(levels_diff):
    api_key = os.environ.get('MAILGUN_API_KEY')
    if not api_key:
        return
    to_emails = os.environ.get('NOTIFIED_EMAILS').split(',')

    return requests.post(
        "https://api.eu.mailgun.net/v3/mail.hicdex.com/messages",
        auth=("api", api_key),
        data={
            "from": "Hicdex API <mailgun@mail.hicdex.com>",
            "to": to_emails,
            "subject": "Rollback hicdex 3",
            "text": f"Chain reorg: {levels_diff} blocks, please reindex!",
        },
    )


async def on_rollback(ctx: RollbackHandlerContext) -> None:
    ctx.logger.warning('Datasource rolled back from level %s to level %s, reindexing', ctx.from_level, ctx.to_level)
    # await ctx.reindex()
    levels_diff = ctx.from_level - ctx.to_level
    send(levels_diff)
