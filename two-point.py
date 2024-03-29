from scipy.fftpack import dct, idct

from PIL import Image
import numpy as np


#point selection
Point_1 = (6,5)
Point_2 = (5,4)
Point_3 = (5,2)

threshold = 55

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
    secret_bytes = secret_message.encode('utf-8')
    secret_bits = ''.join(format(byte, '08b') for byte in secret_bytes)
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
    secret_bytes = []
    for i in range(0, len(secret_bits), 8):
        secret_bytes.append(int(secret_bits[i:i+8], 2))
    secret_message = bytes(secret_bytes).decode('utf-8', errors='ignore')
    return secret_message[0:secret_message.find(special_char)]

def cal_err_rate(origin, new, len):
    err_cnt = 0
    for i in range(len):
        if(origin[i] != new[i]):
            err_cnt += 1
    return err_cnt/len


# 加载原始 JPEG 图像
img = Image.open('test.jpg').convert('YCbCr')
# 加载隐写内容
with open("word.txt", "r", encoding="utf-8") as f:
    secret_message = f.read()
# 保存输出 JPEG 图像
out_img = encodeImg(img, secret_message)
out_img.save('output.jpg')



# 加载编码后 JPED 图像
encoded_image = Image.open('output.jpg').convert('YCbCr')
msg = decodeImg(encoded_image)
print(msg)
#write to decode.txt
with open("decode.txt", "w", encoding="utf-8") as f:
    f.write(msg)

print('error rate :', cal_err_rate(bits_a, bits_b, len(bits_a)))













# from difflib import SequenceMatcher

# def find_string_diff(str1, str2):
#     matcher = SequenceMatcher(None, str1, str2)
#     for opcode, start1, end1, start2, end2 in matcher.get_opcodes():
#         if opcode == 'equal':
#             print("相同: ", str1[start1:end1])
#         elif opcode == 'insert':
#             print("插入: ", str2[start2:end2])
#         elif opcode == 'delete':
#             print("删除: ", str1[start1:end1])
#         elif opcode == 'replace':
#             print("替换: ", str1[start1:end1], " -> ", str2[start2:end2])

# 示例用法
# find_string_diff(bits_a, bits_b)
