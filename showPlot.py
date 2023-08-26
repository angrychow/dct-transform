import numpy as np
import re
import matplotlib.pyplot as plt

#懒得改了，就这样
def plot_3d(filename):
    with open(filename, 'r') as fp:
        content = fp.read()
    numbers = re.findall('\d+', content)
    length = len(numbers)
    i = 0
    Data = []
    x = []
    y = []
    z = []
    while(i < length):
            array = []
            array.append(int(numbers[i]))
            array.append(int(numbers[i+1]))
            array.append(int(numbers[i+2]))
            Data.append(array)
            x.append(int(numbers[i]))
            y.append(int(numbers[i+1]))
            z.append(int(numbers[i+2]))
            i+=3


    # 绘制3D图
    ax = plt.axes(projection='3d')
    ax.plot3D(x, y, z, 'b.')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def plot_2d(filename):
        with open(filename, 'r') as fp:
                content = fp.read()
                numbers = re.findall(r"\d+\.\d+|\d+", content)
        length = len(numbers)
        i = 0
        x = []
        y = []
        while(i < length):
                x.append(float(numbers[i]))
                y.append(float(numbers[i+1]))
                i+=2
        plt.scatter(x,y)
        plt.show()