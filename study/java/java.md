# Java九种基本数据类型的大小，以及他们的封装类

java提供了一组基本数据类型，包括

void,
boolean, 
char,
byte(1字节), 
short(2字节),
int(4字节),
long(8字节),
float(4字节),
double(8字节)

同时，java也提供了这些类型的封装类，分别为

Void,
Boolean,
Character,
Byte,
Short,
Integer,
Long,
Float,
Double

基本数据类型与其对应的封装类由于本质的不同，具有一些区别：

- 基本数据类型只能按值传递，而封装类按引用传递。
- 基本类型在栈中创建；而对于对象类型，对象在堆中创建，对象的引用在栈中创建。

# Switch能否用string做参数

jdk1.7之前不可以, jdk1.7之后可以

jdk1.7并没有新的指令来处理switch string,
而是通过调用switch中string.hashCode,将string转换为int从而进行判断

# equals与==的区别

== 比较的是栈中存放的内存地址, 如果是基本类型的比较, 值相等则为true

equals用来比较的是两个对象的内容是否相等,
由于所有的类都是继承自java.lang.Object类的,
所以适用于所有对象,如果没有对该方法进行覆盖的话,
调用的仍然是Object类中的方法,
而Object中的equals方法返回的却是==的判断。

String s="abc"是一种非常特殊的形式,
和new 有本质的区别。
它是java中唯一不需要new就可以产生对象的途径。
它是在常量池中而不是象new一样放在压缩堆中。
当声明这样的一个字符串后, JVM会在常量池中先查找有有没有一个值为"abc"的对象,
如果有就会把它赋给当前引用,
如果没有则在常量池中新创建一个"abc",
下一次如果有String s1 = "abc"
又会将s1指向"abc"这个对象,
即以这形式声明的字符串,只要值相等,
任何多个引用都指向同一对象。
而String s = new String("abc")和其它任何对象一样,
每调用一次就产生一个新对象。

# Object有哪些公用方法

## clone方法

保护方法，实现对象的浅复制，
只有实现了Cloneable接口才可以调用该方法，
否则抛出CloneNotSupportedException异常。

## getClass方法

final方法，获得运行时类型。

## toString方法

该方法用得比较多，一般子类都有覆盖。

## equals方法

该方法是非常重要的一个方法。
一般equals和==是不一样的，
但是在Object中两者是一样的。
子类一般都要重写这个方法。

## hashCode方法

该方法用于哈希查找，可以减少在查找中使用equals的次数，
重写了equals方法一般都要重写hashCode方法。
这个方法在一些具有哈希功能的Collection中用到。

# hashCode的作用

Java中的集合Set元素无序，但元素不可重复。
equals方法可用于保证元素不重复，
但如果每增加一个元素就检查一次，
若集合中现在已经有1000个元素，
那么第1001个元素加入集合时，
就要调用1000次equals方法。
这显然会大大降低效率。
于是，Java采用了哈希表的原理。

哈希算法也称为散列算法，
是将数据依特定算法直接指定到一个地址上。
这样一来，当集合要添加新的元素时，
先调用这个元素的HashCode方法，
就一下子能定位到它应该放置的物理位置上。

1. 如果这个位置上没有元素，它就可以直接存储在这个位置上，不用再进行任何比较了；
2. 如果这个位置上已经有元素了，就调用它的equals方法与新元素进行比较，相同的话就不存了；
3. 不相同的话，也就是发生了Hash key相同导致冲突的情况，那么就在这个Hash key的地方产生一个链表，将所有产生相同HashCode的对象放到这个单链表上去，串在一起。

这样一来实际调用equals方法的次数就大大降低了。

# ArrayList、LinkedList、Vector的区别

三者都属于List的子类，方法基本相同。
比如都可以实现数据的添加、删除、定位以及都有迭代器进行数据的查找，
但是每个类在安全，性能，行为上有着不同的表现。

Vector是Java中线程安全的集合类，底部实现也是数组来操作，
在添加数据时，会自动根据需要创建新数组增加长度来保存数据，并拷贝原有数组数据

ArrayList是应用广泛的动态数组实现的集合类，
不过线程不安全，所以性能要好的多，也可以根据需要增加数组容量，
不过与Vector的调整逻辑不同，ArrayList增加50%，而Vector会扩容1倍。

LinkedList是基于双向链表实现，不需要增加长度，也不是线程安全的
　　
# HashMap的初始容量机制及扩容机制

第一种情况：当我们没有设置初始化容量时，HashMap就使用默认的初始化容量，也就是16

第二种情况：当我们设置了初始化容量，HashMap就会按照我们设置的容量进行设置吗？
答案是不一定。当你设置的初始化容量是2的n次方时，就会按照你设置的容量设置；
当你设置的初始化容量不是2的n次方时，
就会按照大于你设置的那个值但是最接近你设置的那个值的2的n次方进行设置。

当我们的容量是16，加载因子是0.75时，
当存储的键值对的数量大于16*0.75=12时，HashMap会以2倍的容量进行扩容操作

