import subprocess
from contextlib import suppress
from os import mkdir
from os.path import dirname, join
from shutil import rmtree
from unittest import IsolatedAsyncioTestCase

from tortoise.transactions import in_transaction

import hicdex.models
from dipdup.utils import tortoise_wrapper


class DemosTest(IsolatedAsyncioTestCase):
    # TODO: store cache in xdg_cache_home, keep databases and logs after last run
    def setUp(self):
        with suppress(FileNotFoundError):
            rmtree('/tmp/dipdup')
        mkdir('/tmp/dipdup')

    def run_dipdup(self, config: str):
        subprocess.run(
            [
                'dipdup',
                '-l',
                'warning.yml',
                '-c',
                join(dirname(__file__), config),
                'run',
                '--oneshot',
            ],
            cwd='/tmp/dipdup',
            check=True,
        )

    async def test_hicdex(self):
        self.run_dipdup('hicdex.yml')

        async with tortoise_wrapper('sqlite:///tmp/dipdup/db.sqlite3', 'hicdex.models'):
            holders = await hicdex.models.Holder.filter().count()
            tokens = await hicdex.models.Token.filter().count()
            swaps = await hicdex.models.Swap.filter().count()
            trades = await hicdex.models.Trade.filter().count()

            self.assertEqual(22, holders)
            self.assertEqual(29, tokens)
            self.assertEqual(20, swaps)
            self.assertEqual(24, trades)
