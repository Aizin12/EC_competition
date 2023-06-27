import numpy as np
import datetime
import random

N = 10  #rastrigen関数,rosenbrock関数の次元の数
num_E = 10**6


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


#差分進化の関数
class FuncDE:
    def __init__(self,NP,F,Y,CR,ftype):
        self.NP =NP #母集団サイズ
        self.F = F  #差分重量
        self.Y = Y
        self.CR = CR #交差率
        self.ftype = ftype #目的関数の種類
        self.ind = np.zeros((NP,N)) #遺伝子
        self.target_verctor = np.zeros(N) #ターゲットベクトル
        self.v = np.zeros(N) #変異ベクトル
        self.u = np.zeros(N) #トライアルベクトル

    #初期集団生成
    def initializate(self):
        self.ind = np.random.rand(self.NP,N)

    #評価 
    def evaluate(self):
        result = np.zeros(self.NP)
        for i in range(0,self.NP):
            result = self.ftype(self.ind[i])
        return np.amax(result)

    #乱数によるベースベクトルの選択
    def random_base_select(self):
        self.target_verctor = self.ind[np.random.randint(0,self.NP)]

    #差分突然変異
    def mutation(self):
        #重複のない乱数生成
        checker = np.zeros(self.NP)
        select = np.zeros(2*self.Y)
        loop_cnt = 0
        cnt = 0
        while(cnt<2*self.Y):
            if(np.random.rand()<1/self.NP) and (checker[loop_cnt] == 0):
                select[cnt] = loop_cnt
                checker[loop_cnt] = 1
                cnt += 1
            
            loop_cnt += 1
            if(loop_cnt >= self.NP):
                loop_cnt = 0
        
        sigma = np.zeros(N)
        for i in range(self.Y):
            sigma += (self.ind[int(select[2*i+1])] - self.ind[int(select[2*i])])

        self.v = self.target_verctor + self.F*sigma
        
    #二項交差
    def  binomial_crossover(self):
        self.u = self.target_verctor
        r = np.random.rand()
        if(r < self.CR):
            self.u = self.v
        return self.u
        


def DifferentialEvolution(X,Y,Z,NP,F,CR,ftype):
    evolution = FuncDE(NP,F,Y,CR,ftype)
    G = num_E / NP

    evolution.initializate()
    
    for g in range(G):
        evolution.X()



