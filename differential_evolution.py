import numpy as np

#並列化適応済
def rastringen (arg):
    sigma = np.zeros(len(arg))
    sigma = arg**2 - 10*np.cos(2*np.pi*arg)
    return 10*len(arg)+sigma.sum()

#for文で計算
def rosenbrock (arg):
    sigma = 0
    for i in range(1,len(arg)-1):
        sigma += 100*(arg[i+1]-arg[i]**2)**2 + (arg[i]-1)**2
    return sigma


arg = np.zeros(10)
arg2 = np.zeros(10)
average = 0
average2 = 0

NUM = 10**6
for i in range(1,32):
    np.random.seed(i-1)
    for j in range(1,NUM+1):
        arg = 10.24*np.random.rand(10)-5.12
        arg2 = 4.096*np.random.rand(10) -2.048

        result1 = rastringen(arg)
        result2 = rosenbrock(arg2)
        average += result1
        average2 += result2
    average /= NUM
    average2 /= NUM

average /= 31
average2 /= 31
print(average)
print(average2)
