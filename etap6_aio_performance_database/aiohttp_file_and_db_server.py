"""
Testuje operacje plikowe.
Zadane endpoint, którego wykonanie wymaga dostępu do pliku na dysku.
"""

from dataclasses import asdict, dataclass

import aiofiles
import aiohttp_cors
from aiohttp import web

from etap6_aio_performance_database.db_access import DB
from simplelogger import log


def answer(comment: str, status=200):
    return web.json_response(simple_response(comment), status=status)


@dataclass
class RestResult(object):
    comment: str
    data: str = ''


def simple_response(comment: str):
    return asdict(RestResult(comment))


routes = web.RouteTableDef()


# query = req.match_info.get('query', '')  # for route-resolving, /{query}
# query = req.rel_url.query['query']  # params; required; else .get('query','default')


@routes.get('/status')
async def hello(req):
    return answer(f'app works OK')


@routes.get('/files/blocking')
async def get_file_blocking(req):
    with open('data.txt', 'r') as file:
        data = file.read()
    res = {"data": data}
    return web.json_response(res)


@routes.get('/files/async')
async def get_file_blocking(req):
    async with aiofiles.open('data.txt') as f:
        data = await f.read()
    res = {"data": data}
    return web.json_response(res)


@routes.get('/db/basic')
async def get_file_blocking(req):
    data = await db().all_from_basic()
    res = {"data": data}
    return web.json_response(res)


@routes.get('/db/write')
async def get_file_blocking(req):
    data = await db().random_write()
    res = {"data": 'OK'}
    return web.json_response(res)


app = web.Application()
app.router.add_routes(routes)

#  setup generous CORS:
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

for route in list(app.router.routes()):
    cors.add(route)


##############
# App creation

def db() -> DB:
    return app['db']


async def pre_init():
    log('Creating aiohttp app')
    app['db'] = DB()
    await db().init()


async def app_factory():
    await pre_init()
    return app


def run_it():
    web.run_app(app_factory(), port=2234)


run_it()
