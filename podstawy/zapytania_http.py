import requests

r = requests.get('https://api.github.com/events')

res = r.json()
print(res[0])
