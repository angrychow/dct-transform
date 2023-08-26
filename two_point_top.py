import argparse
import two_point as tp
from PIL import Image
from showPlot import plot_2d, plot_3d
argparser = argparse.ArgumentParser("two_point_top")
argparser.add_argument('mode', choices=['encode', 'decode','t2e', 'min_t'], type = str, help = 'encode or decode', default='encode')
argparser.add_argument('-i', '--image', help = 'image path', type = str, default='image.jpg')
argparser.add_argument('-m', '--message', help = 'message path', type = str,default='word.txt')
argparser.add_argument('-o', '--output', help = 'output path', default='output.jpg', type = str)

args = argparser.parse_args()
if(args.mode == 'encode'):
    if(input('Use default point set? (y/n)') == 'y'):
        tp.Point_1 = (1,4)
        tp.Point_2 = (4,1)
        tp.threshold = 15
    else:
        tp.Point_1 = eval(input("Point_1:"))
        tp.Point_2 = eval(input("Point_2:"))
        tp.threshold = int(input("threshold:"))
    img = Image.open(args.image).convert('YCbCr')
    with open(args.message, "r", encoding="utf-8") as f:
        secret_message = f.read()
    out_img = tp.encodeImg(img, secret_message)
    out_img.save(args.output)
    print("Done!")
elif (args.mode == 'decode'):
    if(input('Use default point set? (y/n)') == 'y'):
        tp.Point_1 = (1,4)
        tp.Point_2 = (4,1)
        tp.threshold = 15
    else:
        tp.Point_1 = eval(input("Point_1:"))
        tp.Point_2 = eval(input("Point_2:"))
        tp.threshold = int(input("threshold:"))
    img = Image.open(args.image).convert('YCbCr')
    encoded_image = Image.open(args.image).convert('YCbCr')
    msg = tp.decodeImg(encoded_image)
    print(msg)
    with open(args.message, "w", encoding="utf-8") as f:
        f.write(msg)
    print("Done!")
elif(args.mode == 't2e'):
    tp.Point_1 = eval(input("Point_1:"))
    tp.Point_2 = eval(input("Point_2:"))
    img = Image.open(args.image).convert('YCbCr')
    with open(args.message, "r", encoding="utf-8") as f:
        secret_message = f.read()
    tp.findErrRate(secret_message, img)
    plot_2d('./data.txt')
    print("Done!")
else:
    img = Image.open(args.image).convert('YCbCr')
    with open(args.message, "r", encoding="utf-8") as f:
        secret_message = f.read()
    tp.findMinThresholdWithPointSet(secret_message, img)
    plot_3d('./data.txt')
    print("Done!")
