import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


fig = plt.figure(figsize=(10, 5))  # 创建图
plt.rcParams["font.family"] = "FangSong"  # 支持中文显示
plt.ylim(-12, 12)  # Y轴取值范围
plt.yticks([-12 + 2 * i for i in range(13)], [-12 + 2 * i for i in range(13)])  # Y轴刻度
plt.xlim(0, 2 * np.pi)  # X轴取值范围
plt.xticks([0.5 * i for i in range(14)], [0.5 * i for i in range(14)])  # X轴刻度
plt.title("函数 y = 10 * sin(x) 在[0,2Π]区间的曲线")   # 标题
plt.xlabel("X轴")  # X轴标签
plt.ylabel("Y轴")  # Y轴标签
x, y = [], []  # 用于保存绘图数据，最开始时什么都没有，默认为空


def update(n):  # 更新函数
    x.append(n)  # 添加X轴坐标
    y.append(10 * np.sin(n))  # 添加Y轴坐标
    plt.plot(x, y, "r--")  # 绘制折线图


ani = FuncAnimation(fig, update, frames=np.arange(0, 2 * np.pi, 0.1), interval=50, blit=False, repeat=False)  # 创建动画效果
plt.show()  #

''' 参数说明
 在Matplotlib库中有一个子库animation，该库下定义了多种用于绘制动态效果图的类，例如FuncAnimation，ArtistAnimation等，我们这里主要介绍FuncAnimation的使用。该类通过重复调用某个功能函数从而实现动态绘图效果，在功能函数中会对图进行一些修改，只要调用时间间隔足够短，给人的感觉就是图在动态变化。创建FuncAnimation对象时，需要传递的主要参数及其含义如下： 
fig：用于显示动态效果的画布，即Figure对象；

func：函数名，重复调用的功能函数；

frames：每一帧数据，通常是可迭代对象，依次取出每一个数据传递给功能函数；

init_func：初始函数，用于执行初始化操作；

fargs：传递给功能函数的额外参数；

save_count：保存计数，默认为100；

interval：重复调用功能函数的间隔时间，单位为毫秒，默认为200；

repeat_delay：动画结束后，重复执行动画的间隔时间，单位为毫秒；

repeat：动画执行结束后，是否重复，默认为True；

blit：是否更新所有点，即更新所有点还是仅更新变化的点，默认为False；

cache_frame_data：是否缓存数据，默认为True； 
'''