# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 09:00:45 2020

@author: YuanbaoQiang
"""

# print('    $bond:cc1'+'  @bond:Backbone'+  '  $atom:bead1'+'/ch3  $atom:bead2'+'/ch2')

# for i in range(0,175):
#     print('    bead1'+' = '+'new ch3.move(10,10,3)')
  
bond_length=1.54

print('    bead1'+' = '+'new ch3.move(10,10,3)') 
for i in range(0,176):
    print('    bead'+str(i+2)+' = '+'new ch2.move('+'10,10,'+str(bond_length*(i+1)+3)+')')
print('    bead'+str(i+3)+' = '+'new ch3.move(10,10,'+str(((i+2)*bond_length)+3)+')')
