# 字节码指令

## aaload

- 操作: 从数组中加载一个 reference 类型数据到操作数栈
- 操作码: aaload
- 操作数: 无
- 操作数栈-执行前: arrayref, index
- 操作数栈-执行后: value
- 说明: 取出数组 arrayref 中索引为 index 的值
- 详细说明: arrayref 必须是一个 reference 的数据，它指向一个组件类型为 reference 的数组(可以理解为指向数组的指针)，index 必须为 int 类型。指令执行后，arrayref 和 index 同时从操作数栈中出栈，index 作为索引定位到数组中的值, 并将其压入到操作数栈中

## aastore

- 操作: 从操作数栈读取一个 reference 类型数据存入到数组中
- 操作码: aastore
- 操作数: 无
- 操作数栈-执行前: arrayref，index，value
- 操作数栈-执行后: 无
- 说明: 把数组 arrayref 中索引为 index 的值设置为 value
- 详细说明: arrayref 必须是一个 reference 类型的数据，它指向一个组件类型为 reference 的数组，index 必须为 int 类型，value 必须为 reference 类型。指令执行后，arrayref、index 和 value 同时从操作数栈出栈，value 存储到 index 作为索引定位到的数组元素中

## aconst_null
- 操作: 从操作数栈读取一个 reference 类型数据存入到数组中
- 操作码: aastore
- 操作数: 无
- 操作数栈-执行前: arrayref，index，value
- 操作数栈-执行后: 无
- 说明: 把数组 arrayref 中索引为 index 的值设置为 value
- 详细说明: arrayref 必须是一个 reference 类型的数据，它指向一个组件类型为 reference 的数组，index 必须为 int 类型，value 必须为 reference 类型。指令执行后，arrayref、index 和 value 同时从操作数栈出栈，value 存储到 index 作为索引定位到的数组元素中