from scipy.fftpack import dct, idct
from huffman import *
from PIL import Image
import numpy as np

# Point_1 = (1,0)
# Point_2 = (0,1)

#point set 0
Point_1 = (1,4)
Point_2 = (4,1)


#point set 1
# Point_1 = (3,3)
# Point_2 = (6,6)

#point set 2
# Point_1 = (4,7)
# Point_2 = (7,4)

#point set 3
# Point_1 = (5,6)
# Point_2 = (6,5)

threshold = 20

_ = bytearray()
_.append(0)
special_char = _.decode("utf-8")

# implement 2D DCT
def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')

# implement 2D IDCT
def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')

# 编码函数
def encodeImg(img, secret_message, method = 'two-point'):

    # 将 JPEG 图像转换为 YCbCr 颜色空间
    y, cb, cr = img.split()

    # 将 Y 分量转换为 numpy 数组
    y_array = np.array(y, dtype=np.float32)

    # 进行 DCT 变换
    dct_array = np.zeros_like(y_array)
    for i in range(0, y_array.shape[0], 8):
        for j in range(0, y_array.shape[1], 8):
            dct_array[i:i+8, j:j+8] = dct2(y_array[i:i+8, j:j+8])

    # 在 DCT 系数中嵌入信息
    secret_message = secret_message + special_char
    secret_bits = msg_to_bits(secret_message)
    global bits_a
    bits_a = secret_bits

    for i in range(0, dct_array.shape[0], 8):
        for j in range(0, dct_array.shape[1], 8):
            if len(secret_bits) == 0:
                break
            block = np.round(dct_array[i:i+8, j:j+8])
            #chose different encode with different method
            if(method == 'two-point'):
                if(abs(block[Point_1] - block[Point_2]) < threshold):
                    if(block[Point_1] < block[Point_2]):
                        block[Point_2] += threshold - abs(block[Point_1] - block[Point_2])
                    else:
                        block[Point_1] += threshold - abs(block[Point_1] - block[Point_2])
                if((secret_bits[0] == '1') ^ (block[Point_1] > block[Point_2])):
                    #switch Point_1 and Point_3
                    temp = block[Point_1]
                    block[Point_1] = block[Point_2]
                    block[Point_2] = temp


            dct_array[i:i+8, j:j+8] = block
            secret_bits = secret_bits[1:]
    # 进行 IDCT 反变换
    for i in range(0, y_array.shape[0], 8):
        for j in range(0, y_array.shape[1], 8):
            y_array[i:i+8, j:j+8] = idct2(dct_array[i:i+8, j:j+8])

    # 将 YCbCr 图像合并为 JPEG 图像
    y = Image.fromarray(np.uint8(np.clip(y_array, 0, 255)), mode='L')
    cb = Image.fromarray(np.array(cb), mode='L')
    cr = Image.fromarray(np.array(cr), mode='L')
    out_img = Image.merge('YCbCr', (y, cb, cr))
    return out_img


def decodeImg(img, method = 'two-point'):
    global bits_b
     # 将 JPEG 图像转换为 YCbCr 颜色空间
    y, cb, cr = img.split()

    # 将 Y 分量转换为 numpy 数组
    y_array = np.array(y, dtype=np.float32)

    # 进行 DCT 变换
    dct_array = np.zeros_like(y_array)
    for i in range(0, y_array.shape[0], 8):
        for j in range(0, y_array.shape[1], 8):
            dct_array[i:i+8, j:j+8] = dct2(y_array[i:i+8, j:j+8])
    # 解码隐写内容
    secret_bits = ''
    for i in range(0, dct_array.shape[0], 8):
        for j in range(0, dct_array.shape[1], 8):
            block = (dct_array[i:i+8, j:j+8])
            if dct_array.shape[0] - i < 8 or dct_array.shape[1] - j < 8:
                break
            #chose different encode with different method
            if(method == 'two-point'):
                if(block[Point_1] > block[Point_2]):
                    secret_bits += '1'
                else:
                    secret_bits += '0'
    # 将二进制字符串转换为字节字符串
    bits_b = secret_bits
    secret_message = bits_to_msg(secret_bits)
    return secret_message[0:secret_message.find(special_char)]

