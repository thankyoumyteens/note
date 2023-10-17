# ClassPathResource

Spring的配置文件读取是通过ClassPathResource进行封装的：

```java
Resource resource = new ClassPathResource("beanFactoryTest.xml");
```

![](../../img/ClassPathResource.png)

Spring对其内部使用到的资源实现了自己的抽象结构：Resource接口。Resource接口抽象了所有Spring内部使用到的底层资源，对不同来源的资源文件都有相应的Resource实现：文件(FileSystemResource)、类路径下的资源(ClassPathResource)、URL资源(UrlResource)、InputStream资源(InputStreamResource)、Byte数组(ByteArrayResource)等。

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

    default boolean isFile() {
        return false;
    }
    // 把资源转换成URL类型
    URL getURL() throws IOException;
    // 把资源转换成URI类型
    URI getURI() throws IOException;
    // 把资源转换成File类型
    File getFile() throws IOException;

    default ReadableByteChannel readableChannel() throws IOException {
        return Channels.newChannel(getInputStream());
    }

    long contentLength() throws IOException;
    // 最后一次修改时间
    long lastModified() throws IOException;
    // 基于当前资源创建一个相对资源
    Resource createRelative(String relativePath) throws IOException;
    // 不带路径信息的文件名
    @Nullable
    String getFilename();
    // 用于在错误处理中打印资源的详细信息
    String getDescription();
}
```

InputStreamSource接口封装任何能返回InputStream的类，它只有一个方法：getlnputStream()，该方法返回一个新的InputStream对象：

```java
public interface InputStreamSource {

    InputStream getInputStream() throws IOException;
}
```

对于getInputStream()方法，ClassPathResource中的实现方式便是通过class或者classLoader提供的底层方法进行调用：

```java
    @Override
    public InputStream getInputStream() throws IOException {
        InputStream is;
        if (this.clazz != null) {
            is = this.clazz.getResourceAsStream(this.path);
        }
        else if (this.classLoader != null) {
            is = this.classLoader.getResourceAsStream(this.path);
        }
        else {
            is = ClassLoader.getSystemResourceAsStream(this.path);
        }
        if (is == null) {
            throw new FileNotFoundException(getDescription() + " cannot be opened because it does not exist");
        }
        return is;
    }
```
