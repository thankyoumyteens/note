# BufferedWriter.write()写中文乱码的解决办法

在用BufferedReader和BufferedWriter读写文件的过程中，发现写的文件中如果含有中文字符会有乱码的情况。
```java
writer = new BufferedWriter(new FileWriter(filePath, false));
writer.write(doc.html());
writer.flush();
```
当我们使用以下方式创建流时，可能会出现中文乱码，

程序断点查看获取到的中文字符没有乱码，是写完文件之后打开乱码，那就和具体生成文件默认打开编码设置有关

所以我们可以在创建流的时候指定编码，如下：
```java
writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(filePath)),"utf-8"));
```
这样就解决了乱码的问题。也可以设置为“GBK”等格式，看自己需求。
