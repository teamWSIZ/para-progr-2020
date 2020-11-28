import asyncio
from asyncio import sleep
from dataclasses import asdict, dataclass
from datetime import datetime

import aiohttp_cors
import psutil
from aiohttp import web
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

from simplelogger import log

"""
For middleware see: https://rollout.io/blog/monitoring-your-asynchronous-python-web-applications-using-prometheus/

"""


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
    req.app['RR'].labels('call_count', 'hello').inc()  # access fields, rr{field1="val1",field2="hello"} 1.0
    return answer(f'app works OK')


### prometheus integration
@routes.get('/metrics')
async def metrics(req):
    resp = web.Response(body=generate_latest())
    resp.content_type = CONTENT_TYPE_LATEST
    return resp


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
# Periodic monitoring

def network_io():
    gg = psutil.net_io_counters(pernic=True)['wlp59s0']
    return gg.bytes_sent / 1000, gg.bytes_recv / 1000


async def update_gauges():
    while True:
        app['RR'].labels('cpu', 'hello').set(psutil.cpu_percent())
        net = network_io()
        app['RR'].labels('net_sent', 'hello').set(net[0])
        app['RR'].labels('net_recv', 'hello').set(net[1])
        print('updated gauges', datetime.now())
        await sleep(5)


##############
# App creation

async def pre_init():
    log('Creating aiohttp app')
    app['RR'] = Gauge('rr', 'test gauge', ['field1', 'field2'])  #
    asyncio.create_task(update_gauges())


async def app_factory():
    await pre_init()
    return app


def run_it():
    web.run_app(app_factory(), port=2233, host='localhost')


run_it()
