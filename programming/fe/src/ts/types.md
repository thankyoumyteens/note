# 数据类型

| 类型        | 描述                                                                 |
| ----------- | -------------------------------------------------------------------- |
| `boolean`   | 可以是 `true` 或 `false`。                                           |
| `number`    | 整数和浮点数类型。                                                   |
| `string`    | 字符串类型。                                                         |
| `array`     | 数组类型。例如：`number[]` 或 `Array<number>`。                      |
| `tuple`     | 表示已知元素数量和类型的数组。例如：`[string, number]`。             |
| `enum`      | 枚举类型是一种特殊的值类型, 用于定义数值或字符串的集合。             |
| `any`       | 可以表示任何类型。通常在不确定类型或者不想限制类型时使用。           |
| `void`      | 用来标识没有返回值的函数。                                           |
| `null`      | 表示没有任何对象值。                                                 |
| `undefined` | 表示未初始化(未赋值)的变量。                                       |
| `never`     | 表示那些永远不会发生的情况的返回类型。                               |
| `object`    | 对象类型。                                                           |
| `unknown`   | 类似于 `any`, 但是更安全。必须经过类型断言或检查才能执行大多数操作。 |

注意：`null` 和 `undefined` 在 TypeScript 中是所有其他类型的子类型。这意味着你可以把 `null` 和 `undefined` 赋给任何类型的变量, 除非你启用了严格模式 (`--strictNullChecks`), 在这种情况下, 你需要显式处理 `null` 和 `undefined`。

此外, TypeScript 还支持联合类型(Union Types)和交叉类型(Intersection Types), 允许你创建更复杂的类型结构。例如：

- `string | number` 表示这个变量既可以是 `string` 也可以是 `number`
- `type Person = { name: string } & { age: number }` 创建了一个同时具有 `name` 和 `age` 属性的对象类型
