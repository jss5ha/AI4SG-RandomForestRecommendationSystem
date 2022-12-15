# This is a sample Python script.

from scipy import stats
import numpy as np
import pandas as pd

data = pd.read_csv('evalcode/AI4G Eval - Blind_December 12, 2022_15.50.csv')

sys1df = data.loc[data['Q1'] == '1']
sys2df = data.loc[data['Q1'] == '2']
sys3df = data.loc[data['Q1'] == '3']

print(type(sys1df))
print(sys1df.shape)
print(sys1df)

#just need to kruskal on these bad boys n we're good to go
l = [4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

print("1 v 2")
for  i in range(0, len(l)):
    s1 = (sys1df.loc[:,("Q"+str(l[i]))])
    s2 = (sys2df.loc[:,("Q"+str(l[i]))])
    print("q" + str(l[i]) + " " + str(stats.kruskal(s1,s2)))

print("3 v 2")
for  i in range(0, len(l)):
    s1 = (sys3df.loc[:,("Q"+str(l[i]))])
    s2 = (sys2df.loc[:,("Q"+str(l[i]))])
    print("q" + str(l[i]) + " " + str(stats.kruskal(s1,s2)))

print("1 v 3")
for  i in range(0, len(l)):
    s1 = (sys1df.loc[:,("Q"+str(l[i]))])
    s2 = (sys3df.loc[:,("Q"+str(l[i]))])
    print("q" + str(l[i]) + " " + str(stats.kruskal(s1,s2)))