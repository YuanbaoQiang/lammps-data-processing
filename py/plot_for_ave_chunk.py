# -*- coding: utf-8 -*-
"""
Created on Mon May 31 13:24:12 2021

@author: YuanbaoQiang


# =============================================================================
# 前置说明
# =============================================================================
# 这是个人使用脚本，仅供参考，希望可以对你有所帮助！
# 建议看懂之后写出属于自己风格的脚本，让Python数据处理成为科研工作中的得力工具！
# 欢迎关注我的CSDN博客：https://blog.csdn.net/qyb19970829
# 本人专注于Java、Python数据处理、操作系统、计算机组成等领域的学习，欢迎交流讨论！

# =============================================================================
# 功能描述
# =============================================================================
# 本人仿真采用的单位为real
# 该脚本用于处理'sharding_for_ave_chunk.py'导出后的数据文件，可绘制1d分布曲线、2d分布云图                                                                                                                               

"""

# =============================================================================
# 导入相关依赖
# =============================================================================
import os, sys, re, time
import numpy as np
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
import scipy.interpolate

# =============================================================================
# 获得数据文件列表
# =============================================================================
target_dir = input("=" * 60 + '\n' + '>>> 请输入数据文件(.profile)的所在目录 <target_dir> : ')
# 切换工作目录
os.chdir(target_dir)

# 获得target_dir路径下的文件列表
item_list = os.listdir('./')
dir_index = 0
dir_list = []
# 获得当前目录下的文件夹列表
print("=" * 60)
for item in item_list:
    if os.path.isdir(item):
        dir_list.append(item)
        print(str(dir_index) + ": " + item)
        dir_index += 1
# 判空
if not dir_list:
    print("文件夹为空，程序退出！")
    sys.exit()

# print("根据👆👆👆👆👆👆👆文件夹列表，选择目标数据所在的文件夹！", end="")
selected_dir_index = int(input('>>> 请输入需要处理的文件夹序号 <selected_index> : '))

# 定义标记
temp_cloud_flag = False
temp_distribution_flag = False
velocity_cloud_flag = False
velocity_distribution_flag = False

# 将选中的文件夹标记为true
if dir_list[selected_dir_index] == "temp_cloud":
    temp_cloud_flag = True
elif dir_list[selected_dir_index] == "temp_distribution":
    temp_distribution_flag = True
elif dir_list[selected_dir_index] == "velocity_cloud":
    velocity_cloud_flag = True
elif dir_list[selected_dir_index] == "velocity_distribution":
    velocity_distribution_flag = True

# 如果选中的是cloud文件夹，则需要设置绘制云图所需的参数
if velocity_cloud_flag or temp_cloud_flag:
    upper_limit_x = int(input('>>> 请输入二维云图横轴上限 <upper_limit_x> : '))
    upper_limit_y = int(input('>>> 请输入二维云图纵轴上限 <upper_limit_y> : '))
    lower_limit_map = int(input('>>> 请输入云图数值下限 <lower_limit_map> : '))
    upper_limit_map = int(input('>>> 请输入云图数值上限 <upper_limit_map> : '))

# 获得处理好的数据文件列表
item_list = os.listdir('./' + dir_list[selected_dir_index] + '/')
# 利用正则表达式对文件列表排序
# 'temp_1.temp', 'temp_2.temp', 'temp_3.temp', 'temp_4.temp'.....
item_list = sorted(item_list, key = lambda i:int(re.search(r'(\d+)',i).group()))
# print(item_list)

# 切换目录
os.chdir('./' + dir_list[selected_dir_index])
# dl为列表类型，将文件转成DataFrame文件添加到列表中，方便后续操作
dl = []
for f in item_list:
  dl.append(pd.read_csv(f,sep='\s+',infer_datetime_format=True))

# 获取DataFrame文件的列名，方便后续根据索引名读取数据
column_name_list = list(dl[0])

