# -*- coding:utf-8 -*-
import numpy as np
from sklearn import svm
import pandas as pd
import csv

dir = "32_0616/"
outdir = "./result/"
clu_list = [str(i) for i in range(32)]  # 32个类别
for clu in clu_list:
    num = 13506
    # num = 5
    collist = [i for i in range(1, num + 1)]
    df = pd.read_csv(dir + clu + ".csv", header=None, usecols=collist)
    X_train = df.ix[:, collist[0:-1]]
    names = np.array(df.ix[:, num])
    train_array = X_train.values
    print(names)
    # fit the model
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    clf.fit(X_train)
    y_pred_train = clf.predict(X_train)
    print(y_pred_train)
    csvfile = open(outdir+"result"+clu+".csv", 'wt',encoding="UTF8", newline="")
    writer=csv.writer(csvfile, delimiter=",")
    writer.writerows(zip(names, y_pred_train))
    csvfile.close()