# 作用域(scope)

## 全局作用域（Global Scope）

最外层函数和在最外层函数外面定义的变量拥有全局作用域

```
var scope="global";  //声明一个全局变量
function checksope(){
    function showglobal(){
        alert(scope); //弹窗全局变量
    }
    showglobal();
}
checksope()   // global 内部函数可以访问全局变量
```

所有末定义直接赋值的变量自动声明为拥有全局作用域

```
function checksope(){
    var scope="local";
    scopeglobal="global";
    alert(scope);
}
checksope();  // local
alert(scopeglobal); //    global  不带var关键词声明的变量，
                          直接升级为全局变量，同时也是全局变量
                           的一个属性
alert(scope); //脚本错误
```

所有 window 对象的属性拥有全局作用域

## 函数作用域

JavaScript 没有块级作用域。JavaScript 取而代之地使用了函数作用域：变量在声明他们的函数体以及这个函数体嵌套的任意函数体内都有定义的。

```
function test（0）{
    var i = 0;  // i在行函数体内时有定义的，
    if（typof 0 == "object"){
        var j = 0;  //j在函数体内是有定义的，不仅仅是在循环内
        for(var k=0; k<10;k++){ //k在行函数体内是有定义的，不仅仅是在循环内
            console.log(k);//输出数字0-9
        }
        console.log(k);  //k 已经定义了，输出10
    }
    console.log(j);    //j 已经定义了，但是可能没有初始化
}
```

## 作为属性的变量

当声明一个全局变量时，实际上是定义了全局对象的一个属性。使用 var 声明的变量不可配置，未声明的可配置

此规则只对全局变量有效

```
var  truvar = 1;   //声明一个不可删除的全局变量
fakevar = 2；       //创建全局对象的一个可删除的属性
this.fakecar2 = 3;//同上
delete truevar //=> false:变量并没有被删除
delete fakevar //=> true:变量并没有被删除
delete this.fakevar2 //=> true:变量并没有被删除
```

# 作用域链

每一段 javascript 代码（全局代码或函数）都有一个与之关联的作用域链。这个作用域连是一个对象列表或者链表，这组对象定义了这段代码“作用域中”的变量。当 javascript 需要查找变量 x 的值的时候（这个过程称作“变量解析”),它会从链中的第一个对象开始查找，如果这个对象有一个名为 x 属性，则会直接使用这个属性的值，如果第一个对象中不存在，则会继续寻找下一个对象，依次类推。如果作用域链上没有任何一个对象含有属性 x，则抛出错误（ReferenceError）异常。

不同的层级作用域上对象的分布

1.  在 javascript 的最顶层（也就是不包含任何函数定义内的代码），作用域链由一个全局对象组成。
2.  在不包含嵌套的函数体内，作用域链上有两个对象，第一个是定义函数参数和局部变量的对象，第二个是全局对象。
3.  在一个嵌套的函数体内，作用域链上至少有三个对象。当调用这个函数时，它创建一个新的对象来存储它的局部变量，它实际上保存在同一个作用域链。
