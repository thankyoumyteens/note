# JavaScript数据类型

5种不同的数据类型：

- string
- number
- boolean
- object
- function

3种对象类型：

- Object
- Date
- Array

2个不包含任何值的数据类型：

- null
- undefined

例子

```
typeof "John"                 // 返回 string
typeof 3.14                   // 返回 number
typeof NaN                    // 返回 number
typeof false                  // 返回 boolean
typeof [1,2,3,4]              // 返回 object
typeof {name:'John', age:34}  // 返回 object
typeof new Date()             // 返回 object
typeof function () {}         // 返回 function
typeof myCar                  // 返回 undefined (如果 myCar 没有声明)
typeof null                   // 返回 object
```

# 判断类型

1. typeof(例: `typeof a` // 不能判断object的具体类型)

2. instanceof(例: `a instanceof Array`)

3. constructor(例: `[1, 2].constructor === Array`)

4. Object.prototype.toString.call(例: `Object.prototype.toString.call(a)` // 输出: [object Array])
