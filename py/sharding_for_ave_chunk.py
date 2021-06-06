# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 09:07:19 2021

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
# 该脚本文件用于处理Lammps模拟程序时间平均（Nevery Nrepeat Nfreq）导出的数据文件，下面有具体的示例
# 该脚本文件不需要同数据文件放在统一文件夹（如果是复制文件到数据文件所在文件夹下的方式，那么脚本版本过多，修改较为麻烦）
# 运行该脚本，根据控制台提示输入相应字符即可，自己想diy的话，也可参考我的代码进行改进即可~

# =============================================================================
# Lammps中涉及到的代码示例
# =============================================================================
# 注意：范例中因为个人需要只涉及到了温度云图、温度分布曲线、速度云图，速度分布曲线，导出的数据文件分别对应：
temp_cloud.profile, temp_distribution.profile, velocity_cloud.profile, velocity_distribution.profile
# 最好使用和我相同的文件名，因为导出的文件名在后续的'plot_for_ave_chunk.py'文件中有调用，
# 如有额外需要可以看懂代码后，自行DIY~

# 2d切分，数据可绘制云图
# 导出<温度>云图数据
# compute     1 A chunk/atom bin/2d y lower 0.05 z lower 0.005 units reduced
# compute     2 A temp/chunk 1 temp com yes
# fix         1 A ave/chunk 100 5 1000 1 temp norm sample bias 2 file temp_cloud.profile

# 导出<速度>云图数据
# compute         		7 A chunk/atom bin/2d y lower 0.05 z lower 0.005 units reduced
# fix             		8 A ave/chunk 100 5 1000 7 vz norm sample file velocity_cloud.profile 

# 1d切分，数据可绘制分布曲线
# 导出<温度>分布曲线数据
# compute     3 A chunk/atom bin/1d z lower 0.005 units reduced
# compute		4 A temp/chunk 3 temp com yes
# fix			6 A ave/chunk 100 5 1000 3 temp norm sample bias 4 file temp_distribution.profile 

# 导出<速度>分布曲线数据
# compute     9 A chunk/atom bin/1d z lower 0.005 units reduced
# fix         5 A ave/chunk 100 5 1000 9 vz norm sample file velocity_distribution.profile

# =============================================================================
# 最终达到的效果
# =============================================================================
# 假如./下，存在temp_cloud.profile，temp_distribution.profile，velocity_cloud.profile，velocity_distribution.profile四个数据文件
# 运行该脚本后，可分别得到四个文件夹，分别为temp_cloud，temp_distribution，velocity_cloud，velocity_distribution，
# 处理好的文件会根据自己设定的前后缀名<prefix_suffix_index_of_output_file>归类到对应文件夹

