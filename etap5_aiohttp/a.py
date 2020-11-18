from argparse import ArgumentParser

import sys
print(f'[{sys.argv}]')


p = ArgumentParser(description='Potrzebne argumenty')
p.add_argument('-p','--port', help='App port', default='8833')
args = p.parse_args()
print(args.port)
