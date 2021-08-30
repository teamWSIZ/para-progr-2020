import asyncio
import time

from simplelogger import log, log_print


def task_name():
    return asyncio.current_task().get_name()


async def job(no):
    log(f'starting job {no}')
    await asyncio.sleep(0.100 * no)         #nieblokujące czekanie: wątek przechodzi do procesowania następnych task-ów
    time.sleep(0.100 * no)                  # blokujące czekanie: wątek (~~ ten jedyny ~~) się tu zatrzyma; cały świat stoi!!
    log(f'nazwa taska: {task_name()}')
    log(f'finishing job {no}')


async def main_task():
    log(f'nazwa taska: {task_name()}')
    t1 = asyncio.create_task(job(2))                    # to już jest osobne zakolejkowane _zadanie_ (task)
    t2 = asyncio.create_task(job(3))                    # kolejne niezależne zadanie
    await asyncio.wait([job(1) for i in range(3)])
    log('tasks: after create_task')
    await t1
    await t2
    log('tasks: after await')
    asyncio.create_task(job(10))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_task())
    print('------')
    log_print()
    loop.close()
