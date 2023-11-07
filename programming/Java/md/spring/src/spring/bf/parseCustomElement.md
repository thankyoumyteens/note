# 解析自定义标签

```java
public class BeanDefinitionParserDelegate {

    public BeanDefinition parseCustomElement(Element ele) {
        return parseCustomElement(ele, null);
    }

    public BeanDefinition parseCustomElement(Element ele, @Nullable BeanDefinition containingBd) {
        // 获取自定义标签的命名空间
        String namespaceUri = getNamespaceURI(ele);
        if (namespaceUri == null) {
            return null;
        }
        // 根据命名空间找到自定义的解析器
        NamespaceHandler handler = this.readerContext.getNamespaceHandlerResolver().resolve(namespaceUri);
        if (handler == null) {
            error("Unable to locate Spring NamespaceHandler for XML schema namespace [" + namespaceUri + "]", ele);
            return null;
        }
        // 使用自定义解析器解析自定义标签
        return handler.parse(ele, new ParserContext(this.readerContext, this, containingBd));
    }
}
```

## 根据命名空间找到自定义的解析器

this.readerContext.getNamespaceHandlerResolver()会返回一个 DefaultNamespaceHandlerResolver 的对象。

```java
public class DefaultNamespaceHandlerResolver implements NamespaceHandlerResolver {

    public NamespaceHandler resolve(String namespaceUri) {
        // 获取解析器map
        // 这个map是一个缓存，一开始valu中会存储解析器的类名，
        // 使用过一次后就会把类名替换成解析器的对象
        Map<String, Object> handlerMappings = getHandlerMappings();
        // 根据命名空间找到对应的NamespaceHandler
        Object handlerOrClassName = handlerMappings.get(namespaceUri);
        if (handlerOrClassName == null) {
            return null;
        } else if (handlerOrClassName instanceof NamespaceHandler) {
            // 已经是个对象了，表示之前获取过，直接返回
            return (NamespaceHandler) handlerOrClassName;
        } else {
            // map里存的不是NamespaceHandler对象，表示第一次获取
            // 解析器的类全名
            String className = (String) handlerOrClassName;
            try {
                // 根据类名创建一个解析器对象
                Class<?> handlerClass = ClassUtils.forName(className, this.classLoader);
                if (!NamespaceHandler.class.isAssignableFrom(handlerClass)) {
                    throw new FatalBeanException("Class [" + className + "] for namespace [" + namespaceUri +
                            "] does not implement the [" + NamespaceHandler.class.getName() + "] interface");
                }
                NamespaceHandler namespaceHandler = (NamespaceHandler) BeanUtils.instantiateClass(handlerClass);
                // 调用init()方法
                // 用户需要重写这个方法，
                // 并在其中指定一个BeanDefinitionParser类型的对象
                // 实际解析自定义标签的代码就写在BeanDefinitionParser类型的对象中
                namespaceHandler.init();
                // 把map里的类名替换成实际的对象
                handlerMappings.put(namespaceUri, namespaceHandler);
                return namespaceHandler;
            } catch (ClassNotFoundException ex) {
                throw new FatalBeanException("Could not find NamespaceHandler class [" + className +
                        "] for namespace [" + namespaceUri + "]", ex);
            } catch (LinkageError err) {
                throw new FatalBeanException("Unresolvable class definition for NamespaceHandler class [" +
                        className + "] for namespace [" + namespaceUri + "]", err);
            }
        }
    }

    // 获取解析器map
    private Map<String, Object> getHandlerMappings() {
        // private volatile Map<String, Object> handlerMappings;
        Map<String, Object> handlerMappings = this.handlerMappings;
        // 懒加载
        if (handlerMappings == null) {
            synchronized (this) {
                handlerMappings = this.handlerMappings;
                // 双重检查锁(DCL)，handlerMappings是volatile的，可以禁止重排序
                if (handlerMappings == null) {
                    try {
                        // 加载自定义的NamespaceHandler
                        // handlerMappingsLocation已经在构造方法中初始化为：META-INF/spring.handlers
                        // public static final String DEFAULT_HANDLER_MAPPINGS_LOCATION = "META-INF/spring.handlers";
                        /*
                        public DefaultNamespaceHandlerResolver(@Nullable ClassLoader classLoader) {
                            this(classLoader, DEFAULT_HANDLER_MAPPINGS_LOCATION);
                        }
                         */
                        // spring.handlers是一个properties文件，key是自定义命名空间，value是解析这个命名空间的解析器的类名
                        Properties mappings = PropertiesLoaderUtils.loadAllProperties(this.handlerMappingsLocation, this.classLoader);
                        // 存入map
                        handlerMappings = new ConcurrentHashMap<>(mappings.size());
                        CollectionUtils.mergePropertiesIntoMap(mappings, handlerMappings);
                        this.handlerMappings = handlerMappings;
                    }
                    catch (IOException ex) {
                        throw new IllegalStateException(
                                "Unable to load NamespaceHandler mappings from location [" + this.handlerMappingsLocation + "]", ex);
                    }
                }
            }
        }
        return handlerMappings;
    }
}
```

## handler.parse()方法

自定义解析器可以继承自 NamespaceHandlerSupport 抽象类，这样只需要自己实现 init()方法，其他方法使用 NamespaceHandlerSupport 中默认的即可：

