# ES6新特性

1. 箭头函数

2. 使用class关键字创建类

3. 对象字面量增强

```
let person = {
    // 定义方法可以不用function关键字
    say() {
        console.log('hahaha')
    }
}

let student = {
    // 可以在对象字面量里面定义原型
    __proto__: person,
    study() {
        console.log('lalala')
    }
}

student.say() // hahaha
```

4. 字符串模板

```
let name = 'kazuma'
let str = `your name is ${name}`
console.log(str) // your name is kazuma
```

5. 解构赋值

```
let [a, b, c] = [1, 2, 3]
console.log(a) // 1
console.log(b) // 2
console.log(c) // 3
```

6. 默认参数，不定参数，拓展参数

```
// 默认参数
function test(type, val = 0) {
    console.log(`${type}${val}`)
}

test('type_') // type_0
test('type_', 1) // type_1

// 不定参数
function test(...args) {
    console.log(args)
}

test(1, 2, 3) // [1, 2, 3]

// 拓展参数
function test(arg1, arg2, arg3) {
    console.log(arg1)
    console.log(arg2)
    console.log(arg3)
}

test(...[1, 2, 3])

// 输出
// 1
// 2
// 3
```

7. let与const关键字

8. for of

```
var arr = [ "a", "b", "c" ];
 
for (v of arr) {
    console.log(v);
}

// 输出 
// a
// b
// c
```

9. Map，Set 和 WeakMap，WeakSet

10. Proxy(target, handler)

```
var engineer = { name: 'Joe Sixpack', salary: 50 };
 
var interceptor = {
  set: function (receiver, property, value) {
    console.log(property, 'is changed to', value);
    receiver[property] = value;
  }
};
 
engineer = Proxy(engineer, interceptor);

engineer.salary = 60;
// salary is changed to 60
```

11. Promise

12. Symbol

# ES7/8 新特性

ES7

1.  判断元素是否在数组中 `Array.prototype.includes(返回Boolean)`

2.  求幂运算 `2 ** 7(2的7次方)`

ES8

1.  在字符串开头或结尾添加填充字符串 `String.prototype.padStart`和`String.prototype.padEnd`

```
// 第一个参数是填充后字符串的长度
// 第二个参数是填充的字符串, 默认是空格
'es8'.padStart(6, 'woof');  // 'wooes8'
'es8'.padEnd(9, 'woof');  // 'es8woofwo'
```

2.  `Object.values`和`Object.entries` 这两个静态方法是对原有的`Object.keys()`方法的补充。

```
const obj = {
  x: 'xxx',
  y: 1
};

Object.keys(obj); // ['x', 'y']

Object.values(obj); // ['xxx', 1]

Object.entries(obj); // [['x', 'xxx'], ['y', 1]]
```

3.  获取对象的属性描述符(不能是继承自原型链中的属性) `Object.getOwnPropertyDescriptors`

```
const obj = { es8: 'hello es8' };
Object.getOwnPropertyDescriptor(obj, 'es8');
/*
    {
        configurable: true,
        enumerable: true,
        value: "hello es8"
        writable: true
    }
*/
```

4.  允许定义或调用函数时在参数末尾添加逗号

```
function es8(var1, var2, var3,) {
  console.log(arguments.length); // 3
}
es8(10, 20, 30,);
```

5.  async/await
