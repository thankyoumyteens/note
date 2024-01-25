# 常量池中的 17 种数据类型的结构

| 常量                        | 项目                        | 类型 | 描述                                                                                                         |
| --------------------------- | --------------------------- | ---- | ------------------------------------------------------------------------------------------------------------ |
| CONSTANT_Utf8               | tag                         | u1   | 值为 1                                                                                                       |
| -                           | length                      | u2   | UTF-8 编码的字符串占用的字节数                                                                               |
| -                           | bytes                       | u1   | 长度为 length 的字符串                                                                                       |
| CONSTANT_Integer            | tag                         | u1   | 值为 3                                                                                                       |
| -                           | bytes                       | u4   | 按照高位在前存储的 int 值                                                                                    |
| CONSTANT_Float              | tag                         | u1   | 值为 4                                                                                                       |
| -                           | bytes                       | u4   | 按照高位在前存储的 float 值                                                                                  |
| CONSTANT_Long               | tag                         | u1   | 值为 5                                                                                                       |
| -                           | bytes                       | u8   | 按照高位在前存储的 long 值                                                                                   |
| CONSTANT_Double             | tag                         | u1   | 值为 6                                                                                                       |
| -                           | bytes                       | u8   | 按照高位在前存储的 double 值                                                                                 |
| CONSTANT_Class              | tag                         | u1   | 值为 7                                                                                                       |
| -                           | index                       | u2   | 指向全限定名常量项的索引                                                                                     |
| CONSTANT_String             | tag                         | u1   | 值为 8                                                                                                       |
| -                           | index                       | u2   | 指向字符串字面量的索引                                                                                       |
| CONSTANT_Fieldref           | tag                         | u1   | 值为 9                                                                                                       |
| -                           | index                       | u2   | 指向声明字段的类或者接口描述符 CONSTANT Class info 的索引项                                                  |
| -                           | index                       | u2   | 指向字段描述符 CONSTANT_NameAndType 的索引项                                                                 |
| CONSTANT_Methodref          | tag                         | u1   | 值为 10                                                                                                      |
| -                           | index                       | u2   | 指向声明方法的类描述符 CONSTANT_Class info 的索引项                                                          |
| -                           | index                       | u2   | 指向名称及类型描述符 CONSTANT_NameAndType 的索引项                                                           |
| CONSTANT_InterfaceMethodref | tag                         | u1   | 值为 11                                                                                                      |
| -                           | index                       | u2   | 指向声明方法的接口描述符 CONSTANT_Class info 的索引项                                                        |
| -                           | index                       | u2   | 指向名称及类型描述符 CONSTANT_NameAndType 的索引项                                                           |
| CONSTANT_NameAndType        | tag                         | u1   | 值为 12                                                                                                      |
| -                           | index                       | u2   | 指向该字段或方法名称常量项的索引                                                                             |
| -                           | index                       | u2   | 指向该字段或方法描述符常量项的索引                                                                           |
| CONSTANT_MethodHandle       | tag                         | u1   | 值为 15                                                                                                      |
| -                           | reference_kind              | u1   | 值必须在 1 至 9 之间(包括 1 和 9), 它决定了方法句柄的类型。方法句柄类型的值表示方法句柄的字节码行为          |
| -                           | reference_index             | u2   | 值必须是对常量池的有效索引                                                                                   |
| CONSTANT_MethodType         | tag                         | u1   | 值为 16                                                                                                      |
| -                           | descriptor_index            | u2   | 值必须是对常量池的有效索引, 常量池在该索引处的项必须是 CONSTANT_Utf8 结构, 表示方法的描述符                  |
| CONSTANT_Dynamic            | tag                         | u1   | 值为 17                                                                                                      |
| -                           | bootstrap_method_attr_index | u2   | 值必须是对当前 Class 文件中引导方法表的 bootstrap_methods[]数组的有效索引                                    |
| -                           | name_and_type_index         | u2   | 值必须是对当前常量池的有效索引, 常量池在该索引处的项必须是 CONSTANT_NameAndType 结构, 表示方法名和方法描述符 |
| CONSTANT_InvokeDynamic      | tag                         | u1   | 值为 18                                                                                                      |
| -                           | bootstrap_method_attr_index | u2   | 值必须是对当前 Class 文件中引导方法表的 bootstrap_methods[]数组的有效索引                                    |
| -                           | name_and_type_index         | u2   | 值必须是对当前常量池的有效索引, 常量池在该索引处的项必须是 CONSTANT_NameAndType 结构, 表示方法名和方法描述符 |
| CONSTANT_Module             | tag                         | u1   | 值为 19                                                                                                      |
| -                           | name_index                  | u2   | 值必须是对当前常量池的有效索引, 常量池在该索引处的项必须是 CONSTANT_Utf8 结构, 表示模块名字                  |
| CONSTANT_Package            | tag                         | u1   | 值为 20                                                                                                      |
| -                           | name_index                  | u2   | 值必须是对当前常量池的有效索引, 常量池在该索引处的项必须是 CONSTANT_Utf8 结构, 表示包名称                    |
