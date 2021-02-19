import unittest
from asyncio import sleep
from random import randint

"""
Przykład testów jednostkowych kodu asynchronicznego: 
W przykładzie pokazujemy jak utworzyć obiekt współdzielony między wieloma testami.
"""


class Engine:
    async def wait_a_second(self):
        await sleep(1)


class FakeDbConnection:
    id: int

    async def connect(self):
        self.id = randint(1, 100)
        await sleep(1)
        print(f'connected; id={self.id}')


state = dict()
state['connection'] = None


def c() -> FakeDbConnection:
    return state['connection']


class Test(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        if state['connection'] is None:
            state['connection'] = FakeDbConnection()
            await c().connect()

    async def asyncTearDown(self):
        pass

    async def test_waiting(self):
        print(f'zaczynamy czekanie; btw -- connection: {c().id}')
        await Engine().wait_a_second()
        print('koniec czekania')

    async def test_waiting2(self):
        print(f'zaczynamy czekanie; btw -- connection: {c().id}')
        await Engine().wait_a_second()
        print('koniec czekania')


if __name__ == "__main__":
    unittest.main()
