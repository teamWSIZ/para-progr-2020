import asyncio

import asyncpg
from faker import Faker
from typing import List

DB_HOST = '10.10.0.33'
DB_PORT = '5432'
DB_DB = 'student'
DB_USER = 'student'
DB_PASS = 'wsiz#1234'


def dicts(rows):
    return [dict(r) for r in rows]


class DB:
    pool: asyncpg.pool.Pool  # connection pool
    faker: Faker  # do generowania losowych danych

    async def init(self):
        print(f'creating pool for db:{DB_HOST}:{DB_PORT}, db={DB_DB}')

        self.pool = await asyncpg.create_pool(host=DB_HOST, port=DB_PORT,
                                              user=DB_USER, database=DB_DB, password=DB_PASS)
        self.faker = Faker(['pl_PL'])

    async def all_from_basic(self) -> List[dict]:
        async with self.pool.acquire() as c:
            rows = await c.fetch('SELECT * FROM basic ORDER BY id')
        return dicts(rows)

    async def random_write(self):
        name = self.faker.name()
        address = self.faker.address()

        async with self.pool.acquire() as c:
            person_id = await c.fetchval('''
                    INSERT INTO PERSONS(name, address) VALUES ($1,$2) RETURNING id''',
                                    name, address)
            print(f'inserted person with id={person_id}')


async def main_task():
    db = DB()
    await db.init()
    data = await db.all_from_basic()
    print(f'data={data}')
    await db.random_write()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_task())
    print('---done---')
    loop.close()
