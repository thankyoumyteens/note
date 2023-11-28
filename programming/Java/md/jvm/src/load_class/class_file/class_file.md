# 类文件结构

class 文件格式采用一种类似于 C 语言结构体的伪结构来存储数据, 这种伪结构中只有两种数据类型: 无符号数和表。

- 无符号数属于基本的数据类型, 以 u1、u2、u4、u8 来分别代表 1 个字节、2 个字节、4 个字节和 8 个字节的无符号数, 无符号数可以用来描述数字、索引引用、数量值或者按照 UTF-8 编码构成字符串值
- 表是由多个无符号数或者其他表作为数据项构成的复合数据类型, 为了便于区分, 所有表的命名都习惯性地以\_info 结尾。表用于描述有层次关系的复合结构的数据, 整个 Class 文件本质上也可以视作是一张表

## Class 文件结构

| 类型           | 名称                | 说明         | 长度     |
| -------------- | ------------------- | ------------ | -------- |
| u4             | magic               | 魔数         | 4 个字节 |
| u2             | minor_version       | 副版本号     | 2 个字节 |
| u2             | major_version       | 主版本号     | 2 个字节 |
| u2             | constant_pool_count | 常量池容量   | 2 个字节 |
| cp_info        | constant_pool       | 常量池       | n 个字节 |
| u2             | access_flags        | 访问标志     | 2 个字节 |
| u2             | this_class          | 类索引       | 2 个字节 |
| u2             | super_class         | 父类索引     | 2 个字节 |
| u2             | interfaces_count    | 接口个数     | 2 个字节 |
| u2             | interfaces          | 接口索引集合 | n 个字节 |
| u2             | fields_count        | 字段个数     | 2 个字节 |
| field_info     | fields              | 字段集合     | n 个字节 |
| u2             | methods_count       | 方法个数     | 2 个字节 |
| method_info    | methods             | 方法集合     | n 个字节 |
| u2             | attributes_count    | 附加属性个数 | 2 个字节 |
| attribute_info | attributes          | 附加属性集合 | n 个字节 |
