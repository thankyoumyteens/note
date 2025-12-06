# ZIP64

传统 ZIP（也就是 PKZIP 的“ZIP32”）有几个关键限制(传统 ZIP 的关键字段只有 32 位):

- 单个文件大小最大：4GB - 1（即 0xFFFFFFFF 字节）
- 压缩数据起始偏移（相对文件开头）：最大 0xFFFFFFFF
- 归档内文件数：最大 65535（0xFFFF）

为了突破这些限制，就有了 ZIP64 扩展格式。

ZIP64 主要扩展了 3 项

1. ZIP64 Extra Field(Header 里的扩展字段), 出现在：
   - Local File Header
   - Central Directory File Header
2. ZIP64 End of Central Directory Record(ZIP64 的 EOCD 记录)
3. ZIP64 End of Central Directory Locator(指向 ZIP64 EOCD 的定位器)

## Local File Header 中的 ZIP64

传统 Local File Header 结构:

| 偏移量(offset) | 长度(字节) | 描述                                       |
| -------------- | ---------- | ------------------------------------------ |
| 0              | 4          | Local File Header 签名，固定值: 0x04034b50 |
| 4              | 2          | 提取本文件需要的最低版本号                 |
| 6              | 2          | 标志位                                     |
| 8              | 2          | 压缩方法                                   |
| 10             | 2          | 文件最后修改时间                           |
| 12             | 2          | 文件最后修改日期                           |
| 14             | 4          | 文件压缩前的 CRC-32                        |
| 18             | 4          | 文件压缩后的大小                           |
| 22             | 4          | 文件压缩前的大小                           |
| 26             | 2          | 文件名长度                                 |
| 28             | 2          | 扩展字段长度                               |
| 30             | n          | 文件名                                     |
| 30 + n         | m          | 扩展字段                                   |

ZIP64 Extra Field 位于偏移量 30+n 的扩展字段中。

如果 文件压缩后的大小/文件压缩前的大小 字段大于 4GB-1, 则对应的 32 位字段填 0xFFFFFFFF, 真正的 64 位值写入 ZIP64 Extra Field 中

加入 ZIP64 Extra Field 后的结构:

| 偏移量(offset) | 长度(字节) | 描述                                       |
| -------------- | ---------- | ------------------------------------------ |
| 0              | 4          | Local File Header 签名，固定值: 0x04034b50 |
| 4              | 2          | 提取本文件需要的最低版本号                 |
| 6              | 2          | 标志位                                     |
| 8              | 2          | 压缩方法                                   |
| 10             | 2          | 文件最后修改时间                           |
| 12             | 2          | 文件最后修改日期                           |
| 14             | 4          | 文件压缩前的 CRC-32                        |
| 18             | 4          | 文件压缩后的大小                           |
| 22             | 4          | 文件压缩前的大小                           |
| 26             | 2          | 文件名长度                                 |
| 28             | 2          | 扩展字段长度                               |
| 30             | n          | 文件名                                     |
| 30 + n         | 2          | ZIP64 Extra Field Header, 固定为: 0x0001   |
| 32 + n         | 2          | 后续 Extra Field 的长度                    |
| 34 + n         | 8          | 文件压缩前的大小, 8 个字节                 |
| 42 + n         | 8          | 文件压缩后的大小, 8 个字节                 |

## Central Directory File Header 中的 ZIP64

ZIP64 Extra Field 位于偏移量 46+n 的扩展字段中。

ZIP64 影响的字段有：

- 文件压缩后大小(偏移量 20)
- 文件压缩前大小(偏移量 24)
- 文件起始位置所在的磁盘编号(偏移量 34)
- 本目录指向的 Entry 相对于第一个 Entry 的起始位置(偏移量 42)

当这些字段超出原范围时：

- 将对应字段设为全 1（0xFFFFFFFF 或 0xFFFF）
- 真正的值放入 ZIP64 Extra Field（Header 也是 0x0001）

规则与 Local File Header 中的 ZIP64 一致。

## ZIP64 End of Central Directory Record

传统 EOCD 中所有的数值都受 16/32 位限制。当条目数、目录大小、偏移量等超出范围时，就必须引入 ZIP64 版本。

ZIP64 EOCD 结构:

| 偏移量(offset) | 长度(字节) | 描述                                                       |
| -------------- | ---------- | ---------------------------------------------------------- |
| 0              | 4          | ZIP64 EOCD 的签名，固定值: 0x06064b50                      |
| 4              | 8          | ZIP64 EOCD 的大小(不包含开头 4 字节签名本身)               |
| 12             | 2          | 使用哪个 ZIP 版本压缩的                                    |
| 14             | 2          | 提取本文件需要的最低版本号                                 |
| 16             | 4          | 占用磁盘数                                                 |
| 20             | 4          | 中央目录的起始位置所在的磁盘                               |
| 24             | 8          | 当前磁盘上的中央目录记录数                                 |
| 32             | 8          | 中央目录的总数量                                           |
| 40             | 8          | 中央目录的总大小                                           |
| 48             | 8          | 中央目录的起始位置相对于 ZIP 文件第一个 Entry 位置的偏移量 |
| 56             | n          | ZIP64 扩展数据扇区(可选，通常为 0 长度)                    |

## ZIP64 End of Central Directory Locator

为了让解压器从文件尾部快速找到 ZIP64 EOCD，需要有一个 Locator 结构。

ZIP64 EOCD Locator 通常位于 ZIP64 EOCD 和传统 EOCD 之间，格式:

| 偏移量(offset) | 长度(字节) | 描述                                          |
| -------------- | ---------- | --------------------------------------------- |
| 0              | 4          | ZIP64 EOCD Locator 的签名，固定值: 0x07064b50 |
| 4              | 4          | ZIP64 EOCD 起始位置的磁盘编号                 |
| 8              | 8          | ZIP64 EOCD 的相对偏移量                       |
| 16             | 4          | 占用磁盘数                                    |

## ZIP64 文件的典型布局

从文件尾往前:

1. EOCD（0x06054b50）
2. ZIP64 EOCD Locator（0x07064b50）
3. ZIP64 EOCD Record（0x06064b50）
4. …（前面是 Central Directory 和 Local Headers）

## ZIP64 文件的解析流程

1. 从文件尾向前扫描找到传统 EOCD（签名 0x06054b50）
2. 再往前尝试找 ZIP64 EOCD Locator（0x07064b50）
3. 如果找到 Locator：
   1. 用 Locator 中的 offset 定位到 ZIP64 EOCD
   2. 从 ZIP64 EOCD 中获取中心目录偏移、大小、条目数等
4. 如果找不到 Locator：
   1. 使用传统 EOCD 中的数据（说明没用 ZIP64，或没超出 4GB 的限制）
