import sys
import math
a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
dt = b*b - 4*a*c
x1 = 0
x2 = 0
if dt > 0:
    x1 = (b * -1 + math.sqrt(dt)) / 2 * a
    x2 = (b * -1 - math.sqrt(dt)) / 2 * a
    print(int(x1))
    print(int(x2))
elif dt == 0:
    x1 = (b * -1) / (2 * a)
    print(int(x1))

else:
    print("")
