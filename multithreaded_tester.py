import requests
from concurrent.futures.process import ProcessPoolExecutor

from utils import ts

M = 5000
executor = ProcessPoolExecutor(16)


def job():
    # print(f'job on thread {threading.current_thread().name}')
    r = requests.get('http://localhost:2233/status')
    return len(r.json()['comment'])


# future = executor.submit(job)

futures = []
start = ts()
for i in range(M):
    futures.append(executor.submit(job))
result = sum(f.result() for f in futures)

print(f'check: 12={result/M}')

delta = ts() - start
print(f'{M} requests in {delta:.3f}s ({M / delta:.0f}RPS)')
