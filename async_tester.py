import aiohttp
import asyncio

from utils import ts

REQUEST_COUNT = 2000
BATCH_SIZE = 100
BATCH_NUMBER = REQUEST_COUNT // BATCH_SIZE

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
        # url = 'http://localhost:2233/files/async'
        url = 'http://localhost:2233/db/basic'
        # url = 'http://localhost:2233/db/write'
        res = await self.fetch_data(url)
        return len(res['data'])


async def main_task():
    engine = AsyncHttpPerfTestEngine()
    await engine.connect()
    suma = 0
    for i in range(BATCH_NUMBER):
        tasks = [asyncio.create_task(engine.job()) for _ in range(BATCH_SIZE)]
        await asyncio.wait(tasks)
        suma += sum(tasks[i].result() for i in range(BATCH_SIZE))
    print(f'check 12.0={suma / REQUEST_COUNT}')
    await engine.disconnect()


if __name__ == '__main__':
    start = ts()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_task())
    loop.close()
    print('------')
    delta = ts() - start
    print(f'{REQUEST_COUNT} requests in {delta:.3f}s ({REQUEST_COUNT / delta:.0f}RPS)')
