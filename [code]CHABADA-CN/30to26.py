#coding=utf-8
__author__ = 'jyj'

import json
import numpy as np
import ast
from pandas import *

f = open("result.json",'r')
jsonl = f.read()
newjson = ast.literal_eval(jsonl)
df1 = pandas.DataFrame(newjson).T.fillna(0)
df1['index'] = df1.index

df2 = pandas.read_csv("new3.csv",header=None,iterator = True,)
df2 = df2.get_chunk(300001)
col_name = df2.columns[0]
df2 = df2.rename(columns = {col_name:'index'})

ff = pandas.merge(df1,df2)
ff.to_csv("nnew4.csv", encoding="utf-8")
