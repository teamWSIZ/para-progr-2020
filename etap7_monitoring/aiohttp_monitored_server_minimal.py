import asyncio
from asyncio import sleep
from datetime import datetime
from random import randint

from aiohttp import web
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST


def answer(msg: str):
    return web.json_response({'comment': msg})


routes = web.RouteTableDef()


# query = req.match_info.get('query', '')  # for route-resolving, /{query}
# query = req.rel_url.query['query']  # params; required; else .get('query','default')


@routes.get('/')
async def hello(req):
    calls_metric().inc()    # zwiększamy licznik
    return web.json_response({'comment': 'works OK'})


### prometheus integration
@routes.get('/metrics')
async def metrics(req):
    resp = web.Response(body=generate_latest())  # generate_latest --> prometheus client
    resp.content_type = CONTENT_TYPE_LATEST
    return resp


app = web.Application()
app.router.add_routes(routes)

##############
# Periodic monitoring
HOST = 'my_pc'


def calls_metric():
    return gauge().labels(HOST, 'calls')


def cpu_metric():
    return gauge().labels(HOST, 'cpu')


async def update_gauges():
    """Periodycznie zbierane informacje"""
    while True:
        cpu_metric().set(randint(0, 100))
        print('updated gauges', datetime.now())
        await sleep(5)


##############
# App creation

def gauge() -> Gauge:
    return app['pro']


async def pre_init():
    app['pro'] = Gauge('mygauge', 'Test gauge #1', ['host', 'metric'])  # rr = nazwa metryki, host/metric -- nazwy pól
    asyncio.create_task(update_gauges())


async def app_factory():
    await pre_init()
    return app


def run_it():
    web.run_app(app_factory(), port=3334, host='localhost')


run_it()
