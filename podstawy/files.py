import json

with open('config.json', 'r') as f:
    dic = json.load(f)
    server_port = dic['server_port']
    print(server_port)

u = {}
u['abcc'] = 123

with open('data.json', 'w') as f:
    json.dump(u, f)