"""
# =============================================================================
# 导入相关依赖
# =============================================================================
import glob, os, shutil, sys, time

# =============================================================================
# 获得数据文件列表，默认为.profile文件
# =============================================================================
# 切换工作目录至待处理数据文件(.profile文件)的所在文件夹
print("=" * 60, end="")
target_dir = input('>>> 请输入待处理数据文件(.profile)的所在目录 <target_dir> : ')
# data_dir = input('>>> 请输入不同数据区域的 <target_dir> : ')

# 切换目录
os.chdir(target_dir)

# 将符合*.profile条件的数据文件都加入到列表中
file = glob.glob(os.path.join("*.profile"))

# 判空操作，如果file中无数据文件，有两种可能：
# 1. 输入的路径地址不对
# 2. 数据文件格式不符合，可自行修改
if not file:
    print("*" * 25 + "程序警告" + "*" * 25)
    print(">>> 请确认: ")
    print(">>> 1. 数据文件是否在<target_dir>下?\n" + ">>> 2. 数据文件后缀是否和程序指定后缀一致?")
    sys.exit()

# =============================================================================
# 选择需要处理的数据文件，步长设置，导出文件名等基本设置
# =============================================================================
# 遍历当前目录下的.profile的文件列表，并且输出显示，方便用户选择文件编号
# index: 文件名
print("=" * 60)
prefix_name_of_file = []
for i in range(0, len(file)):
    print(str(i) + ": " + file[i])

    # 获取文件的前缀名称
    prefix_name_of_file.append(file[i][:-7])

# print("根据👆👆👆👆👆👆👆列表，选择你要读取的文件编号！")
input_file_name_index = int(input('>>> 请输入数据文件编号 <input_file_name_index> : '))
input_file_name = file[input_file_name_index]

# print("\n" + "*" * 45)
# print("读取restart文件，起始步数为上一个restart文件的最终步数！")
# initial_step = int(input('请输入起始步数 <initial_step> : '))

print("=" * 60, end="")
# print("输入Nevery, Nrepeat, and Nfreq参数中的 Nfreq，每Nfreq步就导出一个文件")
Nfreq = int(input('>>> 请输入步长 <Nfreq> : '))

# compute 1 A chunk/atom bin/2d y lower 0.05 z lower 0.005 units reduced
# 每次平均的时间步下共有的bin的数量，这里一共有 1/0.05 * 1/0.005 = 4000个
# bins = int(1/0.05 * 1/0.005)
# print("\n" + "*" * 45)
# print("units reduce参数归一化后，每一次切分的bin数量是确定的！")
# number_of_bins = int(input('请输入bins数量 <number_of_bins> : '))

# 定义输出文件的格式，可根据数据自行扩充列表
print("=" * 60)
prefix_suffix_name_of_output_file = ["temp", "velocity"]
for i in range(0, len(prefix_suffix_name_of_output_file)):
    print(str(i) + ": " + prefix_suffix_name_of_output_file[i])
# print("根据👆👆👆👆👆👆👆列表，选择输出文件的前缀、后缀编号！")
# print("\n" + "注意：本脚本输出文件的后缀与前缀保持一致，例如：temp_0.temp，temp_1.temp, velocity_0.velocity....")
prefix_suffix_index_of_output_file = int(input('>>> 请确认输出文件的前缀、后缀编号 <prefix_suffix_index_of_output_file> : '))

# =============================================================================
# 根据选中的数据文件，进行导出操作
# =============================================================================
# 读取原数据文件
print("=" * 60)
with open(input_file_name, 'r', encoding='UTF-8') as f_initial:
    # 文件开头如下所示：
    # Chunk-averaged data for fix 5 and group norm
    # Timestep Number-of-chunks Total-count
    # Chunk Coord1 Ncount vz
    # 2001000 200 20000
    # 1 0.0025 180.2 -0.000132923
    # 2 0.0075 82.4 0.000112361
    # 3 0.0125 100.4 9.63534e-05
    # ...
    
    # 读取到第3行数据，去除“#”字符，作为输出文件的第一行数据
    # first_line_of_output_file ---->  Chunk Coord1 Ncount vz
    for num, line in enumerate(f_initial):
        if num == 2:
            first_line_of_output_file = line[2:]
            break
    # 读取剩下的所有行
    lines = f_initial.readlines()
    # 数据的起始步数
    initial_step = int(lines[0].split()[0])
    # 最终导出的文件编号，每Nfreq步就导出一个文件
    count = 0
    # 定义初始行
    i = 0
    # 开始循环
    while(i < len(lines)):
        cur_step = initial_step + count * Nfreq
        next_loop_step = initial_step + (count + 1) * Nfreq       
        if lines[i].startswith(str(cur_step)):
            i += 1
            str_name = prefix_suffix_name_of_output_file[prefix_suffix_index_of_output_file]
            with open(str_name + '_' + str(count + 1) + '.' + str_name, 'w', encoding='UTF-8') as f_output:
                f_output.write(first_line_of_output_file)
                
                # bin数量确定的情况
                # for j in range(0, number_of_bins):
                #     f_output.write(lines[i])
                #     i += 1
                
                # bin数量不确定的时候            
                while i < len(lines) and not lines[i].startswith(str(next_loop_step)):
                    if i + 1 < len(lines) and not lines[i + 1].startswith(str(next_loop_step)):
                        f_output.write(lines[i])
                    elif i + 1 < len(lines) and lines[i + 1].startswith(str(next_loop_step)) or i + 1 == len(lines):
                        # s.rstrip(rm) 删除s字符串中结尾处，位于rm删除序列的字符
                        f_output.write(lines[i].rstrip('\n'))
                    i += 1
            f_output.close()
        count += 1
        print("\r", end="")
        print("正在处理文件，数据处理进度: {:.1f}%: ".format(i * (100 / len(lines))), "▋" * int(i * (100 / len(lines)) // 2), end="")
        sys.stdout.flush()
        time.sleep(0.02)
# 关闭数据流
f_initial.close();   

# =============================================================================
# 将处理好的数据归类到对应的文件夹内
# =============================================================================
# dir_path为导出的数据文件所在的最终地址
# temp_cloud ---> ./temp_cloud/
# temp_distribution ---> ./temp_distribution/
dir_path = './' + prefix_name_of_file[input_file_name_index]
# 如果不存在该文件夹，则创建
if not os.path.exists(dir_path):
    # 创建文件夹
    os.makedirs(dir_path)
    
# 之前导出好的文件的前后缀名
prefix_name = prefix_suffix_name_of_output_file[prefix_suffix_index_of_output_file]
suffix_name = prefix_name
# 将目标文件存放到file列表中
file = glob.glob(os.path.join(prefix_name + '_*.' + suffix_name))
# 对文件进行排序，截取字符串中的数字
file.sort(key = lambda x: int(x[len(prefix_name) + 1 : -(len(prefix_name) + 1)]))

# 批量移动文件
count = 1
print()
for item in file:
    # 对于move移动命令: shutil.move(item, dir_path)
    # 如果文件已经存在，则报错
    # 而采用复制命令，可以直接覆盖文件
    shutil.copy(item, dir_path)
    # print("已将" + item + "复制到" + dir_path + "\n")
    # 复制完之后，需要删除./目录下的同名文件
    os.remove(item)
    # print("已将" + item + "从./下" + "删除" + "\n")
    print("\r", end="")
    print("正在转移文件，文件转移进度: {}%: ".format(count * (100 / len(file))), "▋" * int(count * (100 / len(file)) // 2), end="")
    sys.stdout.flush()
    time.sleep(0.02)
    count += 1
    
# 结束程序
print("\n" + "=" * 60)
print("所有流程已经执行完毕，接下来利用'plot_for_ave_chunk.py'进行数据处理叭！")