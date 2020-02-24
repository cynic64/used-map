import random

"""
F urniture
T ools
E lectronics
C lothing
I nstruments
O ther
"""

path = "database.txt"

f = open(path, "w")

for i in range(100):
    f.write("{}, {}, {}\n".format(random.random(), random.random(), random.choice(list("FTECIO"))))

f.close()
