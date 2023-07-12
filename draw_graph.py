import numpy as np
import matplotlib.pyplot as plt
import argparse
import re



#コマンドラインによるファイル指定
parser = argparse.ArgumentParser()
parser.add_argument("subject",nargs='*')
args = parser.parse_args()

#ファイル名から各種パラメータを取得する[目的関数,DE,ベースベクトルの選択方法,Y,交叉方法,NP,F,CR](実環境の場合)
parameter = args.subject.copy()
size = len(args.subject)
for i in range(size):
    parameter[i] = re.split(r'[/_]',parameter[i].replace('.csv','')) 

#ファイル読み取り
def read_file(subject,G,trails):
    result = np.zeros([G+1,trails+1])
    with open(subject,"r")as fr:
        for i in range(G+1):
            result[i] = fr.readline().split(",")
    return result


#散布図の作成
def make_scatterplot(result):
    file_name = f"report_{parameter[0][0]}.png"
    fig,ax = plt.subplots()
    for i in range(size):
        G = 10**5/int(parameter[i][5])
        x = np.arange(G+1)
        ax.plot(x,logscale(result[i]),label=make_name(i),marker="o",markersize=1)
    ax.set_xlabel("generation")
    ax.set_ylabel("lg(fitness+1)")
    plt.legend()
    plt.grid()
    plt.savefig(file_name)

def make_name(cnt):
    s = ""
    for i in range(1,5):
        s += f"{parameter[cnt][i]}/"
    for i in range(5,7):
        s += f"{parameter[cnt][i]}_"
    s += parameter[cnt][7]
    return s


#箱ひげ図作成
def make_boxplot(data):
    file_name = f"report_{parameter[0][0]}.png"
    for i in range(size):
        G = 10**5/int(parameter[i][5])
        fig,ax = plt.subplots()
        bp = ax.boxplot(data[i,G,:31])
        ax.set_xticklabels(make_name(i))
    plt.grid()
    plt.show()

def make_estimate(result):
    file_name = f"{parameter[0][0]}/{parameter[0][1]}_{parameter[0][6]}_{parameter[0][7]}_{parameter[0][2]}_NP={parameter[0][3]}_F={parameter[0][4]}_CR={parameter[0][5]}.png"
    fig,ax = plt.subplots()
    for i in range(size):
        ax.plot(result[0,0,:],result[0,1,:],marker="o")
    ax.set_xlabel(parameter[0][2])
    ax.set_ylabel("fitness")
    plt.grid()
    plt.savefig(file_name)

def read_es_file(G,trails):
    result = np.zeros([size,G+1,trails])
    cnt = 0
    for subject in args.subject:
        with open(subject,"r")as fr:
            for i in range(G+1):
                result[cnt,i] = fr.readline().split(",")
        cnt += 1
    return result

def logscale(value):
    y = np.log10(value+1)
    return y

data = []
cnt = 0
trails = 33
for subject in args.subject:
    G = 10**5/int(parameter[cnt][5])
    data.append(read_file(subject,int(G),trails))
    cnt += 1
data = np.array(data)
make_scatterplot(data[:,:,31])
# make_boxplot(data)

# data = read_es_file(1,100)
# make_estimate(data)
