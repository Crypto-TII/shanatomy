import sys

file_name = sys.argv[1]
fp = open(file_name, 'rt')
times = fp.read()
fp.close()
times = times.split('\n')[:-1]
times = [float(t[29: 33]) for t in times]
print(sum(times) / len(times))
t = 0
for i in range(len(times)):
    if times[i] < 10:
        t +=1
print('terminated = ' + str(t))