# =============================================================================
# 定义相关函数
# =============================================================================
def distribution(i):
    """预处理（温度、速度）1d分布的DataFrame列表数据

    :param i: DataFrame列表中的索引
    :return: 返回行数据、列数据
    """
    
    # 横坐标x_name: column_name_list[1]  ---> Coord1
    x_name = column_name_list[1]
    # 纵坐标y_name: column_name_list[-1] ---> temp 或者 v
    y_name = column_name_list[-1]
    # 筛选出y轴数据>0的部分
    # df = dl[i]
    df = dl[i][(dl[i][y_name] != 0)]
    # 提取数据
    x = -df[x_name]
    if temp_distribution_flag:
        y = df[y_name]
    elif velocity_distribution_flag:
        y = df[y_name] * -1

    return x, y

def cloud(i):
    """预处理（温度、速度）2d分布的DataFrame列表数据

    :param i: DataFrame列表中的索引
    :return: 返回云图所需的数据
    """
    
    # 横坐标x_name: column_name_list[1] == "Coord1"
    x_name = column_name_list[1]
    # 纵坐标y_name: column_name_list[2] == "Coord2"
    y_name = column_name_list[2]
    # 纵坐标y_name: column_name_list[-1] == "temp" or "v"
    z_name = column_name_list[-1]
    # 筛选出z轴数据>0的部分
    df = dl[i][(dl[i][z_name] > 0)]  
    
    dfx = df[x_name] * upper_limit_x
    dfy = df[y_name] * upper_limit_y
    dfz = df[z_name]

    x = np.asarray(dfx)
    y = np.asarray(dfy)
    z = np.asarray(dfz)
       
    xll = x.min()
    xul = x.max()
    
    yll = y.min()
    yul = y.max()
    
    xi = np.linspace(xll, xul, 1000)
    yi = np.linspace(yll, yul, 1000)
    zi = scipy.interpolate.griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
    
    return xi, yi, zi

def plot_cloud(m, n, n_fre, time_step, initial_time, file_delta):
    """绘制（温度、速度）2d分布云图

    :param m: 最终出的图为m行
    :param n: 最终出的图为n列
    :param n_fre: ave/chunk中的采样步数
    :param time_step: Lammps运行的时间步数
    :param initial_time: 第一张云图对应的时间点，单位为ps
    :param file_delta: 每隔file_delta个文件输出一个图样
    """
    
    z_list_initial_index = initial_time_to_file_index(initial_time, n_fre, time_step)
    norm = matplotlib.colors.Normalize(vmin = lower_limit_map, vmax = upper_limit_map) 
    extent = (0, upper_limit_x, 0, upper_limit_y)
    subfig_index = 1
    subfig_list = []
    main_fig = plt.figure(dpi = 300,figsize = (12,10))
    for i in range(0, m):
        for j in range(0, n):
            plt.subplot(m, n, subfig_index)
            subfig_index += 1
            # j * 2代表每隔2个文件作图
            subfig = plt.imshow(z_list[z_list_initial_index + j * file_delta], extent = extent, origin='lower',cmap = plt.cm.hot, norm = norm)
            subfig_list.append(subfig)
            plt.xlim(0, upper_limit_x)
            plt.ylim(0, upper_limit_y)
            plt.xlabel( 'Y Direction'+'$\ (\AA)$')
            plt.ylabel( 'Z Direction'+'$\ (\AA)$')
            z_list_initial_index += 1
    
    main_fig.subplots_adjust(right=0.9)       
    
    # 颜色条大小
    l = 0.92
    b = 0.2
    w = 0.015
    h = 1 - 2 * b 

    # 对应 l,b,w,h；设置colorbar位置；
    rect = [l, b, w, h] 
    cbar_ax = main_fig.add_axes(rect) 
    plt.colorbar(subfig_list[-1], cax = cbar_ax)


