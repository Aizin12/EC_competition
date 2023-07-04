import numpy as np
import matplotlib.pyplot as plt
import argparse
import re



#コマンドラインによるファイル指定
parser = argparse.ArgumentParser()
parser.add_argument("subject",nargs='*')
args = parser.parse_args()

#ファイル名から各種パラメータを取得する[目的関数,DE,ベースベクトルの選択方法,Y,交叉方法,NP,F,CR]
parameter = args.subject
parameter = re.split(r'[/_]',parameter.replace('.csv',''))

num_E = 10**4
G = int(num_E/int(parameter[5]))
result = np.zeros([G+1,34])
with open(args.subject,"r")as fr:
    for i in range(G+1):
        result[i] = fr.readline().split(",")


#箱ひげ図
fig,ax = plt.subplots()
bp = ax.boxplot(result[G,:31])
ax.set_xticklabels([args.subject])
plt.grid()
plt.show()