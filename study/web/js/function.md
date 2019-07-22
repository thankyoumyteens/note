- <a href="#数组方法">数组方法</a>
- <a href="#字符串方法">字符串方法</a>
- <a href="#数组去重">数组去重</a>

<a id="数组方法"></a>
# 数组方法

## 创建数组

```
var arr1 = new Array(); //创建一个空数组
var arr2 = new Array(20); // 创建一个包含20项的数组
var arr3 = new Array("lily","lucy","Tom"); // 创建一个包含3个字符串的数组
var arr4 = []; //创建一个空数组
var arr5 = [20]; // 创建一个包含1项的数组
var arr6 = ["lily","lucy","Tom"]; // 创建一个包含3个字符串的数组
```

## 数组方法

> 1.  join()

join(separator): 将数组的元素组起一个字符串，以 separator 为分隔符，省略的话则用默认用逗号为分隔符，该方法只接收一个参数：即分隔符。

```
var arr = [1,2,3];
console.log(arr.join()); // 1,2,3
console.log(arr.join("-")); // 1-2-3
console.log(arr); // [1, 2, 3]（原数组不变）
```

通过 join()方法可以实现重复字符串，只需传入字符串以及重复的次数，就能返回重复后的字符串，函数如下：

```
function repeatString(str, n) {
return new Array(n + 1).join(str);
}
console.log(repeatString("abc", 3)); // abcabcabc
console.log(repeatString("Hi", 5)); // HiHiHiHiHi
```

> 2.  push()和 pop()

push(): 可以接收任意数量的参数，把它们逐个添加到数组末尾，并返回修改后数组的长度。
pop()：数组末尾移除最后一项，减少数组的 length 值，然后返回移除的项。

```
var arr = ["Lily","lucy","Tom"];
var count = arr.push("Jack","Sean");
console.log(count); // 5
console.log(arr); // ["Lily", "lucy", "Tom", "Jack", "Sean"]
var item = arr.pop();
console.log(item); // Sean
console.log(arr); // ["Lily", "lucy", "Tom", "Jack"]
```

> 3.  shift() 和 unshift()

shift()：删除原数组第一项，并返回删除元素的值；如果数组为空则返回 undefined 。
unshift:将参数添加到原数组开头，并返回数组的长度 。

这组方法和上面的 push()和 pop()方法正好对应，一个是操作数组的开头，一个是操作数组的结尾。

```
var arr = ["Lily","lucy","Tom"];
var count = arr.unshift("Jack","Sean");
console.log(count); // 5
console.log(arr); //["Jack", "Sean", "Lily", "lucy", "Tom"]
var item = arr.shift();
console.log(item); // Jack
console.log(arr); // ["Sean", "Lily", "lucy", "Tom"]
```

> 4.  sort()

sort()：按升序排列数组项——即最小的值位于最前面，最大的值排在最后面。

在排序时，sort()方法会调用每个数组项的 toString()转型方法，然后比较得到的字符串，以确定如何排序。即使数组中的每一项都是数值， sort()方法比较的也是字符串，因此会出现以下的这种情况：

```
var arr1 = ["a", "d", "c", "b"];
console.log(arr1.sort()); // ["a", "b", "c", "d"]
arr2 = [13, 24, 51, 3];
console.log(arr2.sort()); // [13, 24, 3, 51]
console.log(arr2); // [13, 24, 3, 51](元数组被改变)
```

为了解决上述问题，sort()方法可以接收一个比较函数作为参数，以便我们指定哪个值位于哪个值的前面。比较函数接收两个参数，如果第一个参数应该位于第二个之前则返回一个负数，如果两个参数相等则返回 0，如果第一个参数应该位于第二个之后则返回一个正数。以下就是一个简单的比较函数：

```
function compare(value1, value2) {
    if (value1 < value2) {
        return -1;
    } else if (value1 > value2) {
        return 1;
    } else {
        return 0;
    }
}
arr2 = [13, 24, 51, 3];
console.log(arr2.sort(compare)); // [3, 13, 24, 51]
```

如果需要通过比较函数产生降序排序的结果，只要交换比较函数返回的值即可：

```
function compare(value1, value2) {
    if (value1 < value2) {
        return 1;
    } else if (value1 > value2) {
        return -1;
    } else {
        return 0;
    }
}
arr2 = [13, 24, 51, 3];
console.log(arr2.sort(compare)); // [51, 24, 13, 3]
```

