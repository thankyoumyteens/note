# 1.1 A Bit of History

Java 语言是一个通用的, 支持并发的面向对象语言。它的语法和 C/C++类似, 但它去掉了 C/C++中复杂难懂和不安全的用法。Java
平台一开始是为了开发能联网的消费级设备上的软件而设计的。它支持多主机架构并且支持软件组件的安全分发。为了满足这些要求, 编译后的代码需要通过网络传输, 在任意客户端上安全地运行。

万维网的普及使这些特性更有趣。浏览器使人们很容易就能在网上浏览各种内容。最终, 不管你使用什么机器, 网速是快还是慢, 你的所见所闻都是一样的。

Web爱好者很快发现HTML格式的文档限制太大了。 HTML extensions, such as forms, only
highlighted those limitations, while making it clear that no browser could include
all the features users wanted. 解决方案是可扩展性。

The HotJava browser first showcased the interesting properties of the Java
programming language and platform by making it possible to embed programs
inside HTML pages. Programs are transparently downloaded into the browser
along with the HTML pages in which they appear. Before being accepted by the
browser, programs are carefully checked to make sure they are safe. Like HTML
pages, compiled programs are network- and host-independent. The programs
behave the same way regardless of where they come from or what kind of machine
they are being loaded into and run on.

A Web browser incorporating the Java platform is no longer limited to a
predetermined set of capabilities. Visitors to Web pages incorporating dynamic
content can be assured that their machines cannot be damaged by that content.
Programmers can write a program once, and it will run on any machine supplying
a Java run-time environment.
