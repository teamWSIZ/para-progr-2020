import threading
import time


def t():
    return threading.current_thread().name


class MyJob(threading.Thread):
    def __init__(self, title: str):
        threading.Thread.__init__(self)
        self.title = title  # jakiś napis, który ustalamy przy uruchomieniu wątku; będzie jego własnością

    def run(self):
        print(f'title:{self.title}; nazwa:{t()} ---- start')
        time.sleep(100)
        print(f'title:{self.title}; nazwa:{t()} ---- koniec')


jobs = []
for i in range(5):
    MyJob(f'job{i}').start()