> 5.  reverse()

reverse()：反转数组项的顺序。

```
var arr = [13, 24, 51, 3];
console.log(arr.reverse()); //[3, 51, 24, 13]
console.log(arr); //[3, 51, 24, 13](原数组改变)
```

> 6.  concat()

concat() ：将参数添加到原数组中。这个方法会先创建当前数组一个副本，然后将接收到的参数添加到这个副本的末尾，最后返回新构建的数组。在没有给 concat()方法传递参数的情况下，它只是复制当前数组并返回副本。

```
var arr = [1,3,5,7];
var arrCopy = arr.concat(9,[11,13]);
console.log(arrCopy); //[1, 3, 5, 7, 9, 11, 13]
console.log(arr); // [1, 3, 5, 7](原数组未被修改)
```

从上面测试结果可以发现：传入的不是数组，则直接把参数添加到数组后面，如果传入的是数组，则将数组中的各个项添加到数组中。但是如果传入的是一个二维数组呢？

```
var arrCopy2 = arr.concat([9,[11,13]]);
console.log(arrCopy2); //[1, 3, 5, 7, 9, Array[2]]
console.log(arrCopy2[5]); //[11, 13]
```

上述代码中，arrCopy2 数组的第五项是一个包含两项的数组，也就是说 concat 方法只能将传入数组中的每一项添加到数组中，如果传入数组中有些项是数组，那么也会把这一数组项当作一项添加到 arrCopy2 中。

> 7.  slice()

slice()：返回从原数组中指定开始下标到结束下标之间的项组成的新数组。slice()方法可以接受一或两个参数，即要返回项的起始和结束位置。在只有一个参数的情况下， slice()方法返回从该参数指定位置开始到当前数组末尾的所有项。如果有两个参数，该方法返回起始和结束位置之间的项——但不包括结束位置的项。

```
var arr = [1,3,5,7,9,11];
var arrCopy = arr.slice(1);
var arrCopy2 = arr.slice(1,4);
var arrCopy3 = arr.slice(1,-2);
var arrCopy4 = arr.slice(-4,-1);
console.log(arr); //[1, 3, 5, 7, 9, 11](原数组没变)
console.log(arrCopy); //[3, 5, 7, 9, 11]
console.log(arrCopy2); //[3, 5, 7]
console.log(arrCopy3); //[3, 5, 7]
console.log(arrCopy4); //[5, 7, 9]
```

arrCopy 只设置了一个参数，也就是起始下标为 1，所以返回的数组为下标 1（包括下标 1）开始到数组最后。
arrCopy2 设置了两个参数，返回起始下标（包括 1）开始到终止下标（不包括 4）的子数组。
arrCopy3 设置了两个参数，终止下标为负数，当出现负数时，将负数加上数组长度的值（6）来替换该位置的数，因此就是从 1 开始到 4（不包括）的子数组。
arrCopy4 中两个参数都是负数，所以都加上数组长度 6 转换成正数，因此相当于 slice(2,5)。

> 8.  splice()

splice()：很强大的数组方法，它有很多种用法，可以实现删除.插入和替换。

删除：可以删除任意数量的项，只需指定 2 个参数：要删除的第一项的位置和要删除的项数。例如， splice(0,2)会删除数组中的前两项。

插入：可以向指定位置插入任意数量的项，只需提供 3 个参数：起始位置. 0（要删除的项数）和要插入的项。例如，splice(2,0,4,6)会从当前数组的位置 2 开始插入 4 和 6。
替换：可以向指定位置插入任意数量的项，且同时删除任意数量的项，只需指定 3 个参数：起始位置.要删除的项数和要插入的任意数量的项。插入的项数不必与删除的项数相等。例如，splice (2,1,4,6)会删除当前数组位置 2 的项，然后再从位置 2 开始插入 4 和 6。

splice()方法始终都会返回一个数组，该数组中包含从原始数组中删除的项，如果没有删除任何项，则返回一个空数组。

