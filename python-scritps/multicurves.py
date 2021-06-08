# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 21:42:09 2020

@author: YuanbaoQiang
"""

######################################################################### 
'''This is a simple script to deal with txt files output from **log.py**
Keep only txt files and multicurve.py in the same folder'''
######################################################################### 




import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame 
import pandas as pd 
import glob,os


path=os.getcwd()
file=glob.glob(os.path.join(path, "*.txt"))
print(file)
dl = []
for f in file:
  dl.append(pd.read_csv(f,sep='\s+',infer_datetime_format=True))

'''title'''
plt.title( 'Change of temp')
'''x axis'''
plt.xlabel( 'Step')
'''y axis'''
plt.ylabel( 'Temperature(K)')

'''figure setting'''
plt.rcParams['figure.figsize'] = (8, 4) 
plt.rcParams['savefig.dpi'] = 300 


# Sample of three *.txt files
df0 = DataFrame(dl[0])
df1 = DataFrame(dl[1])
df2 = DataFrame(dl[2])
plt.plot(df0.loc[:,'Step'],df0.loc[:,'c_T_C'])
plt.plot(df1.loc[:,'Step'],df1.loc[:,'c_T_C'])
plt.plot(df2.loc[:,'Step'],df2.loc[:,'c_T_C'])
