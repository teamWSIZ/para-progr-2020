from simplelogger import log, log_print

log('st')
with open('d.txt', 'r') as file:
    data = file.read()
log(f'size:{len(data)/1000}kB')
log('ed')
log_print()