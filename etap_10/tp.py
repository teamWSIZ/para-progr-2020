import threading
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from time import sleep


def t():
    return threading.current_thread().name


def clock():
    return datetime.now().strftime('%H:%M:%S.%f')[:-3]


def log(what):
    print(f'[{clock()}]: {what}')


def zadanie(arg1, arg2):
    log(f'wykonuję zadanie {arg1} (drugi arg:{arg2}), wątek: {t()}')
    sleep(2.0)
    return arg1 * arg2


if __name__ == '__main__':
    pool = ThreadPoolExecutor(4)
    r = []
    for i in range(4):
        f = pool.submit(zadanie, 12, 14)
        r.append(f)
    for f in r:
        print(f.result())
    print(t())
