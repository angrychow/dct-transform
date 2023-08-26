# 隐写程序使用说明

## 两点法 two_point.exe

在当前目录下使用命令行启动，具体格式如下:

```powershell
./two_point [-h][-i][-m][-o] {encode,decode,t2e,min_t}
```

|  参数   |                    说明                    |   默认值   |
| :-----: | :----------------------------------------: | :--------: |
|   -h    |             Help 查看参数说明              |     ——     |
|   -i    |         Input Image 输入图片的路径         | image.jpg  |
|   -o    |     Output Image 图片隐写后的输出路径      | output.jpg |
|   -m    | Message 隐写信息文件的路径，用于输入和输出 |  word.txt  |
| operate |               希望执行的操作               |   encode   |

### 操作的具体说明

- encode 将Message文件中的文本以UTF-8编码隐写入Input image对应的图片，使用者可以自行指定选点和阈值，并将结果图片输出到 Output image路径。
- decode 将Input image图片认为是隐写后图片，在用户给出选点和阈值后尝试解码。由于使用哈夫曼编码压缩信息，若字典部分损坏则输出一个报错，结果为空；否则将解码后的信息输出到Message文件。
- t2e 操作是debug功能：在选定一组点后,输出这组点在隐写时，使用的阈值和误码率的关系，输出到data.txt。
- min_t 是debug功能：给出在一个点确定的情况下，任意取其他点，可以达到0误码隐写所需要的最小阈值，并输出到data.txt。



## 比特高频直写法

在当前目录下使用命令行启动：

```powershell
./steganography [-h][-i][-m][-o] {encode,decode}
```

|  参数   |                    说明                    |   默认值   |
| :-----: | :----------------------------------------: | :--------: |
|   -h    |             Help 查看参数说明              |     ——     |
|   -i    |         Input Image 输入图片的路径         | image.jpg  |
|   -o    |     Output Image 图片隐写后的输出路径      | output.jpg |
|   -m    | Message 隐写信息文件的路径，用于输入和输出 |  word.txt  |
| operate |               希望执行的操作               |   encode   |

### 操作的具体说明

- encode 将Message文件中的文本以UTF-8编码隐写入Input image对应的图片，并将结果图片输出到 Output image路径。
- decode 将Input image图片以隐写图片看待进行解码。由于使用哈夫曼编码压缩信息，若字典部分损坏则输出一个报错，结果为空；否则将解码后的信息输出到Message文件。