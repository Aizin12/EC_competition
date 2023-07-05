import numpy as np
import matplotlib.pyplot as plt
import argparse
import re



#コマンドラインによるファイル指定
parser = argparse.ArgumentParser()
parser.add_argument("subject",nargs='*')
args = parser.parse_args()

#ファイル名から各種パラメータを取得する[目的関数,DE,ベースベクトルの選択方法,Y,交叉方法,NP,F,CR](実環境の場合)
parameter = args.subject
size = len(args.subject)
for i in range(size):
    parameter = re.split(r'[/_]',parameter[i].replace('.csv','')) 

#ファイル読み取り
def read_file(G,trails):
    result = np.zeros([size,G+1,trails])
    cnt = 0
    for subject in args.subject:
        with open(subject,"r")as fr:
            for i in range(G+1):
                result[cnt,i] = fr.readline().split(",")
        cnt += 1
    return result


def make_scatterplot(result):
    file_name = f"{parameter[0]}/{parameter[1]}_{parameter[6]}_{parameter[7]}_{parameter[2]}_NP={parameter[3]}_F={parameter[4]}_CR={parameter[5]}.png"
    fig,ax = plt.subplots()
    for i in range(size):
        ax.plot(result[i,0,:],result[i,1,:],marker="o")
    ax.set_xlabel(parameter[2])
    ax.set_ylabel("fitness")
    plt.savefig(file_name)



#箱ひげ図作成
def make_boxplot():
    fig,ax = plt.subplots()
    bp = ax.boxplot(result[G,:31])
    ax.set_xticklabels([args.subject])
    plt.grid()
    plt.show()


data = read_file(1,100)
make_scatterplot(data)