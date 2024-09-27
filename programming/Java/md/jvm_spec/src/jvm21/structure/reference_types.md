# 引用类型

有三种 `reference` 类型: class 类型, array 类型, 和 interface 类型. 它的值引用的是动态创建的类实例, 数组, 或者实现了某些接口的类实例或数组。

一个数组类型由一个单一维度的 _组件类型(component type)_ 组成 (whose length is not given by the type). 一个数组类型的组件类型本身可能也是数组类型。如果，从任何数组类型开始, one considers its component type, and then
(if that is also an array type) the component type of that type, and so on, 最终
one must reach a component type that is not an array type; this is called the _element
type_ of the array type. The element type of an array type is necessarily either a
primitive type, or a class type, or an interface type. (如三维数组 `int[][][]` 的组件类型为 `int[][]`, 二维数组 `int[][]` 的组件类型为 `int[]`, 一维数组 `int[]` 的组件类型是 `int`。)

A `reference` value may also be the special null reference, a reference to no object,
which will be denoted here by `null`. The `null` reference initially has no run-time
type, but may be cast to any type. The default value of a `reference` type is `null`.

This specification does not mandate a concrete value encoding `null`.
