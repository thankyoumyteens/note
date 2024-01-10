# class 文件结构

| 类型           | 名称                | 说明               |
| -------------- | ------------------- | ------------------ |
| u4             | magic               | 魔数               |
| u2             | minor_version       | 副版本号           |
| u2             | major_version       | 主版本号           |
| u2             | constant_pool_count | 常量池中常量的个数 |
| cp_info        | constant_pool       | 常量池             |
| u2             | access_flags        | 访问标志           |
| u2             | this_class          | 类索引             |
| u2             | super_class         | 父类索引           |
| u2             | interfaces_count    | 接口个数           |
| u2             | interfaces          | 接口索引集合       |
| u2             | fields_count        | 字段个数           |
| field_info     | fields              | 字段集合           |
| u2             | methods_count       | 方法个数           |
| method_info    | methods             | 方法集合           |
| u2             | attributes_count    | 附加属性个数       |
| attribute_info | attributes          | 附加属性集合       |

class 文件中定义了两种数据类型:

1. u1、u2、u4、u8 分别代表 1 个字节、2 个字节、4 个字节和 8 个字节的无符号数
2. 以 \_info 结尾的类型称为表。表是由多个无符号数或者其他表构成的复合类型, 整个 class 文件也可以视作是一张表
