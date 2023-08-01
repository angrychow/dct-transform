# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import binascii


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# 读取 UTF-8 编码的文件
# with open("word.txt", "r", encoding="utf-8") as f:
#     content = f.read()
content = "蒲俊松"

# 将文件内容转换为八位二进制数
# binary_str = binascii.hexlify(content.encode("utf-8")).decode("utf-8")
byte_array = bytearray(content, "utf-8")

# 将二进制数保存到新文件中
with open("binary.txt", "wb") as f:
    f.write(byte_array)
print(len(byte_array))

# utf8_str =