# String、StringBuffer与StringBuilder的区别

String: 不可变字符序列

StringBuffer: 可变字符序列, 效率低, 线程安全

StringBuilder: 可变字符序列, 效率高, 线程不安全

# HashMap和HashTable的区别

1. 两者计算hash的方法不同
2. HashMap的初始容量为16，HashTable初始容量为11，两者的填充因子默认都是0.75
3. HashMap扩容时是当前容量翻倍即:capacity*2，HashTable扩容时是容量翻倍+1即:capacity*2+1
4. HashMap是非线程安全的，HashTable是线程安全的
5. HashMap中key和value都允许为null。key为null的键值对永远都放在以table[0]为头结点的链表中。HashTable在遇到null时，会抛出NullPointerException异常

# 当try、catch中有return时，finally中的代码会执行么

1. 不管有没有异常，finally中的代码都会执行
2. 当try、catch中有return时，finally中的代码依然会继续执行
3. finally是在return后面的表达式运算之后执行的，此时并没有返回运算之后的值，而是把值保存起来，不管finally对该值做任何的改变，返回的值都不会改变，依然返回保存起来的值。也就是说方法的返回值是在finally运算之前就确定了的。
4. 如果return的数据是引用数据类型，而在finally中对该引用数据类型的属性值的改变起作用，try中的return语句返回的就是在finally中改变后的该属性的值。
5. finally代码中最好不要包含return，程序会提前退出，也就是说返回的值不是try或catch中的值

# 抽象类和接口的不同

1. 抽象类是对类抽象，而接口是对行为抽象；
2. 抽象类只能继承一个，而接口可以实现多个；
3. 抽象类有构造方法（为子类准备），而接口没有构造方法；
4. 抽象类中可以有非抽象方法，而接口中只能有抽象方法，并且只能是public类型的，默认为 public abstract 类型（JDK1.8开始，接口中可以通过default关键字来定义非抽象方法，解决扩展问题）；
5. 抽象类中可以有成员变量和属性，而接口中只能有由static final修饰的常量；
6. 抽象类和接口中都可以包含静态成员变量，抽象类中的静态成员变量的访问类型可以是任意类型，但接口中定义的变量只能是 public static final 类型，并且默认为 public static final 类型。

# 实现多线程的两种方法

## 继承Thread类创建线程

Thread类本质上是实现了Runnable接口的一个实例，代表一个线程的实例。
启动线程的唯一方法就是通过Thread类的start()实例方法。
start()方法是一个native方法，它将启动一个新线程，并执行run()方法。
这种方式实现多线程很简单，通过自己的类直接extend Thread，并复写run()方法，
就可以启动新线程并执行自己定义的run()方法

```
public class MyThread extends Thread {  
　　public void run() {  
　　 System.out.println("MyThread.run()");  
　　}  
}  
 
MyThread myThread1 = new MyThread();  
MyThread myThread2 = new MyThread();  
myThread1.start();  
myThread2.start();
```

## 实现Runnable接口创建线程

如果自己的类已经extends另一个类，就无法直接extends Thread，
此时，可以实现一个Runnable接口

```
public class MyThread extends OtherClass implements Runnable {  
　　public void run() {  
　　 System.out.println("MyThread.run()");  
　　}  
} 

MyThread myThread = new MyThread();  
Thread thread = new Thread(myThread);  
thread.start();
```

# String类中常用的方法

1. int length(): 获取字符串的长度
2. char charAt(int index): 获取指定的索引处的字符串
3. int indexOf(String str, int fromIndex): 获取str在字符串对象中第一次出现的索引
4. int lastIndexOf(String str, int fromIndex): 从字符串的末尾位置向前查找
5. String substring(int start，int end): 从start开始截取字符，到end结束截取字符
6. char[] toCharArray(): 把字符串转换为字符数组；
7. String toLowerCase(): 把字符串转换为小写字符串
8. String toUpperCase(): 把字符串转换为小写字符串
9. int compareTo(String str): 对字符串内容按字典顺序进行大小比较 
10. int compareToIgnoreCase (String str): 与compareTo方法相似，但忽略大小写
11. boolean equals(Object obj): 比较当前字符串和参数字符串是否相等
12. boolean equalsIgnoreCase(String str): 与equals方法相似，但忽略大小写
13. String trim(): 去除字符串两端的空格，中间的空格不变
14. String[] split(String str): 将字符串分割成字符串数组
15. String replace(char oldChar, char newChar): 用字符newChar替换当前字符串中所有的oldChar字符，并返回一个新的字符串
16. String replace(String oldStr, String newStr): 用字符串newStr替换当前字符串中所有的oldStr字符串，并返回一个新的字符串
17. String replaceFirst(String regex,String replacement): 用字符replacement的内容替换当前字符串中遇到的第一个和正则表达式regex相匹配的子串，并将新的字符串返回
18. String replaceAll(String regex,String replacement): 用字符replacement的内容替换当前字符串中遇到的所有和正则表达式regex相匹配的子串，并将新的字符串返回