def plot_distribution(count, n_fre, time_step, initial_time, file_delta):
    """绘制（温度、速度）1d分布曲线

    :param count: 一张图上共有count条曲线
    :param initial_time: 第一条曲线的时间点，单位为ps
    :param n_fre: 数据采样间隔
    :param file_delta: 输出曲线的间隔量，1代表隔一个数据文件输出一条曲线，2代表每隔两个数据文件输出一条曲线
    """
    
    # time_step_eachfile为每个文件之间的间隔时间，单位为ps
    time_step_eachfile = n_fre * time_step / 1000
    # 步长、时间步数按照自己需求设置
    file_index = initial_time_to_file_index(initial_time, n_fre, time_step)
    # fig, ax = plt.subplots()
    # for i in range(0, count):
    #     ax.plot(x_list[file_index + i], y_list[file_index + i])
    for i in range(0, count):
        plt.plot(x_list[file_index + i * file_delta], y_list[file_index + i * file_delta], label = str(initial_time + i * file_delta * time_step_eachfile) + 'ps')
    plt.legend(loc="upper right")
    plt.xlabel( 'Z Direction'+'$\ (\AA)$')
    if temp_distribution_flag:
        plt.ylabel( 'Temperature'+'$\ (K)$')
    elif velocity_distribution_flag:
        plt.ylabel( 'Velocity'+'$\ (\AA \ / \ fs)$')
    
            
    
def initial_time_to_file_index(initial_time, n_fre, time_step):
    """根据时间点返回对应的文件下标

    :param initial_time: 时间点，单位为ps
    :param n_fre: 采样间隔
    :param time_step: 时间步
    """
    # 每一个文件的跨度时间为  Nfre * timestep
    # file_index = 0 的文件对应的ps数为：(file_index + 1) * n_fre * time_step / 1000 = initial_time
    # file_index = initial_time * 1000 / n_fre / time_step - 1
    # 定义一个当前的时间 ps
    return int(initial_time * 1000 / n_fre / time_step - 1)
 
# =============================================================================
# 预处理数据
# =============================================================================
x_list = []
y_list = []
z_list = []
print("=" * 60)
for i in range(0, len(item_list)):
    if temp_distribution_flag or velocity_distribution_flag:
        x_list.append(distribution(i)[0])
        y_list.append(distribution(i)[1])
        # print("正在处理第%d个文件，还剩下%d个文件......"%(i + 1, len(item_list) - i - 1))
        print("\r", end="")
        print("正在处理文件，数据处理进度: {}%: ".format((i + 1) * (100 / len(item_list))), "▋" * int((i + 1) * (100 / len(item_list)) // 2), end="")
        sys.stdout.flush()
        time.sleep(0.02)
    elif velocity_cloud_flag or temp_cloud_flag:
        x_list.append(cloud(i)[0])
        y_list.append(cloud(i)[1])
        z_list.append(cloud(i)[2])
        # print("正在处理第%d个文件，还剩下%d个文件......"%(i + 1, len(item_list) - i - 1))
        print("\r", end="")
        print("正在处理文件，数据处理进度: {}%: ".format((i + 1) * (100 / len(item_list))), "▋" * int((i + 1) * (100 / len(item_list)) // 2), end="")
        sys.stdout.flush()
        time.sleep(0.02)
    
# =============================================================================
# 出图
# =============================================================================
print("\n" + "文件处理完毕，正在出图...")
# 为方便起见，画图程序已封装为函数调用，具体看上面的函数形参描述
# 图表绘制只能用于基本演示，正式图需要根据格式和自己需求来！！！
if temp_cloud_flag or velocity_cloud_flag:
    plot_cloud(1, 5, 1000, 0.5, 0.5, 10)
elif temp_distribution_flag or velocity_distribution_flag:        
    plot_distribution(5, 1000, 0.5, 0.5, 5)
print("绘图完毕，请到绘图区查看！", end="")