import asyncio
import concurrent.futures
import threading
from datetime import datetime

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


def cover(path, file, file_small, height=320, width=200):
    # will resample if needed to get required size, ratio preserved
    log('saving')
    with open(path + file, 'r+b') as f:
        with Image.open(f) as image:
            res = resizeimage.resize_cover(image, (height, width))
            res.save(path + file_small, image.format)
            log(f'saved, {t()}')


async def small_update():
    await asyncio.sleep(0.1)
    log(f'. {t()}')


async def main():
    loop = asyncio.get_running_loop()
    tasks = []
    st = ts()
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    for i in range(1000):
        if i % 10 == 0:
            cover(*['./', 'plasma.png', 'sm_plasma.png', 300, 300])
            # t = loop.run_in_executor(None, cover, *['./', 'plasma.png', 'sm_plasma.png', 300, 300])
            # t = loop.run_in_executor(pool, cover, *['./', 'plasma.png', 'sm_plasma.png', 300, 300])
            # tasks.append(t)
        else:
            tasks.append(asyncio.create_task(small_update()))

    log(f'before main.await: {ts()-st:.6f}s')
    await asyncio.wait(tasks)
    pool.shutdown()
    log(f'after main.await: {ts()-st:.6f}s')


asyncio.run(main())
