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


def encodeImg(img, secret_message):

    # 加载原始 JPEG 图像
    # img = Image.open('image.jpg').convert('YCbCr')

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
    _ = bytearray()
    _.append(0)
    special_char = _.decode("utf-8")

    # with open("word.txt", "r", encoding="utf-8") as f:
    #     secret_message = f.read() + special_char

    secret_bytes = secret_message.encode('utf-8')
    secret_bits = ''.join(format(byte, '08b') for byte in secret_bytes)
    # secret_bits = msg_to_bits(secret_message)
    # secret_bits += '0' * (8-(len(secret_bits) % 8))
    secret_bits = np.array(list(secret_bits), dtype=np.float32).reshape(-1, 8)
    # print(secret_bits.size)

    for i in range(0, dct_array.shape[0], 8):
        for j in range(0, dct_array.shape[1], 8):
            if len(secret_bits) == 0:
                break
            block = np.round(dct_array[i:i+8, j:j+8])
            if dct_array.shape[0] - i < 8 or dct_array.shape[1] - j < 8:
                break
            for t in range(6, 8):
                for k in range(4, 8):
                    block[k, t] = secret_bits[0, k-4+(t-6)*4]*100
            # print(block)
            dct_array[i:i+8, j:j+8] = block
            secret_bits = secret_bits[1:]

    # 进行 IDCT 反变换
    for i in range(0, y_array.shape[0], 8):
        for j in range(0, y_array.shape[1], 8):
            y_array[i:i+8, j:j+8] = idct2(dct_array[i:i+8, j:j+8])

    # print(y_array[0:8, 0:8])
    # 将 YCbCr 图像合并为 JPEG 图像
    y = Image.fromarray(np.uint8(np.clip(y_array, 0, 255)), mode='L')
    cb = Image.fromarray(np.array(cb), mode='L')
    cr = Image.fromarray(np.array(cr), mode='L')
    out_img = Image.merge('YCbCr', (y, cb, cr))

    # 保存输出 JPEG 图像
    return out_img