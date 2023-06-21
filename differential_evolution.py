import numpy as np

N = 10

class objective_function:
    def __init__(self,array):
        self.array = array

    #並列化適応済
    def rastringen(self):
        sigma = np.zeros(len(self.array))
        sigma = arg**2 - 10*np.cos(2*np.pi*self.array)
        return 10*len(self.array)+sigma.sum()

    #for文で計算
    def rosenbrock(self):
        sigma = 0
        for i in range(1,len(self.array)-1):
            sigma += 100*(self.array[i+1]-self.array[i]**2)**2 + (self.array[i]-1)**2
        return sigma

    #計算の正確性の確認
    def  checkfunction(self):
        f = objective_function(np.zeros(10))
        print(f.rosenbrock())
        
class DifferentialEvolutin(self):
    def __init__(self,NP,F,CR,f_type):
        self.NP =NP #母集団サイズ
        self.F = F  #差分重量
        self.CR = CR #交差率
        self.f_type = f_type #評価関数の種類

    ind = np.zeros(self.NP,N)

    #初期集団生成
    def initialization(self):
        for i in range(0,self.NP)




arg = np.zeros(10)
arg2 = np.zeros(10)
