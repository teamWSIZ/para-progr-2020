import asyncio

import aiohttp
from concurrent.futures.thread import ThreadPoolExecutor
import threading
from datetime import datetime

import requests


# from etap5_aiohttp.utils import ts
def ts():
    return datetime.now().timestamp()


M = 50000

"""
Idea: odpalić `M` job-ów na event-loopie.

"""


def job():
    # print(f'job on thread {threading.current_thread().name}')
    r = requests.get('http://localhost:9081/')
    # r = requests.get('http://localhost:2233/status')
    return len(r.json()['comment'])


class Engine:
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

    async def job(self) -> int:
        url = 'http://localhost:2233/status'
        res = await self.fetch_data(url)
        return len(res['comment'])


async def main_task():
    engine = Engine()
    await engine.connect()
    tasks = [asyncio.create_task(engine.job()) for _ in range(M)]
    await asyncio.wait(tasks)
    suma = sum(tasks[i].result() for i in range(M))
    print(f'check 12={suma / M}')
    await engine.disconnect()


if __name__ == '__main__':
    start = ts()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_task())
    print('------')
    loop.close()
    delta = ts() - start
    print(f'{M} requests in {delta:.3f}s ({M / delta:.0f}RPS)')
