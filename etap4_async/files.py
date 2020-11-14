import asyncio

import aiofiles

from simplelogger import log, log_print


def task_name():
    return asyncio.current_task().get_name()


async def write_large():
    async with aiofiles.open('d.txt', 'w') as out:
        for j in range(100):
            for i in range(1000):
                await out.write(f'line{j * 1000 + i}\n')
            await out.flush()
    print('done')


async def job(no):
    log(f'starting job {no}')
    await asyncio.sleep(0.100 * no)  # nieblokujące czekanie: wątek przechodzi do procesowania następnych task-ów
    log(f'nazwa taska: {task_name()}')
    log(f'finishing job {no}')


async def wait_jobs():
    await asyncio.wait([job(10) for i in range(100)])


async def main_task():
    log('start')
    # await write_large()
    t = asyncio.create_task(wait_jobs())
    async with aiofiles.open('d.txt') as f:
        async for line in f:
            log(line.strip())
    await t
    log('end')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_task())
    print('------')
    log_print()
    loop.close()
