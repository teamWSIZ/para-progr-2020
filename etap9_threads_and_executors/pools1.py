import threading
from concurrent.futures._base import Future
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from time import sleep
from typing import List


def t():
    return threading.current_thread().name


def clock():
    return datetime.now().strftime('%H:%M:%S.%f')[:-3]


def log(what):
    print(f'[{clock()}]: {what}')


def zadanie(arg):
    log(f'wykonuję zadanie {arg}, wątek: {t()}')
    sleep(2.0)
    return arg * arg


executor = ThreadPoolExecutor(4)  # single physical thread; async

futures: List[Future] = []

for i in range(12):
    f = executor.submit(zadanie, i)  # wrzuca zadanie do wykonania; nie czeka na wynik
    futures.append(f)
    log(f'submitted {i}')
log('wszystkie zadania zasubmitowane')

# zebranie wyników
results = []
for fu in futures:
    results.append(fu.result()) # tu czekamy na rezultaty
log(results)
