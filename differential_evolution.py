import numpy as np

#rastrigen関数,rosenbrock関数の次元の数
N = 10

#並列化適応済
def rastrigen(array):
        sigma = np.zeros(len(array))
        sigma = array**2 - 10*np.cos(2*np.pi*array)
        return 10*len(array)+sigma.sum()

#for文で計算
def rosenbrock(array):
    sigma = 0
    for i in range(1,len(array)-1):
       sigma += 100*(array[i+1]-array[i]**2)**2 + (array[i]-1)**2
    return sigma

#計算の正確性の確認
def  checkfunction():
    f = objective_function(np.zeros(N))
    print(f.rosenbrock())
        
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




a = DifferentialEvolutin(10,1,1,rastrigen)
a.initializate()
result = a.evaluate()
print(result)