```
var arr = [1,3,5,7,9,11];
var arrRemoved = arr.splice(0,2);
console.log(arr); //[5, 7, 9, 11]
console.log(arrRemoved); //[1, 3]
var arrRemoved2 = arr.splice(2,0,4,6);
console.log(arr); // [5, 7, 4, 6, 9, 11]
console.log(arrRemoved2); // []
var arrRemoved3 = arr.splice(1,1,2,4);
console.log(arr); // [5, 2, 4, 4, 6, 9, 11]
console.log(arrRemoved3); //[7]
```

> 9.  indexOf()和 lastIndexOf()

indexOf()：接收两个参数：要查找的项和（可选的）表示查找起点位置的索引。其中， 从数组的开头（位置 0）开始向后查找。
lastIndexOf：接收两个参数：要查找的项和（可选的）表示查找起点位置的索引。其中， 从数组的末尾开始向前查找。

这两个方法都返回要查找的项在数组中的位置，或者在没找到的情况下返回 1。在比较第一个参数与数组中的每一项时，会使用全等操作符。

```
var arr = [1,3,5,7,7,5,3,1];
console.log(arr.indexOf(5)); //2
console.log(arr.lastIndexOf(5)); //5
console.log(arr.indexOf(5,2)); //2
console.log(arr.lastIndexOf(5,4)); //2
console.log(arr.indexOf("5")); //-
```

> 10. forEach()

forEach()：对数组进行遍历循环，对数组中的每一项运行给定函数。这个方法没有返回值。参数都是 function 类型，默认有传参，参数分别为：遍历的数组内容；第对应的数组索引，数组本身。

```
var arr = [1, 2, 3, 4, 5];
arr.forEach(function(x, index, a){
    console.log(x + '|' + index + '|' + (a === arr));
});
// 输出为：
// 1|0|true
// 2|1|true
// 3|2|true
// 4|3|true
// 5|4|true
```

> 11. map()

map()：指“映射”，对数组中的每一项运行给定函数，返回每次函数调用的结果组成的数组。

下面代码利用 map 方法实现数组中每个数求平方。

```
var arr = [1, 2, 3, 4, 5];
var arr2 = arr.map(function(item){
    return item*item;
});
console.log(arr2); //[1, 4, 9, 16, 25]
```

> 12. filter()

filter()：“过滤”功能，数组中的每一项运行给定函数，返回满足过滤条件组成的数组。

```
var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
var arr2 = arr.filter(function(x, index) {
    return index % 3 === 0 || x >= 8;
});
console.log(arr2); //[1, 4, 7, 8, 9, 10]
```

> 13. every()

every()：判断数组中每一项都是否满足条件，只有所有项都满足条件，才会返回 true。

```
var arr = [1, 2, 3, 4, 5];
var arr2 = arr.every(function(x) {
    return x < 10;
});
console.log(arr2); //true
var arr3 = arr.every(function(x) {
    return x < 3;
});
console.log(arr3); // false
```

> 14. some()

some()：判断数组中是否存在满足条件的项，只要有一项满足条件，就会返回 true。

```
var arr = [1, 2, 3, 4, 5];
var arr2 = arr.some(function(x) {
    return x < 3;
});
console.log(arr2); //true
var arr3 = arr.some(function(x) {
    return x < 1;
});
console.log(arr3); // false
```

> 15. reduce()和 reduceRight()

这两个方法都会实现迭代数组的所有项，然后构建一个最终返回的值。reduce()方法从数组的第一项开始，逐个遍历到最后。而 reduceRight()则从数组的最后一项开始，向前遍历到第一项。

这两个方法都接收两个参数：一个在每一项上调用的函数和（可选的）作为归并基础的初始值。

传给 reduce()和 reduceRight()的函数接收 4 个参数：前一个值.当前值.项的索引和数组对象。这个函数返回的任何值都会作为第一个参数自动传给下一项。第一次迭代发生在数组的第二项上，因此第一个参数是数组的第一项，第二个参数就是数组的第二项。

下面代码用 reduce()实现数组求和，数组一开始加了一个初始值 10。

```
var values = [1,2,3,4,5];
var sum = values.reduceRight(function(prev, cur, index, array){
    return prev + cur;
},10);
console.log(sum); //25
```

<a id="字符串方法"></a>
# 字符串方法

> 1.  charAt 返回指定索引出的字符

```
var str='abcd';
var a=str.charAt(0);
console.log(a); //'a'
console.log(str); //'abcd'
```