def cal_err_rate(origin, new, len):
    err_cnt = 0
    for i in range(len):
        if(origin[i] != new[i]):
            err_cnt += 1
    return err_cnt/len

#二分递归，找出当前点集下,经过encodeImage和decodeImage后,误码为0时最小的threshold，最小分度为1
def findMinThreshold(secret_message, img, l, r)->int:
    if(l == r):
        return l
    mid = (l + r) // 2
    global threshold
    threshold = mid
    out_img = encodeImg(img, secret_message)
    out_img.save('output.jpg')
    encoded_image = Image.open('output.jpg').convert('YCbCr')
    msg = decodeImg(encoded_image)
    if(cal_err_rate(bits_a, bits_b, min(len(bits_a),len(bits_b))) == 0):
        return findMinThreshold(secret_message, img, l, mid)
    else:
        return findMinThreshold(secret_message, img, mid + 1, r)

# 给出threshold在（0,100）分度为1下，编码解码后的误码率，以(threshold, err_rate)换行的形式print

def findErrRate(secret_message, img):
    global threshold
    with open("data.txt", "w", encoding = "utf-8") as f:
        for i in range(0, 100):
            threshold = i
            out_img = encodeImg(img, secret_message)
            out_img.save('output.jpg')
            encoded_image = Image.open('output.jpg').convert('YCbCr')
            msg = decodeImg(encoded_image)
            f.write("{"+str(i)+","+str(cal_err_rate(bits_a, bits_b, min(len(bits_a),len(bits_b))))+"},")


#穷举每一个点做固定点,另一点任意，找出固定点下，与某一个任一点组成点集后，可以编码解码误码率为零的最小阈值
def findMinThresholdWithPoint(secret_message, img, point)->int:
    global Point_1
    Point_1 = point
    min_threshold = 100
    for i in range(0, 8):
        for j in range(0, 8):
            if((i == point[0] and j == point[1]) or i == j == 0 ):
                continue
            global Point_2
            Point_2 = (i,j)
            print(Point_2)
            threshold = findMinThreshold(secret_message, img, 0, 100)
            if(threshold < min_threshold):
                min_threshold = threshold
    return min_threshold

#使用上述方法，穷举固定点，打印出最小阈值与固定点的关系，以{x,y,threshold},换行的形式打印到当前目录下data.txt
def findMinThresholdWithPointSet(secret_message, img):
    with open("data.txt", "w", encoding = "utf-8") as f:
        for i in range(0, 8):
            for j in range(0, 8):
                if(i == 0 and j == 0):
                    continue
                f.write("{"+str(i)+","+str(j)+","+str(findMinThresholdWithPoint(secret_message, img, (i,j)))+"},")

# # 加载原始 JPEG 图像
# img = Image.open('image.jpg').convert('YCbCr')
# # 加载隐写内容
# with open("word.txt", "r", encoding="utf-8") as f:
#     secret_message = f.read()
# # 保存输出 JPEG 图像
# out_img = encodeImg(img, secret_message)
# out_img.save('output.jpg')
# findErrRate(secret_message, img)

# findMinThresholdWithPointSet(secret_message, img)

# # 加载编码后 JPED 图像
# encoded_image = Image.open('output.jpg').convert('YCbCr')
# # encoded_image = out_img
# msg = decodeImg(encoded_image)
# print(msg)
# #write to decode.txt
# with open("decode.txt", "w", encoding="utf-8") as f:
#     f.write(msg)
# print(len(bits_b))
# print('error rate :', cal_err_rate(bits_a, bits_b, len(bits_a)))


