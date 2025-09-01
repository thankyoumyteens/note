# 图像加密和解密

通过按位异或运算可以实现图像的加密和解密。通过对原始图像与密钥图像进行按位异或，可以实现加密；将加密后的图像与密钥图像再次进行按位异或，可以实现解密。

异或运算（符号 ^ 或 XOR）的规则是：两个二进制位相同则结果为 0，不同则结果为 1。其最关键的特性是自反性：对于任意二进制值 a 和密钥 k，满足 (a ^ k) ^ k = a。即：用密钥 k 对数据 a 加密后（得到 a^k），再用同一密钥 k 对加密结果进行一次异或运算，就能还原出原始数据 a。

这一特性直接保证了加密和解密可以用同一套逻辑实现，仅需重复一次异或操作即可完成解密，非常适合图像加密。

```py
import cv2
import numpy as np

# 读取灰度图像
img = cv2.imread("a.png", 0)
height, width = img.shape

# 生成与图像同尺寸的随机密钥
key = np.random.randint(0, 256, size=(height, width), dtype=np.uint8)

# 加密：图像与密钥异或
encrypted = cv2.bitwise_xor(img, key)

# 解密：加密结果与密钥再次异或
decrypted = cv2.bitwise_xor(encrypted, key)

# 显示结果
cv2.imshow("Original", img)
cv2.imshow("Encrypted", encrypted)  # 加密后为杂乱无章的噪声图
cv2.imshow("Decrypted", decrypted)  # 解密后还原原始图像
cv2.waitKey(0)
```
