import numpy as np
import datetime
import random

#-----パラメーター------

D = 10  #rastrigen関数,rosenbrock関数の次元の数
num_E = 10**6


#-----目的関数-----

def rastrigen(array):   #並列化適応済
    array = 10.24*array - 5.12 
    sigma = np.zeros(len(array))
    sigma = array**2 - 10*np.cos(2*np.pi*array)
    return 10*len(array)+sigma.sum()

def rosenbrock(array):  #for文で計算
    array = 4.196*array - 2.048
    sigma = 0
    for i in range(0,len(array)-1):
       sigma += 100*((array[i+1]-array[i]**2)**2)+ (array[i]-1)**2
    return sigma

#計算の正確性の確認
def  check_function(func,seed):
    np.random.seed(seed)
    array = np.zeros(D)
    array = np.random.rand(D)
    result = func(array)
    array = array.reshape(1,D)
    with open('check_function.csv','at') as cfile:
        np.savetxt(cfile,[func.__name__],fmt="%s",newline="\n")
        np.savetxt(cfile,array,delimiter=',')
        np.savetxt(cfile,[result])
        np.savetxt(cfile,[datetime.datetime.now()],fmt="%s")



#------差分進化の関数-----
class DifferentialEvolution:
    def __init__(self,NP,F,Y,CR,target):
        self.NP =NP #母集団サイズ
        self.F = F  #スケーリングサイズ
        self.Y = Y
        self.CR = CR #交差率
        self.target = target #目的関数の種類
        self.ind = np.zeros((NP,D)) #遺伝子
        self.base_verctor = np.zeros(D) #ベースベクトル
        self.target_vector = np.zeros(D) #ターゲットベクトル
        self.v = np.zeros(D) #変異ベクトル
        self.u = np.zeros(D) #トライアルベクトル
        self.path = f"./{target.__name__}/DE_{NP}_{F}_{Y}_{CR}.csv" #結果格納用アドレス名

    #初期集団生成
    def initializate(self):
        self.ind = np.random.rand(self.NP,D)

    #評価 
    def evaluate(self):
        result = np.zeros(self.NP)
        for i in range(self.NP):
            result[i] = self.target(self.ind[i])
        return np.amin(result)

    #乱数によるベースベクトルの選択
    def random_base_select(self):
        self.base_verctor = self.ind[np.random.randint(0,self.NP)].copy()

    #差分突然変異
    def mutation(self):
        #重複のない乱数生成
        select = np.random.permutation(self.NP)
        select = select[:2*self.Y]
        
        sigma = np.zeros(D)
        for i in range(self.Y):
            sigma += (self.ind[int(select[2*i])] - self.ind[int(select[2*i+1])])

        self.v = self.base_verctor + self.F*sigma
        
    #二項交差
    def  binomial_crossover(self):
        self.u = self.target_vector.copy()
        jr = np.random.randint(D)
        for j in range(D):
            r = np.random.rand()
            if(r < self.CR) or (j == jr):
                if(self.v[j] < 0):
                    self.u[j] = self.base_verctor[j] + np.random.rand()*(-self.base_verctor[j])
                elif (self.v[j] > 1):
                    self.u[j] = self.base_verctor[j] + np.random.rand()*(1-self.base_verctor[j])
                else:
                    self.u[j] = self.v[j].copy()


#
    def DE_random_Y_binomial(self):
        result = np.zeros(int(G)+1)

        self.initializate()
        result[0] = self.evaluate()
    
        for g in range(int(G)):
            for i in range(self.NP):
                self.target_vector = self.ind[i].copy()
                self.random_base_select()
                self.mutation()
                self.binomial_crossover()
                if (self.target(self.u) < self.target(self.target_vector)):
                    self.ind[i] = self.u.copy()
            result[g+1] = self.evaluate()
        return result


#
class  Runner:
    def __init__(self,NP,F,Y,CR,target):
        self.NP =NP #母集団サイズ
        self.F = F  #スケーリングサイズ
        self.Y = Y  #差ベクトルの数
        self.CR = CR #交差率
        self.target = target #目的関数の種類
        
    def DE_random_Y_binomial(self):
        evolution = DifferentialEvolution(self.NP,self.F,self.Y,self.target,self.target)
        G =  num_E/NP
        result = np.zeros((int(G)+1,34))

        for i in range(31):
            np.random.seed(i)
            result[:,i] = evolution.DE_random_Y_binomial()


        for g in range(int(G)+1):
            result[g,31] = np.average(result[g])
            result[g,32] = np.median(result[g])
            result[g,33] = np.std(result[g])

        with open(evolution.path,'wt') as cfile:
            np.savetxt(cfile,result,delimiter=',')
            np.savetxt(cfile,[datetime.datetime.now()],fmt="%s")
        


# -----main-----

evolution = Runner(100,1,1,1,rastrigen)
