# 定义资源

资源可以是任何东西: 服务，服务里的方法，甚至是一段代码。使用 Sentinel 来进行资源保护，主要分为几个步骤:

1. 定义资源
2. 定义规则
3. 检验规则是否生效

先把可能需要保护的资源定义好，之后再配置规则。也可以理解为，只要有了资源，我们就可以在任何时候灵活地定义各种流量控制规则。在编码的时候，只需要考虑这个代码是否需要保护，如果需要保护，就将之定义为一个资源。

对于主流的框架，Sentinel 会默认定义提供的服务，方法等为资源。

## 通过注解定义资源

Sentinel 支持通过 `@SentinelResource` 注解定义资源并配置 blockHandler 和 fallback 函数来进行限流之后的处理。

`@SentinelResource` 注解包含以下属性：

- value：资源名称，必填
- entryType：entry 类型，默认为 EntryType.OUT
- blockHandler: blockHandler 对应处理 BlockException 的函数名称。blockHandler 函数需要是 public，返回类型需要与原方法相匹配，参数类型需要和原方法相匹配并且最后加一个额外的参数，类型为 BlockException。blockHandler 函数默认需要和原方法在同一个类中。若希望使用其他类的函数，则可以指定 blockHandlerClass 为对应的类的 Class 对象，注意对应的函数必需为 static 函数，否则无法解析
- fallback：用于在抛出异常的时候提供自定义处理逻辑。fallback 函数可以针对所有类型的异常(除了 exceptionsToIgnore 里面排除掉的异常类型)进行处理。fallback 函数签名和位置要求：
  - 返回值类型必须与原函数返回值类型一致
  - 方法参数列表需要和原函数一致，或者可以额外多一个 Throwable 类型的参数用于接收对应的异常
  - fallback 函数默认需要和原方法在同一个类中。若希望使用其他类的函数，则可以指定 fallbackClass 为对应的类的 Class 对象，注意对应的函数必需为 static 函数，否则无法解析
- defaultFallback: 默认的 fallback 函数名称，通常用于通用的 fallback 逻辑(即可以用于很多服务或方法)。若同时配置了 fallback 和 defaultFallback，则只有 fallback 会生效
- exceptionsToIgnore: 用于指定哪些异常被排除掉，不会计入异常统计中，也不会进入 fallback 逻辑中，而是会原样抛出

若 blockHandler 和 fallback 都进行了配置，则被限流降级而抛出 BlockException 时只会进入 blockHandler 处理逻辑。若未配置 blockHandler、fallback 和 defaultFallback，则被限流降级时会将 BlockException 直接抛出。

```java
public class TestService {

    // 对应的 handleException 函数需要位于 ExceptionUtil 类中，并且必须为 static 函数
    @SentinelResource(value = "test", blockHandler = "handleException", blockHandlerClass = {ExceptionUtil.class})
    public void test() {
        System.out.println("Test");
    }

    @SentinelResource(value = "hello", blockHandler = "exceptionHandler", fallback = "helloFallback")
    public String hello(long s) {
        return String.format("Hello at %d", s);
    }

    // Fallback 函数，函数签名与hello函数一致或加一个 Throwable 类型的参数
    public String helloFallback(long s) {
        return String.format("Halooooo %d", s);
    }

    // Block 异常处理函数，参数最后多一个 BlockException，其余与原函数一致
    public String exceptionHandler(long s, BlockException ex) {
        // Do some log here.
        ex.printStackTrace();
        return "Oops, error occurred at " + s;
    }
}
```
