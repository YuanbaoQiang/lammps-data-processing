# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 09:00:45 2020

@author: YuanbaoQiang
"""

print('    $bond:cc1'+'  @bond:Backbone'+  '  $atom:bead1'+'/ch3  $atom:bead2'+'/ch2')
for i in range(0,175):
    print('    $bond:cc'+str(i+2)+'  @bond:Backbone'+  '  $atom:bead'+str(i+2)+'/ch2  $atom:bead'+str(i+3)+'/ch2')    
    result='    $bond:cc'+str(i+3)+'  @bond:Backbone'+  '  $atom:bead'+str(i+3)+'/ch2  $atom:bead'+str(i+4)+'/ch3'  
print(result)

# with open('./data.txt','w') as f:
#     for i in range(0,9997):
#         f.write('    $bond:cc'+str(i+2)+'  @bond:Backbone'+  '  $atom:bead'
#               +str(i+2)+'/ch2  $atom:bead'+str(i+3)+'/ch2'+'\n')
    
   
     
# print('    bead1'+' = '+'new ch3.move(10,10,3)')  
# for i in range(0,98):

#     print('    bead'+str(i+2)+' = '+'new ch2.move('+'10,10,'+str(1.53*(i+1)+3)+')')
# print('    bead'+str(i+3)+' = '+'new ch3.move(10,10,'+str(((i+2)*1.53)+3)+')')
