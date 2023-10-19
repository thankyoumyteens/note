# ClassPathResource

Spring的配置文件读取是通过ClassPathResource进行封装的：

```java
Resource resource = new ClassPathResource("beanFactoryTest.xml");
```

![](../../img/ClassPathResource.png)

## Resource接口

Spring使用Resource接口封装其内部使用到的资源。

Resource接口抽象了所有Spring内部使用到的底层资源，对不同来源的资源文件都有相应的Resource实现：

- 文件(FileSystemResource)
- 类路径下的资源(ClassPathResource)
- URL资源(UrlResource)
- InputStream资源(InputStreamResource)
- Byte数组(ByteArrayResource)
- 其他

```java
public interface Resource extends InputStreamSource {
    // 资源是否存在
    boolean exists();
    // 资源是否可读
    default boolean isReadable() {
        return true;
    }
    // 资源是否处于打开状态
    default boolean isOpen() {
        return false;
    }
    // 把资源转换成URL类型
    URL getURL() throws IOException;
    // 把资源转换成URI类型
    URI getURI() throws IOException;
    // 把资源转换成File类型
    File getFile() throws IOException;
    // 最后一次修改时间
    long lastModified() throws IOException;
    // 基于当前资源创建一个相对资源
    Resource createRelative(String relativePath) throws IOException;
    // 不带路径信息的文件名
    String getFilename();
    // 用于在错误处理中打印资源的详细信息
    String getDescription();
}
```