> 2.  charCodeAt 返回指定索引出的 unicode 字符

```
str.charCodeAt(0);   //97
```

> 3.  indexOf 判断一个字符第一次出现在某个字符串的索引，如果包含返回它的索引，如果不包含返回-1.

```
str.indexOf('a');     //0
str.indexOf('e');     //-1
```

> 4.  lastIndexOf 判断一个字符最后一次出现在某个字符串的索引，如果包含返回它的索引，如果不包含返回-1.

```
str.lastIndexOf('b');   //1
str.lastIndexOf('e');   //-1
```

> 5.  concat 拼接 2 个字符串，返回一个新字符串，对原有字符串没有任何改变。

```
var str='qwe';
var str1='abc';
var str2=str.concat(str1);
console.log(str2);//"qweabc"
```

> 6.  substr(n,m) 从索引 n 开始，截取 m 个字符，将截取的字符返回，对原字符串没有任何改变。

```
var b=s.substr(1,1)
console.log(b);  //'w'
```

> 7.  substring(n,m) 从索引 n 开始，截取到索引 m,不包括 m.将截取的字符返回,对原字符串没有任何改变.

```
var ee=str.substring(1,3);
console.log(ee);  //"bc"
```

> 8.  slice(n,m) 从索引 n 开始，截取到索引 m,不包括 m.将截取的字符返回,对原字符串没有任何改变.

```
var aa=str.slice(0,3);
console.log（aa）;//'abc'
```

> 9.  split 用指定字符分割字符串，返回一个数组.对原字符串没有任何改变。

```
var a=str.split('');
console.log(a);  //["a", "b", "c", "d"]
```

> 10. replace('a',1); 替换指定字符，返回替换后新的字符串，对原有字符串有改变。(第一个参数可以是正则表达式) 只能替换一次 ，配合正则模式修饰符 g 使用

```
var str='aaaaee';
var reg=/a/g;
str.replace(reg,1);   //"1111ee"
```

> 11. match() 可在字符串内检索指定的值，或找到一个或多个正则表达式的匹配。把找到的字符放在数组里，返回一个数组。

```
var str='aaaa3ed33';
var reg=/a/g;
str.match(reg);  //["a", "a", "a", "a"]
```

> 12. search() 方法用于检索字符串中指定的子字符串，或检索与正则表达式相匹配的子字符串。

<a id="数组去重"></a>
# 数组去重


```
/*
    * 新建一新数组，遍历传入数组，值不在新数组就push进该新数组中
    */
function uniq(array) {
    let temp = [];
    for (let i = 0; i < array.length; i++) {
        if (temp.indexOf(array[i]) == -1) {
            temp.push(array[i]);
        }
    }
    return temp;
}
```


```
/*
    * 缺点: 空间占用多
    *
    * 新建一js对象以及新数组，遍历传入数组时，判断值是否为js对象的键，
    * 不是的话给对象新增该键并放入新数组。
    * 问题: 判断是否为js对象键时，会自动对传入的键执行toString()，
    * 不同的键可能会被误认为一样，例如n[val]-- n[1]、n["1"]；
    * 解决上述问题还是得调用"indexOf"
    */
function uniq(array) {
    let result = [];
    let obj = {};
    for (let i = 0; i < array.length; i++) {
        let item = array[i];
        if (!obj[item]) {
            result.push(item);
            obj[item] = true;
        }
    }
    return result;
}
```


```
/*
    * 给传入数组排序，排序后相同值相邻，
    * 然后遍历时,新数组只加入不与前一值重复的值。
    * 会打乱原来数组的顺序
    */
function uniq(array) {
    array.sort();
    var temp = [array[0]];
    for (var i = 1; i < array.length; i++) {
        if (array[i] !== temp[temp.length - 1]) {
            temp.push(array[i]);
        }
    }
    return temp;
}
```


```
/*
    *
    * 如果当前数组的第i项在当前数组中第一次出现的位置不是i，
    * 那么表示第i项是重复的，忽略掉。否则存入结果数组。
    */
function uniq(array) {
    var temp = [];
    for (var i = 0; i < array.length; i++) {
        if (array.indexOf(array[i]) == i) {
            temp.push(array[i])
        }
    }
    return temp;
}
```


```
// ES6的Set
function uniq(array) {
    return Array.from(new Set(array));
}
```
