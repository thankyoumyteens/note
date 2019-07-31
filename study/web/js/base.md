# 变量对象

变量对象定义着一个函数内定义的参数列表.内部变量和内部函数。

![vo](../img/vo.png)

变量对象是在函数被调用，但是函数尚未执行的时刻被创建的，
这个创建变量对象的过程实际就是函数内数据(函数参数.内部变量.内部函数)初始化的过程。

# 活动对象

未进入执行阶段之前，变量对象中的属性都不能访问！但是进入执行阶段之后，
变量对象转变为了活动对象，里面的属性都能被访问了，然后开始进行执行阶段的操作。
所以活动对象实际就是变量对象在真正执行时的另一种形式。

# 变量提升的原因

首先要了解两个名词。

**JS 作用域和词法分析**

如何了解 JS 作用域呢？ 那么就要了解什么是执行环境。

执行环境：执行环境定义了变量和函数有权访问的其他数据。每个执行环境都有对应的变量对象(Variable Object),保存着该环境中定义的变量和函数。我们无法通过代码来访问它，但是解析器在处理数据的时候会在后台使用到它。

- 全局执行环境：最外围的执行环境。我们可以认为是 window 对象，因此所有的全局变量和函数都是做为 window 的属性和方法创建的。

- 局部执行环境：每个函数都有自己的执行环境，当执行流进入到一个函数时，函数的环境就被推入到执行栈当中，当函数执行完毕并且没有引用时，栈将其环境弹出，将控制权返回给之前的执行环境。

作用域

- 全局作用域：可以在代码中的任何地方都能被访问。

- 局部作用域 : 只有在函数内部才能访问。

- 作用域链：全局作用域和局部作用域中变量的访问，其实是由作用域链决定的。

每次进入一个新的执行环境，都会创建一个用于搜索变量和函数的作用域链。作用域链是函数被创建的作用域中对象的集合。作用域链可以保证对执行环境有权访问的所有变量和函数的有序访问。

作用域链的最前端始终是当前执行的代码所在的环境的变量对象，如果该环境是函数，则将其活动对象作为变量对象，下一个变量对象来自包含环境，下一个变量对象来自包含环境的包含环境，依次往上，直到全局执行变量。

标识符解析沿着作用域一级一级的向上搜索标识符的过程。搜索过程始终是从作用域的前端逐渐向后回朔，直到找到标识符。

这就是 JS 的作用域和作用域链。

词法分析：

在 JS 代码执行前，会执行词法分析。所以 JS 运行要分为词法分析和执行两个阶段。

函数在运行的瞬间，会生成一个活动对象 Active Object，简称 AO。

分析形参

- 如果函数有形参，则给当前活动对象增加属性，赋值为 undefined。
  分析变量
- 如果 AO 上还没有 XXX 属性，则给当前活动对象增加属性，赋值为 undefined.
- 如果 AO 上有 XXX 属性，则不做任何影响。
  分析函数
- 把函数赋值给 AO.XXX 属性
- 如果此前 XXX 属性已存在，则覆盖。