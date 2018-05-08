import sys

p = [70, 152, 195, 284, 475, 612, 791, 896, 810, 850, 737, 1332, 1469, 1120, 1470, 832, 1785, 2196, 1520, 1480, 1449];
answer = []
i = 0
for _p in p:
        if i != 0:
                answer.append(chr(_p / (i + 1)))
        else:
                answer.append(chr(_p))
        i = i + 1

for a in answer:
        sys.stdout.write(a)