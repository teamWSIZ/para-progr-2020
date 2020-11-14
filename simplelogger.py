from datetime import datetime

start = datetime.now().timestamp()


def clock():
    return datetime.now().timestamp() - start


logged = []


def log(what):
    logged.append(f'[{clock():.6f}]: {what}')


def log_print():
    for l in logged:
        print(l)
