import asyncio

from simplelogger import log, log_print


def task_name():
    return asyncio.current_task().get_name()


async def job(no):
    log(f'starting job {no}')
    await asyncio.sleep(0.100 * no)  # nieblokujące czekanie: wątek przechodzi do procesowania następnych task-ów
    log(f'nazwa taska: {task_name()}')
    log(f'finishing job {no}')


async def main_task():
    await job(1)
    log('job #1 -- after await')
    log(f'nazwa taska: {task_name()}')

    t1 = asyncio.create_task(job(2))  # to już jest osobne zakolejkowane _zadanie_ (task)
    t2 = asyncio.create_task(job(3))  # kolejne niezależne zadanie
    await asyncio.sleep(0)
    log('tasks: after create_task')
    await t1
    await t2
    log('tasks: after await')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_task())
    print('------')
    log_print()
    loop.close()
