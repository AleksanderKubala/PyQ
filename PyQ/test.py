from PyQ.Circuit import Circuit
from PyQ.Gatename import Gatename

x = Circuit(3)
x.start()
x.stop()
results = x.get_results()
x.start()
results = x.get_results()
print(results)