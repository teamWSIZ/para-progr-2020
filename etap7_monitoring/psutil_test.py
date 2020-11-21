from time import sleep
import psutil

# info: https://psutil.readthedocs.io/en/latest/

for i in range(30):
    # print(psutil.getloadavg())
    # print(psutil.cpu_percent())
    # print(psutil.disk_io_counters().read_bytes)
    # print(psutil.net_io_counters(pernic=True)['wlp59s0'].bytes_recv)
    print(psutil.sensors_temperatures())
    sleep(1)
