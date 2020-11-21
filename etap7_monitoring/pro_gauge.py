from prometheus_client import Gauge

g = Gauge('my_inprogress_requests', 'Description of gauge')
g.inc()  # Increment by 1
g.dec(10)  # Decrement by given value
g.set(0)  # Set to a given value


# opis: https://github.com/prometheus/client_python

@g.track_inprogress()
def foo():
    pass


foo()
foo()


print(g.collect())

