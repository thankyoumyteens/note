# 定义

splice() 会直接对数组进行修改

```js
array.splice(index,howmany,item1...)
```

- index: 从何处添加/删除元素
- howmany: 要删除几个元素, 不传则删除从index开始到数组结尾的所有元素。
- item1...: 要插入到数组的新元素

# 插入

```js
var colors = ["red", "green", "blue"]
// 从索引1开始插入两项: ["red", "yellow", "orange", "green", "blue"]
colors.splice(1, 0, "yellow", "orange")
```

# 删除

```js
var colors = ["red", "green", "blue"]
// 删除第一项: ["green", "blue"]
colors.splice(0, 1)
```

# 替换


```js
var colors = ["red", "green", "blue"]
// 索引2的元素替换成yellow: ["red", "green", "yellow"]
colors.splice(2, 1, "yellow")
```
