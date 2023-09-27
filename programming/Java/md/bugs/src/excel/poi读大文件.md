# org.apache.poi.util.RecordFormatException: Tried to allocate an array of length 4276190, but 1000000 is the maximum for this record type

POI有一些缺陷，比如07版Excel解压缩以及解压后存储都是在内存中完成的，内存消耗依然很大。poi在处理之前使用IOUtils里面的方法校验了下数据的字节长度，当超过常量配置的长度后会抛出一个异常，就是我们上面看见的异常。

## 解决方案

使用EasyExcel

