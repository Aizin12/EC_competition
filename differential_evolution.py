import numpy as np
import datetime

#rastrigen関数,rosenbrock関数の次元の数
N = 10

#並列化適応済
def rastrigen(array):
        array = 10.24*array - 5.12 
        sigma = np.zeros(len(array))
        sigma = array**2 - 10*np.cos(2*np.pi*array)
        return 10*len(array)+sigma.sum()

#for文で計算
def rosenbrock(array):
    array = 4.196*array - 2.048
    sigma = 0
    for i in range(0,len(array)-1):
       sigma += 100*((array[i+1]-array[i]**2)**2)+ (array[i]-1)**2
    return sigma

#計算の正確性の確認
def  checkfunction(func):
    np.random.seed(0)
    array = np.zeros(N)
    array = np.random.rand(N)
    result = func(array)
    array = array.reshape(1,N)
    with open('check_function.csv','at') as cfile:
        np.savetxt(cfile,[func.__name__],fmt="%s",newline="\n")
        np.savetxt(cfile,array,delimiter=',')
        np.savetxt(cfile,[result])
        np.savetxt(cfile,[datetime.datetime.now()],fmt="%s")
        
#遺伝子
class DifferentialEvolutin:
    def __init__(self,NP,F,CR,ftype):
        self.NP =NP #母集団サイズ
        self.F = F  #差分重量
        self.CR = CR #交差率
        self.ftype = ftype #目的関数の種類
        self.ind = np.zeros((NP,N)) 

    #初期集団生成
    def initializate(self):
        self.ind = np.random.rand(self.NP,N)

    #評価 
    def evaluate(self):
        result = np.zeros(self.NP)
        for i in range(0,self.NP):
            result = self.ftype(self.ind[i])
        return np.amax(result)    




# a = DifferentialEvolutin(10,1,1,rastrigen)
# a.initializate()
# result = a.evaluate()
# print(result)

checkfunction(rosenbrock)