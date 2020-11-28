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
    app['request_count'] += 1
    return answer(f'app works OK')


@routes.get('/test')
async def hello(req):
    app['request_count'] += 1
    print(f'current counter: {app["request_count"]}')
    return web.json_response({"result": 15, "comment": 'OK'})


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

async def pre_init():
    log('Creating aiohttp app')
    app['request_count'] = 0


async def app_factory():
    await pre_init()
    return app


def run_it():
    web.run_app(app_factory(), port=2234)


run_it()
