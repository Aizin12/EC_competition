import numpy as np
import datetime
import random
from scipy import stats

#-----パラメーター------

D = 10  #rastrigin関数,rosenbrock関数の次元の数
num_E = 10**5


#-----目的関数-----

def rastrigin(array):   #並列化適応済
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
    def __init__(self,NP,F,Y,CR,G,target,base_select,crossover):
        self.NP =NP #母集団サイズ
        self.F = F  #スケーリングサイズ
        self.Y = Y #差ベクトルの数
        self.CR = CR #交差率
        self.G = G #世代数
        self.target = target #目的関数の種類
        self.ind = np.zeros((NP,D)) #遺伝子
        self.base_vector = np.zeros(D) #ベースベクトル
        self.base_id = 0    #ベースベクトルのID
        self.target_vector = np.zeros(D) #ターゲットベクトル
        self.best_vector = np.zeros(D)  #最適な遺伝子
        self.v = np.zeros(D) #変異ベクトル
        self.u = np.zeros(D) #トライアルベクトル

        #JADE用のパラメータ
        self.p = 0.05 #current-to-pbestの上p%を採用
        self.c = 0.1
        self.mu_F = 2*np.random.rand()
        self.mu_CR = np.random.rand()
        self.sum_F = 0
        self.sum_expF = 0
        self.sum_CR = 0
        self.sum_N = 0

        self.path = f"./{target.__name__}/DE_{base_select}_{Y}_{crossover}_{NP}_{F}_{CR}.csv" #結果格納用アドレス名

        self.base_select = base_select #ベースベクトルの選択方法
        self.dict_bs = {"rand":self.random_base_select, "best":self.best_base_select, "current-to-pbest":self.current_to_pbest_base_select} #参照できるように辞書化
        self.crossover = crossover #交叉方法
        self.dict_cr = {"bin":self.binomial_crossover} #参照できるように辞書化

    #初期集団生成
    def initializate(self):
        self.ind = np.random.rand(self.NP,D)

    #評価 
    def evaluate(self):
        result = np.zeros(self.NP)
        for i in range(self.NP):
            result[i] = self.target(self.ind[i])
        self.id = np.argmin(result)
        self.best_vector = self.ind[self.id].copy()
        self.list_best = np.argsort(result)[::-1]
        return np.amin(result)

    #乱数によるベースベクトルの選択
    def random_base_select(self):
        self.base_id = np.random.randint(0,self.NP)
        self.base_vector = self.ind[self.base_id].copy()

    #最良選択によるベースベクトルの選定
    def best_base_select(self):
        self.base_vector = self.best_vector

    #上位p%の乱数によるベースベクトル選択
    def current_to_pbest_base_select(self):
        n = int(self.NP*self.p)
        if(n <= 0):
            self.base_id = 0
        else:
            self.base_id = np.random.randint(0,n)
        self.base_vector = self.target_vector+self.F*(self.ind[self.list_best[self.base_id]].copy()-self.target_vector)

    #差分突然変異
    def mutation(self):
        #重複のない乱数生成
        select = np.random.permutation(self.NP)
        select = select[select != self.id]
        select = select[:2*self.Y]
        
        sigma = np.zeros(D)
        for i in range(self.Y):
            sigma += (self.ind[int(select[2*i])] - self.ind[int(select[2*i+1])])

        self.v = self.base_vector + self.F*sigma
        
    #二項交差
    def  binomial_crossover(self):
        self.u = self.target_vector.copy()
        jr = np.random.randint(D)
        for j in range(D):
            r = np.random.rand()
            if(r < self.CR) or (j == jr):
                if(self.v[j] < 0):
                    self.u[j] = self.base_vector[j] + np.random.rand()*(-self.base_vector[j])
                elif (self.v[j] > 1):
                    self.u[j] = self.base_vector[j] + np.random.rand()*(1-self.base_vector[j])
                else:
                    self.u[j] = self.v[j].copy()

    #入れ替え
    def substitute(self,i):
        if (self.target(self.u) < self.target(self.target_vector)):
            self.ind[i] = self.u.copy()
            self.sum_N += 1
            self.sum_F += self.F
            self.sum_expF += self.F**2
            self.sum_CR += self.CR

    #従う確率のパラメータの変更
    def exp_moving(self):
        if(self.sum_F != 0)and(self.sum_N != 0):
            self.mu_F = (1-self.c)*self.mu_F + self.c*self.sum_expF/self.sum_F
            self.mu_CR = (1-self.c)*self.mu_CR + self.c*self.sum_CR/self.sum_N
        
        self.sum_N = 0
        self.sum_F = 0
        self.sum_expF = 0
        self.sum_CR = 0
    
    
    def set_parameter(self):
        self.F = np.abs(stats.cauchy.rvs(loc=self.mu_F,scale=0.1))
        self.CR = np.abs(stats.norm.rvs(loc=self.mu_CR,scale=0.1))

        if(self.F > 2):
            self.F = 2
        if(self.CR > 1):
            self.CR = 1

    #進化計算の実行
    def run(self):
        result = np.zeros(int(self.G)+1)

        self.initializate()
        result[0] = self.evaluate()
    
        for g in range(int(self.G)):
            for i in range(self.NP):
                self.target_vector = self.ind[i].copy()
                self.dict_bs[self.base_select]()
                self.mutation()
                self.dict_cr[self.crossover]()
            if (self.target(self.u) < self.target(self.target_vector)):
                self.ind[i] = self.u.copy()
            result[g+1] = self.evaluate()
        return result

    #JADEの実行
    def jade(self):
        result = np.zeros(int(self.G)+1)

        self.initializate()
        result[0] = self.evaluate()
    
        for g in range(int(self.G)):
            for i in range(self.NP):
                self.target_vector = self.ind[i].copy()
                self.set_parameter()
                self.dict_bs[self.base_select]()
                self.mutation()
                self.dict_cr[self.crossover]()
                self.substitute(i)
            result[g+1] = self.evaluate()
            self.exp_moving()
        self.f = 2*np.random.rand()
        self.CR = np.random.rand()
        return result


