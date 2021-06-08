# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 16:09:37 2020

@author: YuanbaoQiang
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy.interpolate
import glob,os


  

path=os.getcwd()
file=glob.glob(os.path.join(path, "*.temp"))#read all *.temp files
file.sort()#sort the file
print(file)
df = []
for f in file:
  df.append(pd.read_csv(f,sep='\s+',infer_datetime_format=True))

def xyz(df):
    dff = df.loc[(df['temp']>0)]  
    dfx = dff.loc[:,'Coord1']
    dfy = dff.loc[:,'Coord2']
    dfz = dff.loc[:,'temp']

    x=np.asarray(dfx)
    y=np.asarray(dfy)
    z=np.asarray(dfz)
       
    xll = x.min()
    xul = x.max()
    yll = y.min()
    yul = y.max()
    
    xi = np.linspace(xll, xul,1000)
    yi = np.linspace(yll, yul,1000)
    zi = scipy.interpolate.griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
    return xi,yi,zi


x0,y0,z0=xyz(df[0])#data in the first file
x1,y1,z1=xyz(df[1])#data in the second file
x2,y2,z2=xyz(df[2])#data in the third file

'''figure setting'''
plt.rcParams['savefig.dpi'] = 300 #dpi
plt.rcParams['figure.dpi'] = 300 #dpi



fig = plt.figure(figsize = (18,4))#figure size
vmin=0
vmax=500

norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)#Map colors between vmin ~ vmax
extent=(1,63,37,83)#define the data range(xl,xh,yl,yh)

#first
plt.subplot(1,3,1)
fig0=plt.imshow(z0,extent=extent,origin='lower',cmap = plt.cm.jet,norm = norm)
plt.xlim(2,63)
plt.ylim(40,78)

'''x axis'''
plt.xlabel( 'Y Direction'+'$\ (\AA)$')
'''y axis'''
plt.ylabel( 'Z Direction'+'$\ (\AA)$')

#second
plt.subplot(1,3,2)
fig1=plt.imshow(z1,extent=extent,origin='lower',cmap = plt.cm.jet,norm = norm)
plt.xlim(2,63)
plt.ylim(40,78)
'''x axis'''
plt.xlabel( 'Y Direction'+'$\ (\AA)$')
'''y axis'''
plt.ylabel( 'Z Direction'+'$\ (\AA)$')

#third
plt.subplot(1,3,3)
fig2=plt.imshow(z2,extent=extent,origin='lower',cmap = plt.cm.jet,norm = norm)
plt.xlim(2,63)
plt.ylim(40,78)

'''x axis'''
plt.xlabel( 'Y Direction'+'$\ (\AA)$')
'''y axis'''
plt.ylabel( 'Z Direction'+'$\ (\AA)$')

fig.subplots_adjust(right=0.9)



#colorbar size
l = 0.92
b = 0.2
w = 0.015
h = 1-2*b 


#对应 l,b,w,h；设置colorbar位置；
rect = [l,b,w,h] 
cbar_ax = fig.add_axes(rect) 
cb = plt.colorbar(fig2, cax=cbar_ax)
# cb=plt.colorbar(fig2,shrink=0.8)


plt.savefig('contour_different_t.png',bbox_inches='tight',dpi=300,pad_inches=0.0)
print('OK')
