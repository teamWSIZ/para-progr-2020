from time import sleep
import psutil

# info: https://psutil.readthedocs.io/en/latest/

for i in range(30):
    # print(psutil.getloadavg())
    # print(psutil.cpu_percent())
    # print(psutil.disk_io_counters().read_bytes)
    # print(psutil.net_io_counters(pernic=True)['wlp59s0'].bytes_recv)
    # print(psutil.sensors_temperatures())
    # print(psutil.virtual_memory().total/1024/1024)
    # print(psutil.virtual_memory().total/1024/1024)
    # print(psutil.virtual_memory().active/1024/1024)
    print(psutil.virtual_memory().available/1024/1024)  # reported as available by `free -m`
    sleep(1)