#
class  Runner:
    def __init__(self,NP,F,Y,CR,target,base_select,crossover):
        self.NP =NP #母集団サイズ
        self.F = F  #スケーリングサイズ
        self.Y = Y  #差ベクトルの数
        self.CR = CR #交差率
        self.target = target #目的関数の種類
        self.base_select = base_select #ベースベクトルの選択方法
        self.crossover = crossover #交叉方法
        
    #実環境
    def main(self):
        G =  num_E/self.NP
        evolution = DifferentialEvolution(self.NP,self.F,self.Y,self.CR,G,self.target,self.base_select,self.crossover)
        result = np.zeros((int(G)+1,34))

        for i in range(31):
            np.random.seed(i)
            result[:,i] = evolution.run()


        for g in range(int(G)+1):
            result[g,31] = np.average(result[g])
            result[g,32] = np.median(result[g])
            result[g,33] = np.std(result[g])


        with open(evolution.path,'wt') as cfile:
            np.savetxt(cfile,result,delimiter=',')
            np.savetxt(cfile,[datetime.datetime.now()],fmt="%s")

    
    def jade(self):
        G =  num_E/self.NP
        evolution = DifferentialEvolution(self.NP,self.F,self.Y,self.CR,G,self.target,self.base_select,self.crossover)
        evolution.path = f"./{self.target.__name__}/JADE_{self.base_select}_{self.Y}_{self.crossover}_{self.NP}_{self.F}_{self.CR}.csv"
        result = np.zeros((int(G)+1,34))

        for i in range(31):
            np.random.seed(i)
            result[:,i] = evolution.jade()


        for g in range(int(G)+1):
            result[g,31] = np.average(result[g])
            result[g,32] = np.median(result[g])
            result[g,33] = np.std(result[g])


        with open(evolution.path,'wt') as cfile:
            np.savetxt(cfile,result,delimiter=',')
            np.savetxt(cfile,[datetime.datetime.now()],fmt="%s")

    #パラメータ推定
    def estimate(self,type):
        evolution.path = f"estimate/{evolution.target.__name__}_{type}_{self.NP}_{self.F}_{self.CR}_{self.base_select}_{self.crossover}.csv"
        result = np.zeros((2,100))
        if (type == "NP"):
            for i in range(100):
                self.NP = 50 + 50*i
                result[0,i] = self.NP
                result[1,i] = self.est_run()
           
        elif (type == "F"):
            for i in range(100):
                self.F = 0.02 + 0.02*i
                result[0,i] = self.F
                result[1,i] = self.est_run()

        elif (type == "CR"):
            for i in range(100):
                self.CR = 0.01*i
                result[0,i] = self.CR
                result[1,i] = self.est_run()
        
        result = np.reshape(result,(2, 100))
        with open(evolution.path,'wt') as fw:
            np.savetxt(fw,result,delimiter=',')
            np.savetxt(fw,[datetime.datetime.now()],fmt="%s")   


    #簡易環境
    def est_run(self):
        G = 5000 / self.NP
        evolution = DifferentialEvolution(self.NP,self.F,self.Y,self.CR,G,self.target,self.base_select,self.crossover)
        result = np.zeros([10,int(G+1)])
        for i in range(10):
            np.random.seed(i)
            result[i] = evolution.run()
        return np.average(result[:,int(G)])

        


# -----main-----
base_select = "current-to-pbest"
crossover = "bin"
evolution = Runner(100,1,1,1,rastrigin,base_select,crossover) #NP,F,Y,CR,target,base_select,crossover
# evolution.main()
evolution.jade()