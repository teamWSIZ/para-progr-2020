import requests
from utils import ts

M = 100  # liczba zapytań do serwera http


def job():
    r = requests.get('http://localhost:2233/status')
    return len(r.json()['comment'])


st = ts()
g = 0

for i in range(M):
    g += job()

en = ts()
delta = en - st
print(f'{M} requests in {delta:.3f}s ({M / delta:.0f}RPS)')
