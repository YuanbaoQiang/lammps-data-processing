# 为什么要数据处理？

对于开源分子动力学模拟软件`Lammps`导出的大数据量文件（单个数据文件上10G都是有可能的），是不太适合利用`Excel`或者`Origin`等常规软件来进行数据处理和绘图的。笔者从2020年正式学习`Lammps`时，就做了利用`Python`进行全流程（后处理+科研绘图）的尝试，也都取得了相关的论文成果，论文中除结构示意图外，数据图都是采用`Python`来进行的。

# 前期基础

## 博客

**我的博客地址**：[快乐学术猿_YuanbaoQiang_CSDN博客-LeetCode,剑指offer刷题记录,科研记录领域博主](https://blog.csdn.net/qyb19970829)，内容包含我的**研究生科研记录**、**Java学习记录**、**计算机基础**等内容，会长期更新自己的学习内容。

## 论文

**论文1**

+ **原文链接**：[Progressive Molecular Rearrangement and Heat Generation of Amorphous Polyethene Under Sliding Friction: Insight from the United-Atom Molecular Dynamics Simulations | Langmuir (acs.org)](https://pubs.acs.org/doi/10.1021/acs.langmuir.0c01949)
+ **审稿意见及回复**：[10.1021-acs.langmuir.0c01949](https://github.com/YuanbaoQiang/10.1021-acs.langmuir.0c01949)

# 仓库内容

本仓库分为两个文件夹：`examples`和`python-scritps`，`examples`主要是一些建模或者数据文件，`python-scritps`是一些**个人常用**的处理数据的脚本，专门针对`examples`中的数据文件做相关处理和数据图绘制。

# 脚本使用

笔者列出一些常见的可导出数据的`Lammps`命令，针对命令导出的数据文件，给出相应的脚本使用说明。

## ave/chunk

针对`ave/chunk`导出的`1d`切分和`2d`切分的数据文件，可利用[sharding_for_ave_chunk.py](https://github.com/YuanbaoQiang/lammps-data-processing/blob/master/python-scritps/sharding_for_ave_chunk.py) 和 [plot_for_ave_chunk.py](https://github.com/YuanbaoQiang/lammps-data-processing/blob/master/python-scritps/plot_for_ave_chunk.py)来进行数据的切分和数据图的简单绘制。使用方法见我的博客记录：[数据处理-500行Python代码处理ave/chunk命令下1d和2d分块数据_快乐学术猿-CSDN博客](https://yuanbaoqiang.blog.csdn.net/article/details/117651669)，代码注释较为详尽。