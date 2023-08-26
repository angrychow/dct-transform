from dct_transform import encodeImg
from decode_dct_transform import decodeImg
from PIL import Image
import argparse


argparser = argparse.ArgumentParser("new_top")
argparser.add_argument('mode', choices=['encode', 'decode'], type = str, help = 'encode or decode', default='encode')
argparser.add_argument('-i', '--image', help = 'input image path', type = str, default='image.jpg')
argparser.add_argument('-m', '--message', help = 'message path', type = str,default='word.txt')
argparser.add_argument('-o', '--output', help = 'output image path', default='output.jpg', type = str)

args = argparser.parse_args()

if(args.mode == 'encode'):
    img = Image.open(args.image).convert('YCbCr')
    with open(args.message, "r", encoding="utf-8") as f:
        secret_message = f.read()
    out_img = encodeImg(img, secret_message)
    out_img.save(args.output)
    print("Done!")
else:
    encoded_image = Image.open(args.image).convert('YCbCr')
    msg = decodeImg(encoded_image)
    print(msg)
    with open(args.message, "w", encoding="utf-8") as f:
        f.write(msg)
    print("Done!")