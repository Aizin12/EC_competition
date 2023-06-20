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
arg = 10.12*np.random.rand(10)-5.12
result =rosenbrock(arg)
print(result)
