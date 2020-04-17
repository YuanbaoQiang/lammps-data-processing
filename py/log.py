# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 21:42:09 2020

@author: YuanbaoQiang
"""

############################################################# 
'''This is a script to deal with log file from Lammps'''
'''Only one file can be exported at a time'''
############################################################# 

# Package import
import pandas as pd 
import numpy as np

# Intial file inpute
print('Input file sample: log.xxxx')
file = input('Please type your file name:')
print('\n')
print('Then you should type loop number you need, here is the loop count sample:')
print('*'*30)
print('''Per MPI rank memory...
...
...
...
Loop time of...''')
print('*'*30+'\n')

print('This is a complete loop, which starts from 0, and loop input you need must be an integer, , such as: 0,1,2,3...')

loop = int(input('Now, please type the loop you need:'))


# Count
count1 = []
count2 = []

# File open
with open(file,'r',encoding='UTF-8') as f_initial:
    lines = f_initial.readlines()
    num = len(lines)
    for i, line in enumerate(lines):
        if line.startswith('Per MPI rank memory'):
            start = i
            count1.append(start)
        if line.startswith('Loop time of'):
            end = i
            count2.append(end)

# Define the region you don't need
skip1 = np.arange(0,count1[loop]+1)
skip2 = np.arange(count2[loop],num)
skip = np.hstack((skip1,skip2))
df = pd.read_csv(r'./'+file,sep='\s+',skiprows=skip,infer_datetime_format=True)

# Save the txt file you need
result = file[4:]+'_'+str(loop)+'.txt'
df.to_csv(result,sep='\t',index=False,header=True)


print('\n'+'Completed')

