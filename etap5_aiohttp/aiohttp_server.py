from asyncio import sleep
from dataclasses import asdict, dataclass

import aiohttp_cors
from aiohttp import web

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


@routes.get('/')
async def hello(req):
    counter().cnt += 1
    await sleep(1)
    return answer(f'app works OK')

@dataclass
class Counter:
    cnt = 0


def counter() -> Counter:
    return app['state']                                                     # zapinanie obiektów globalnych; app['state'] nie będzie się zmieniać (ale wnętrze Counter tak)

@routes.get('/test')
async def get_counters(req):
    counter().cnt += 1
    print(f'current counter: {counter().cnt}')
    return web.json_response({"result": counter().cnt, "comment": 'OK'})


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

async def app_factory():
    log('Creating aiohttp app')
    app['state'] = Counter()
    return app


def run_it():
    web.run_app(app_factory(), port=2234)


run_it()
