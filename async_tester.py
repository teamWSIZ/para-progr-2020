import asyncio
from datetime import datetime

import aiohttp
import requests

from utils import ts

M = 5000

"""
Idea: odpalić `M` job-ów na event-loopie.

"""


class AsyncHttpPerfTestEngine:
    """
    Klasa przechowująca sesję ClientSession,
    i wykonująca asynchronicznie self.job()
    """
    session: aiohttp.ClientSession

    def __init__(self, conn=None):
        self.session = conn

    async def connect(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    async def disconnect(self):
        return await self.session.close()

    async def fetch_data(self, url):
        async with self.session.get(url) as response:
            if response.status == 500:
                return None
            return await response.json()

    async def job(self):
        """
        Właściwa funkcja zawierająca testowany kod/endpoint.
        """
        # url = 'http://localhost:2233/status'
        # url = 'http://localhost:2233/files/blocking'
        url = 'http://localhost:2233/files/async'
        res = await self.fetch_data(url)
        return len(res['data'])


async def main_task():
    engine = AsyncHttpPerfTestEngine()
    await engine.connect()
    tasks = [asyncio.create_task(engine.job()) for _ in range(M)]
    await asyncio.wait(tasks)
    suma = sum(tasks[i].result() for i in range(M))
    print(f'check 12.0={suma / M}')
    await engine.disconnect()


if __name__ == '__main__':
    start = ts()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_task())
    loop.close()
    print('------')
    delta = ts() - start
    print(f'{M} requests in {delta:.3f}s ({M / delta:.0f}RPS)')
