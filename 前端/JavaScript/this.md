# this的指向

this的指向在函数定义的时候是确定不了的，
只有函数执行的时候才能确定this到底指向谁，
实际上this的最终指向的是那个调用它的对象

情况1：如果一个函数中有this，
但是它没有被上一级的对象所调用，
那么this指向的就是window。
```
// 这里的this指向window
function a(){
    var user = "追梦子";
    console.log(this.user); //undefined
    console.log(this); //Window
}
a();

// 这里的this指向window
var o = {
    a:10,
    b:{
        a:12,
        fn:function(){
            console.log(this.a); //undefined
            console.log(this); //window
        }
    }
}
// 在将fn赋值给变量j的时候并没有执行所以最终指向的是window
var j = o.b.fn;
j();
```

情况2：如果一个函数中有this，
这个函数有被上一级的对象所调用，
那么this指向的就是上一级的对象。
```
// 这里的this指向o, 因为调用这个fn是通过o.fn()执行的
var o = {
    user:"追梦子",
    fn:function(){
        console.log(this.user);  //追梦子
    }
}
o.fn();
```

情况3：如果一个函数中有this，
这个函数中包含多个对象，
尽管这个函数是被最外层的对象所调用，
this指向的也只是它上一级的对象。
```
// 这里的this指向b
var o = {
    a:10,
    b:{
        a:12,
        fn:function(){
            console.log(this.a); //12
        }
    }
}
o.b.fn();

// 这里的this指向b
var o = {
    a:10,
    b:{
        fn:function(){
            console.log(this.a); //undefined
        }
    }
}
o.b.fn();
```

情况4：构造函数中的this
```
function Fn(){
    this.user = "追梦子";
}
// new关键字改变了this的指向，将这个this指向对象a
var a = new Fn();
console.log(a.user); //追梦子
```
```
// 如果返回值是一个对象，那么this指向的就是那个返回的对象
function fn()  
{  
    this.user = '追梦子';  
    return {};  
}
var a = new fn;  
console.log(a.user); //undefined
```
```
// 如果返回值不是一个对象(包括特例null)那么this还是指向函数的实例
function fn()  
{  
    this.user = '追梦子';  
    return 1;
}
var a = new fn;  
console.log(a.user); //追梦子
```

## 改变this指向

1.  call(this 指向谁,arg1,arg2,...) // 参数一个一个传

2.  apply(this 指向谁,[arg1,arg2...]) // 参数为数组

3.  bind(this 指向谁,arg1,arg2,...) // 定义时传的参数供调用时使用

```
var a=2;
var json = {
    a: 1,
    show(){
        // alert(this.a); // 输出：1
        setTimeout(function(){
            // setTimeout中this默认为window,
            // 使用bind()改变this为json对象
            alert(this.a);
        }.bind(this),1000)
    }
}
json.show();// 正确输出：1，而不是：2
```
