from argparse import ArgumentParser


def get_args():
    p = ArgumentParser()
    p.add_argument('-p', '--port', help='App port', default='8833')
    return p.parse_args()


print(get_args().port)
