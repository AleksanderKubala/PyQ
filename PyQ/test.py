from PyQ.Circuit import Circuit
x = Circuit(2)
print(x.get_results())
x.set_ideal(False)
for i in range(x.layer_count):
    x.next()
    print(x.get_results())
