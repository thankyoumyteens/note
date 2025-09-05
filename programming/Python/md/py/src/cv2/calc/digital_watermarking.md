# 数字水印

数字水印（Digital Watermarking）是一种隐藏在数字内容（如图像、音频、视频、文档）中的不可见（或低可见性）信息，核心作用是实现对数字内容的版权保护、来源追踪、完整性验证或内容标注，且不影响原始内容的正常使用和感知质量。

将一个需要隐藏的二值图像信息嵌入载体图像(能够隐藏其他图像的图像)的最低有效位，即将载体图像的 bit0 位平面替换为当前需要隐藏的二值图像，从而实现将二值图像隐藏的目的。由于二值图像处于载体图像的最低有效位上，所以嵌入二值图像对于载体图像的影响非常小，其具有较高的隐蔽性。在必要时直接将载体图像的最低有效位层提取出来，即可得到嵌入在该位上的二值图像，达到提取秘密信息的目的。

## 嵌入水印

1. 创建一个和载体图像大小相同的提取矩阵, 矩阵中的每个元素的值均为 254(11111110)
2. 将载体图像与提取矩阵进行按位与运算, 将载体图像内所有像素的高七位保留、最低位清零
3. 将水印图像(二值图像)中的像素值为 255 的都转换为像素值 1，以方便嵌入载体图像
4. 将载体图像与水印图像进行按位或运算，把水印信息嵌入载体图像内

```py
# 以灰度图为例
img = cv2.imread('a.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
height, width = gray.shape
# 创建一个和载体图像大小相同的提取矩阵
matrix = np.zeros((height, width), dtype=np.uint8)
# 矩阵中的每个元素的值均为 254
matrix[:, :] = 254
# 将载体图像内所有像素的高七位保留、最低位清零
gray = cv2.bitwise_and(gray, matrix)
# 获取水印图像
watermark_img = get_watermark('hello world', height, width)
# 把水印信息嵌入载体图像内
result = cv2.bitwise_or(gray, watermark_img)

cv2.imshow('result', result)
cv2.waitKey(0)
```

## 提取水印

1. 创建一个和载体图像大小相同的提取矩阵, 矩阵中的每个元素的值均为 1(00000001)
2. 将载体图像与提取矩阵进行按位与运算, 将载体图像内所有像素的高七位清零、最低位保留
3. 此时得到的图像就是水印图像(二值图像)

```py
# 创建一个和载体图像大小相同, 且所有值都是 0b00000001 的提取矩阵
extract_matrix = np.full((height, width), 1, dtype=np.uint8)
# 提取水印
extracted = cv2.bitwise_and(result, extract_matrix)
print(parse_watermark(extracted))
```

## 完整代码

```py
import cv2
import numpy as np


# 字符串转二进制表示的字节数组
# 示例: "Hello World" -> ['01001000', '01100101', '01101100', ...]
def str_to_byte_array(input_str: str) -> list[str]:
    byte_arr: list[str] = []
    encoded_str = input_str.encode('utf-8')
    for byte_val in encoded_str:
        # bin(byte_val)[2:]的说明:
        # bin(byte_val) 得到的是0b1010..., 需要把0b去掉
        bits_val = bin(byte_val)[2:].zfill(8)
        byte_arr.append(bits_val)
    return byte_arr


# 二进制表示的字节数组转比特数组
# 示例: ['01001000', '01100101', '01101100', ...] -> [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, ...]
def byte_array_to_bit_array(byte_arr: list[str]) -> list[int]:
    result_arr: list[int] = []
    for byte_val in byte_arr:
        result_arr.extend([int(bit_val) for bit_val in byte_val])
    return result_arr


# 字符串转比特数组
# 示例: "Hello World" -> [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, ...]
def str_to_bit_array(input_str: str) -> list[int]:
    byte_arr = str_to_byte_array(input_str)
    bit_arr = byte_array_to_bit_array(byte_arr)
    return bit_arr


# 把比特数组转为numpy的二维数组
# 数据格式: 有效数据的长度(16位) + 数据 + 补0
def bit_array_to_matrix(bit_array: list[int], row_count: int, col_count: int) -> np.ndarray:
    count = row_count * col_count
    arr_len = len(bit_array)
    # 有效数据的长度
    arr_len_binary = bin(arr_len)[2:].zfill(16)
    target_arr = []
    target_arr.extend([int(bit_val) for bit_val in arr_len_binary])
    arr_len += len(target_arr)
    if arr_len > count:
        raise Exception('bit_array is too long')
    padding_bit_count = count - arr_len
    target_arr.extend(bit_array)
    # 补0
    target_arr.extend([0] * padding_bit_count)
    # 把数组转成np一维数组
    np_arr = np.array(target_arr, dtype=np.uint8)
    # 把一维数组转成二维数组
    np_arr = np_arr.reshape((row_count, col_count))
    return np_arr


# 字符串转水印图像
def get_watermark(input_text: str, height: int, width: int) -> np.ndarray:
    bit_arr = str_to_bit_array(input_text)
    np_arr = bit_array_to_matrix(bit_arr, height, width)
    return np_arr


# 比特数组转二进制表示的字节数组
# 示例: [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, ...] -> ['01001000', '01100101', '01101100', ...]
def bit_array_to_byte_array(bit_arr: list[int]) -> list[str]:
    byte_arr: list[str] = []
    counter = 0
    byte_val = ''
    for bit_val in bit_arr:
        byte_val += str(bit_val)
        counter += 1
        if counter == 8:
            byte_arr.append(byte_val)
            counter = 0
            byte_val = ''
    return byte_arr


# 二进制表示的字节数组转字符串
# 示例: ['01001000', '01100101', '01101100', ...] -> "Hello World"
def byte_array_to_str(byte_arr: list[str]) -> str:
    bytes_val = b''
    for bits_val in byte_arr:
        int_val_from_bits = int(bits_val, 2)
        byte_val = int_val_from_bits.to_bytes(1)
        bytes_val += byte_val
    result_str = bytes_val.decode('utf-8')
    return result_str


# 解析二值图像水印
def parse_watermark(matrix: np.ndarray) -> str:
    bit_arr = matrix.flatten().tolist()
    # 取出记录数据长度的前16位
    msg_len = '0b' + ''.join([str(i) for i in bit_arr[:16]])
    msg_len = int(msg_len, base=2)
    # 去掉数据长度部分
    bit_arr = bit_arr[16:]
    # 去掉补的0, 取出实际的数据部分
    bit_arr = bit_arr[:msg_len]
    byte_arr = bit_array_to_byte_array(bit_arr)
    msg = byte_array_to_str(byte_arr)
    return msg


if __name__ == '__main__':
    img = cv2.imread('a.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    # 创建一个和载体图像大小相同的提取矩阵
    matrix = np.zeros((height, width), dtype=np.uint8)
    # 矩阵中的每个元素的值均为 254
    matrix[:, :] = 254
    # 将载体图像内所有像素的高七位保留、最低位清零
    gray = cv2.bitwise_and(gray, matrix)
    # 获取水印图像, 水印是: hello world
    watermark_img = get_watermark('hello world', height, width)
    # 把水印信息嵌入载体图像内
    result = cv2.bitwise_or(gray, watermark_img)

    # 创建一个和载体图像大小相同, 且所有值都是 00000001 的提取矩阵
    extract_matrix = np.full((height, width), 1, dtype=np.uint8)
    # 提取水印
    extracted = cv2.bitwise_and(result, extract_matrix)
    # 解析水印
    print(parse_watermark(extracted))
```
