# -*- coding:utf-8 -*-
import numpy as np
from sklearn import svm
import pandas as pd
import csv
import os

result_dir = './result/'


def gettrained(num):
    apps0 = csv.reader(open(num + ".csv", "r"))
    count = 0
    # print('hi')
    for line in apps0:
        name = line[13506]
        # print(name)
        flag = 0
        with open("virus2.csv", "r") as f1:
            apps1 = csv.reader(f1)
            for l1 in apps1:
                # print(name, l1[0])
                if l1[0] == name:
                    flag = 1
                    count = count + 1
                    print('delete', count)
                    break
            if flag == 0:
                with open(result_dir+"dele"+num+".csv", "a") as f:
                    writer = csv.writer(f)
                    writer.writerow(line)
    print('total deleted', count)
    f = open('result.txt', 'a')
    f.writelines(['===============\n' + num + ':' + str(count) + '\n'])
    f.close()


def ocsvm(serial, param):
    num = 13506
    # num = 5
    collist = [i for i in range(1, num + 1)]
    # df = pd.read_csv(dir + clu + ".csv", header=None, usecols=collist)
    df = pd.read_csv(serial+".csv", header=None, usecols=collist)
    df_train = pd.read_csv(result_dir + "dele" + serial + ".csv", header=None, usecols=collist)
    X = df.ix[:, collist[0:-1]]
    X_train = df_train.ix[:, collist[0:-1]]
    names = np.array(df.ix[:, num])  # package name
    # fit the model
    clf = svm.OneClassSVM(nu=param, kernel="rbf")
    clf.fit(X_train)
    y_pred_train = clf.predict(X)
    print(y_pred_train)
    csvfile = open(result_dir + str(param) + "result" + serial + ".csv", 'wt', encoding="UTF8", newline="")
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(zip(names, y_pred_train))
    csvfile.close()


def check(num, param):
    apps0 = pd.read_csv(result_dir + str(param) + "result" + num + ".csv", header=None)
    a = 0
    b = 0
    for line in apps0.itertuples():
        name = line[1]
        index = line[2]
        if int(index) == -1:
            b = b + 1
            with open("virus2.csv", "r") as f1:
                apps1 = csv.reader(f1)
                for l1 in apps1:
                    # print(name, l1[0])
                    if l1[0] == name:
                        a = a + 1
                        print('found', a)
                        # with open(result_dir + param + "result" + num + ".csv", "a") as f:
                        #     writer = csv.writer(f)
                        #     writer.writerow([name])
                        break

    print('true virus found:', a, ', judged virus:', b)
    return [a, b]


def run(num, param0):
    ocsvm(num, param0)
    [a, b] = check(num, param0)
    f = open('result.txt', 'a')
    f.writelines([str(param0) + ':' + str(a) + ',' + str(b) + '\n'])
    f.close()


if __name__ == '__main__':
    clulist = ['1', '7', '5', '15', '12', '19', '23', '27', '31']
    params = [0.1, 0.2, 0.3, 0.4, 0.5]

    for clu in clulist:
        aflag = 0
        for param in params:
            if aflag == 0:
                if os.path.exists('./result/dele' + clu + '.csv'):
                    print('ok')
                    pass
                else:
                    gettrained(clu)
                aflag = 1
            run(clu, param)
