import asyncio
import concurrent.futures
import threading
from datetime import datetime
from math import sin
from PIL import Image
from PIL import Image, ImageEnhance
from resizeimage import resizeimage


def t():
    return threading.current_thread().name


def ts():
    return datetime.now().timestamp()


def clock():
    return datetime.now().strftime('%H:%M:%S.%f')[:-3]


def log(what):
    print(f'[{clock()}]: {what}')


def cover_job(path, file, file_small, height=320, width=200):
    # will resample if needed to get required size, ratio preserved
    log('saving')
    with open(path + file, 'r+b') as f:
        with Image.open(f) as image:
            res = resizeimage.resize_cover(image, (height, width))
            res.save(path + file_small, image.format)
            log(f'saved, {t()}')
    return 1


def compute_job():
    res = 0
    log('compute start')
    for i in range(10000):
        res += sin(i)
    log(f'compute end, {t()}')
    return int(res)


async def tick():
    await asyncio.sleep(0.1)
    log(f'. {t()}')
    return 1


async def small_update():
    await asyncio.sleep(0.1)
    log(f'. {t()}')


async def main():
    loop = asyncio.get_running_loop()
    tasks = []
    st = ts()
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=64)
    for i in range(100000):
        if i % 10 == 0:
            # cover_job(*['./', 'plasma.png', 'sm_plasma.png', 300, 300])
            # t = loop.run_in_executor(pool, cover_job, *['./', 'plasma.png', f'sm_plasma.png', 300, 300])
            t = loop.run_in_executor(pool, compute_job)
            tasks.append(t)
        else:
            tasks.append(asyncio.create_task(tick()))

    log(f'before main.await: {ts() - st:.6f}s')
    w = await asyncio.wait(tasks)  # czeka na wszystkie, zbiera wyniki
    # print(w)
    pool.shutdown()
    log(f'after main.await: {ts()-st:.6f}s')


asyncio.run(main())
