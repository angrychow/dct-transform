from scipy.fftpack import dct, idct
from huffman import *
from PIL import Image
import numpy as np

# implement 2D DCT
def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')

# implement 2D IDCT
def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')

def decodeImg(img):
    

    # 加载原始 JPEG 图像
    # img = Image.open('output.jpg').convert('YCbCr')

    # 将 JPEG 图像转换为 YCbCr 颜色空间
    y, cb, cr = img.split()

    # 将 Y 分量转换为 numpy 数组
    y_array = np.array(y, dtype=np.float32)
    # print(y_array[0:8, 0:8])

    # 进行 DCT 变换
    dct_array = np.zeros_like(y_array)
    for i in range(0, y_array.shape[0], 8):
        for j in range(0, y_array.shape[1], 8):
            dct_array[i:i+8, j:j+8] = dct2(y_array[i:i+8, j:j+8])


    # 在 DCT 系数中嵌入信息
    # secret_message = "Hello, world!"
    # secret_bytes = secret_message.encode('utf-8')
    # secret_bits = ''.join(format(byte, '08b') for byte in secret_bytes)
    # secret_bits += '0' * ((dct_array.size // 64) * 64 - len(secret_bits))
    # secret_bits = np.array(list(secret_bits), dtype=np.float32).reshape(-1, 8)
    # print(secret_bits.size)
    decode_bytes = bytearray()

    flag = False

    for i in range(0, dct_array.shape[0], 8):
        for j in range(0, dct_array.shape[1], 8):
            block = dct_array[i:i+8, j:j+8]
            # if i == 0 and j == 0:
            #     print(block)
            bytes_temp = ''
            # for k in range(0, 8):
            #     if 200 < block[0, -k-1] < 2000:
            #         bytes_temp += '1'
            #     else:
            #         bytes_temp += '0'
            if dct_array.shape[0] - i < 8 or dct_array.shape[1] - j < 8:
                break
            for t in range(6, 8):
                for k in range(4, 8):
                    if 30 < block[k ,t] < 170:
                        bytes_temp += '1'
                    else:
                        bytes_temp += '0'
            if flag:
                break
            decode_bytes.append(int(bytes_temp, 2))
        if flag:
            break

    secret_message = decode_bytes.decode("utf-8", errors='ignore')
    # print(secret_message)

    _ = bytearray()
    _.append(0)
    special_char = _.decode("utf-8")

    return secret_message[:secret_message.find(special_char)]