```java
public class MyNamespaceHandler extends NamespaceHandlerSupport {
    public void init() {
        registerBeanDefinitionParser("mytag", new MyBeanDefinitionParser());
    }
}
```

假设 handler.parse()方法调用的是 NamespaceHandlerSupport::parse()方法。

```java
public abstract class NamespaceHandlerSupport implements NamespaceHandler {

    public BeanDefinition parse(Element element, ParserContext parserContext) {
        // 找到用户指定的BeanDefinitionParser对象
        BeanDefinitionParser parser = findParserForElement(element, parserContext);
        // 解析自定义标签
        // 如果用户通过继承AbstractSingleBeanDefinitionParser类来实现自定义解析器，
        // 那么他需要重写parse()方法中的doParse()方法
        // 如果用户通过实现BeanDefinitionParser接口来实现自定义解析器，
        // 那么他需要实现整个parse()方法，并在其中自己注册bean
        return (parser != null ? parser.parse(element, parserContext) : null);
    }

    private BeanDefinitionParser findParserForElement(Element element, ParserContext parserContext) {
        // 比如<tx:annotation-driven transaction-manager="transactionManager"/>
        // 其中tx是命名空间
        // annotation-driven就是localName
        String localName = parserContext.getDelegate().getLocalName(element);
        // 获取NamespaceHandler中指定的BeanDefinitionParser
        BeanDefinitionParser parser = this.parsers.get(localName);
        if (parser == null) {
            parserContext.getReaderContext().fatal(
                    "Cannot locate BeanDefinitionParser for element [" + localName + "]", element);
        }
        return parser;
    }
}
```

## 通过继承 AbstractSingleBeanDefinitionParser 类来实现自定义解析器

与 NamespaceHandler 类似，自定义的 BeanDefinitionParser 实现类也可以继承 AbstractSingleBeanDefinitionParser 以减少代码量。

```java
public abstract class AbstractSingleBeanDefinitionParser extends AbstractBeanDefinitionParser {

    /**
     * parse()方法是AbstractSingleBeanDefinitionParser的父类中的方法
     */
    public final BeanDefinition parse(Element element, ParserContext parserContext) {
        // 把自定义标签解析成BeanDefinition
        AbstractBeanDefinition definition = parseInternal(element, parserContext);
        // 注册bean
        if (definition != null && !parserContext.isNested()) {
            try {
                String id = resolveId(element, definition, parserContext);
                if (!StringUtils.hasText(id)) {
                    parserContext.getReaderContext().error(
                            "Id is required for element '" + parserContext.getDelegate().getLocalName(element)
                                    + "' when used as a top-level tag", element);
                }
                String[] aliases = null;
                // 处理别名
                if (shouldParseNameAsAliases()) {
                    String name = element.getAttribute(NAME_ATTRIBUTE);
                    if (StringUtils.hasLength(name)) {
                        aliases = StringUtils.trimArrayElements(StringUtils.commaDelimitedListToStringArray(name));
                    }
                }
                BeanDefinitionHolder holder = new BeanDefinitionHolder(definition, id, aliases);
                // 注册bean
                registerBeanDefinition(holder, parserContext.getRegistry());
                if (shouldFireEvents()) {
                    // 通知监听器进行处理
                    BeanComponentDefinition componentDefinition = new BeanComponentDefinition(holder);
                    postProcessComponentDefinition(componentDefinition);
                    parserContext.registerComponent(componentDefinition);
                }
            }
            catch (BeanDefinitionStoreException ex) {
                String msg = ex.getMessage();
                parserContext.getReaderContext().error((msg != null ? msg : ex.toString()), element);
                return null;
            }
        }
        return definition;
    }

    /**
     * 把自定义标签解析成BeanDefinition
     */
    protected final AbstractBeanDefinition parseInternal(Element element, ParserContext parserContext) {
        // 构建GenericBeanDefinition
        BeanDefinitionBuilder builder = BeanDefinitionBuilder.genericBeanDefinition();
        // 处理上级标签
        String parentName = getParentName(element);
        if (parentName != null) {
            builder.getRawBeanDefinition().setParentName(parentName);
        }
        // 获取自定义标签中的类
        // 用户需要重写getBeanClass()方法
        Class<?> beanClass = getBeanClass(element);
        if (beanClass != null) {
            builder.getRawBeanDefinition().setBeanClass(beanClass);
        } else {
            // 如果不想重写getBeanClass()方法
            // 也可以重写getBeanClassName()方法
            String beanClassName = getBeanClassName(element);
            if (beanClassName != null) {
                builder.getRawBeanDefinition().setBeanClassName(beanClassName);
            }
        }
        builder.getRawBeanDefinition().setSource(parserContext.extractSource(element));
        BeanDefinition containingBd = parserContext.getContainingBeanDefinition();
        // 若存在父bean，则使用父bean的scope属性
        if (containingBd != null) {
            builder.setScope(containingBd.getScope());
        }
        // 是否延迟加载bean
        if (parserContext.isDefaultLazyInit()) {
            builder.setLazyInit(true);
        }
        // 用户需要重写doParse()方法
        doParse(element, parserContext, builder);
        // 构建BeanDefinition
        return builder.getBeanDefinition();
    }

    protected void doParse(Element element, ParserContext parserContext, BeanDefinitionBuilder builder) {
        doParse(element, builder);
    }

    // 空的，用户需要重写，在这里解析标签里自己的属性
    protected void doParse(Element element, BeanDefinitionBuilder builder) {}
}
```
