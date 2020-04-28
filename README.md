# LAMMPS_TOOLBOX

"""
@author: YuanbaoQiang
"""

##log.py

'''
This is a simple script to deal with log file from Lammps

Only one file can be exported at a time
'''

**Input**
You should follow the point shown in the running window.
In this script, you should input two parameters:

1. The full name of log file you need to deal with;
2. The loop number, start from zero, and must be a integer.

**Output**
If the two parameters you typed are log.50 and 0, the final name is log_50_0(normally).

 <br />
##multicurves.py
'''
This is a simple script to deal with txt files output from **log.py**
Keep only txt files and multicurve.py in the same folder
I have also provided three sample txt files in examples/multicurves
'''
**Input**
*.txt files;

**Output**
Rough preview of results(such as temp, e_bond, etc. parameters you setted in thermo_style)

 <br />

##contour.py

**Input**

see files in example and py script

**Output**

a figure with subgraphs