import asyncio
import json
from asyncio import sleep
from datetime import datetime
from http.client import BAD_REQUEST

import psutil
from aiohttp import web
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST, Histogram

from simplelogger import log

"""
For my_middleware see: https://rollout.io/blog/monitoring-your-asynchronous-python-web-applications-using-prometheus/

"""


def answer(msg: str):
    return web.json_response({'comment': msg})


routes = web.RouteTableDef()


# query = req.match_info.get('query', '')  # for route-resolving, /{query}
# query = req.rel_url.query['query']  # params; required; else .get('query','default')


@routes.get('/')
async def hello(req):
    raise RuntimeError('ha!')
    return web.json_response({'comment': 'some error'}, status=BAD_REQUEST)


@routes.get('/long_requests')
async def hello(req):
    long_metric().inc()
    print('long')
    await sleep(1.5)
    return answer(f'app works OK')


### prometheus integration
@routes.get('/metrics')
async def metrics(req):
    resp = web.Response(body=generate_latest())  # generate_latest --> prometheus client
    resp.content_type = CONTENT_TYPE_LATEST
    return resp


@web.middleware
async def my_middleware(request, handler):
    print(f'enter: {request.rel_url}')
    h = app['h']
    st = datetime.now().timestamp()
    calls_metric().inc()
    try:
        response = await handler(request)
        en = datetime.now().timestamp()
        delta = en - st
        h.observe(delta)
        print(f'finish in {delta:.3f}')
        return response
    except:
        message = 'internal exception'
        error_metric().inc()
    return web.json_response({'error': message})


app = web.Application(middlewares=[my_middleware])
app.router.add_routes(routes)

##############
# Periodic monitoring
HOST = 'my_pc'


def calls_metric():
    return gauge().labels(HOST, 'calls')


def long_metric():
    return gauge().labels(HOST, 'long')


def error_metric():
    return gauge().labels(HOST, 'error')


def cpu_metric():
    return gauge().labels(HOST, 'cpu')


async def update_gauges():
    """Periodycznie zbierane informacje"""
    while True:
        cpu_metric().set(psutil.cpu_percent())
        print('updated gauges', datetime.now())
        await sleep(5)


##############
# App creation

def gauge() -> Gauge:
    return app['RR']


async def pre_init():
    log('Creating aiohttp app')
    app['RR'] = Gauge('rr', 'test gauge', ['host', 'metric'])  # rr = nazwa metryki, host/metric -- nazwy pól
    buckets = []
    for i in range(1,21):
        buckets.append(0.0001*i)
    buckets.append(0.1)
    buckets.append(0.5)
    buckets.append(1)
    buckets.append(2)
    buckets.append(4)
    app['h'] = Histogram('rx', 'Call execution times', buckets=buckets)

    asyncio.create_task(update_gauges())


async def app_factory():
    await pre_init()
    return app


def run_it():
    web.run_app(app_factory(), port=3333, host='localhost')


run_it()
