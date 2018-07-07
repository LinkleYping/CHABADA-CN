# coding:utf-8
import pandas as pd

dir = "./merge/"
list = [i for i in range(32)]
for i in list:
    refile = "0.01result"+str(i)+".csv"
    name1 = ['package', 'T/F']
    df1 = pd.read_csv("./32_0616/"+refile, header=None, names=name1, encoding='utf-8')

    name2 = ['package', 'describe','name','undef']
    df2 = pd.read_csv("appdescNew.csv", header=None, names=name2, encoding='utf-8')

    result = pd.merge(df1, df2, how="outer")
    final = result[['T/F', 'describe', 'name']]
    final.to_csv(dir+refile, encoding="utf-8", index=False)
