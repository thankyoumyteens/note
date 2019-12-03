# 箭头函数

优势

- 更加简洁

- 修复了 this 的指向

普通函数中的 this:

1.  this 总是代表它的直接调用者(js 的 this 是执行上下文), 例如 obj.func ,那么 func 中的 this 就是 obj

2.  非严格模式下, 没找到直接调用者,则 this 指的是 window

3.  在严格模式下, 没找到直接调用者,则 this 指的是 undefined

4.  使用 call,apply,bind 可以改变 this 的指向

箭头函数中的 this

箭头函数没有自己的 this(也没有 arguments), 它的 this(和 arguments)是从父作用域继承而来; 默认指向在定义它时所处的对象(宿主对象),而不是执行时的对象

由于箭头函数不绑定 this, 它会捕获其所在上下文(即定义的位置)的 this 值, 作为自己的 this 值

所以 call() / apply() / bind() 方法对于箭头函数来说只是传入参数, 对它的 this 毫无影响。

```
function P() {
    this.tmp = 0;
    setInterval(function () {
        // this -> Window
        this.tmp++;
        console.log('P -> ' + this.tmp);
    }, 1000);
}

function P2(val) {
    this.tmp2 = val;
    setInterval(() => {
        // this -> P2实例化的对象
        this.tmp2++;
        console.log('P2 -> ' + this.tmp2);
    }, 1000);
}

let o = new P();
let o2 = new P2(0);
let o3 = new P2(100);

/*
    输出:
    P -> NaN
    P2 -> 1
    P2 -> 101
    P -> NaN
    P2 -> 2
    P2 -> 102
    P -> NaN
    P2 -> 3
    P2 -> 103
*/
```

# 对象字面量增强

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

# 字符串模板

```
let name = 'kazuma'
let str = `your name is ${name}`
console.log(str) // your name is kazuma
```

# 解构赋值

```
let [a, b, c] = [1, 2, 3]
console.log(a) // 1
console.log(b) // 2
console.log(c) // 3
```

# 默认参数, 不定参数, 拓展参数

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

# for of

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

# Proxy(target, handler)

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

# 变量提升

JavaScript 引擎的工作方式是, 先解析代码, 
获取所有被声明的变量, 然后再一行一行地运行。
这造成的结果, 就是所有的变量的声明语句, 都会被提升到代码的头部, 
这就叫做变量提升。

变量提升只对 var 命令声明的变量有效, 如果一个变量不是用 var 命令声明的, 就不会发生变量提升

```
console.log(a); // undefined
var a =1;
console.log(aa); // ReferenceError: aa is not defined
aa =1;
```

let/const 声明的变量存在变量提升,  
但是由于死区(当前作用域顶部到该变量声明位置中间的部分, 都是该 let 变量的死区)
我们无法在声明前访问这个变量

```
console.log(a);// ReferenceError: a is not defined
let a = 1;
```
