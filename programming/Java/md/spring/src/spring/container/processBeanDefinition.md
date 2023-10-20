# 解析bean标签

```java
public class DefaultBeanDefinitionDocumentReader implements BeanDefinitionDocumentReader {

    protected void processBeanDefinition(Element ele, BeanDefinitionParserDelegate delegate) {
        // 解析bean标签，创建BeanDefinition
        BeanDefinitionHolder bdHolder = delegate.parseBeanDefinitionElement(ele);
        if (bdHolder != null) {
            // 如果标签的子节点下再有自定义标签，还需要再次对自定义标签进行解析
            bdHolder = delegate.decorateBeanDefinitionIfRequired(ele, bdHolder);
            try {
                // 对解析后的bdHolder进行注册
                BeanDefinitionReaderUtils.registerBeanDefinition(bdHolder, getReaderContext().getRegistry());
            }
            catch (BeanDefinitionStoreException ex) {
                getReaderContext().error("Failed to register bean definition with name '" +
                        bdHolder.getBeanName() + "'", ele, ex);
            }
            // 通知相关的监听器，这个bean已经加载完成了
            getReaderContext().fireComponentRegistered(new BeanComponentDefinition(bdHolder));
        }
    }
}
```

## parseBeanDefinitionElement

首先委托BeanDefinitionParserDelegate::parseBeanDefinitionElement()方法进行元素解析，返回BeanDefinitionHolder类的实例bdHolder，经过这个方法后，bdHolder实例已经包含xml配置文件中bean标签配置的各种属性了，例如class、name、id、alias等属性。

```java
public class BeanDefinitionParserDelegate {

    public BeanDefinitionHolder parseBeanDefinitionElement(Element ele) {
        return parseBeanDefinitionElement(ele, null);
    }

    // 解析bean标签，如：<bean id="myTestBean" class="bean.MyTestBean">
    public BeanDefinitionHolder parseBeanDefinitionElement(
            Element ele, @Nullable BeanDefinition containingBean) {
        // 解析id属性，public static final String ID_ATTRIBUTE = "id";
        String id = ele.getAttribute(ID_ATTRIBUTE);
        // 解析name属性，public static final String NAME_ATTRIBUTE = "name";
        String nameAttr = ele.getAttribute(NAME_ATTRIBUTE);

        List<String> aliases = new ArrayList<>();
        if (StringUtils.hasLength(nameAttr)) {
            // name属性可以指定多个name，用逗号或者分号或者空格隔开，
            // 比如：<bean name="bean1,bean2,bean3" class="bean.MyTestBean">
            // public static final String MULTI_VALUE_ATTRIBUTE_DELIMITERS = ",; ";
            String[] nameArr = StringUtils.tokenizeToStringArray(nameAttr, MULTI_VALUE_ATTRIBUTE_DELIMITERS);
            // 所有name都作为别名
            aliases.addAll(Arrays.asList(nameArr));
        }

        String beanName = id;
        // 如果没指定id属性，则把第一个name作为bean的唯一标识
        if (!StringUtils.hasText(beanName) && !aliases.isEmpty()) {
            beanName = aliases.remove(0);
        }
        // bean的id属性要求唯一
        if (containingBean == null) {
            checkNameUniqueness(beanName, aliases, ele);
        }
        // 解析其他属性
        AbstractBeanDefinition beanDefinition = parseBeanDefinitionElement(ele, beanName, containingBean);
        if (beanDefinition != null) {
            if (!StringUtils.hasText(beanName)) {
                try {
                    // 如果bean标签未指定id和name属性，则spring会给其一个默认的id，值为其类全名
                    if (containingBean != null) {
                        beanName = BeanDefinitionReaderUtils.generateBeanName(
                                beanDefinition, this.readerContext.getRegistry(), true);
                    }
                    else {
                        // 处理bean的别名
                        // 首先获取bean的类名，然后检查这个类名是否与bean的名称相同，并且这个类名没有被使用过
                        // 如果满足这些条件，那么就将这个类名添加到别名列表中
                        // 这样做是为了解决Spring 1.2/2.0向后兼容性的问题
                        beanName = this.readerContext.generateBeanName(beanDefinition);
                        String beanClassName = beanDefinition.getBeanClassName();
                        if (beanClassName != null &&
                                beanName.startsWith(beanClassName) && 
                                beanName.length() > beanClassName.length() &&
                                !this.readerContext.getRegistry().isBeanNameInUse(beanClassName)) {
                            aliases.add(beanClassName);
                        }
                    }
                }
                catch (Exception ex) {
                    error(ex.getMessage(), ele);
                    return null;
                }
            }
            String[] aliasesArray = StringUtils.toStringArray(aliases);
            // 将获取到的信息封装到BeanDefinitionHolder的实例中
            return new BeanDefinitionHolder(beanDefinition, beanName, aliasesArray);
        }

        return null;
    }

    // 解析bean标签的其他属性
    public AbstractBeanDefinition parseBeanDefinitionElement(
            Element ele, String beanName, @Nullable BeanDefinition containingBean) {
        // 记录正在解析的bean
        this.parseState.push(new BeanEntry(beanName));
        // 解析class属性，public static final String CLASS_ATTRIBUTE = "class";
        String className = null;
        if (ele.hasAttribute(CLASS_ATTRIBUTE)) {
            className = ele.getAttribute(CLASS_ATTRIBUTE).trim();
        }
        // 解析parent属性，public static final String PARENT_ATTRIBUTE = "parent";
        String parent = null;
        if (ele.hasAttribute(PARENT_ATTRIBUTE)) {
            parent = ele.getAttribute(PARENT_ATTRIBUTE);
        }

        try {
            // 创建BeanDefinition
            AbstractBeanDefinition bd = createBeanDefinition(className, parent);
            // 解析bean的singleton、scope、abstract等属性
            parseBeanDefinitionAttributes(ele, beanName, containingBean, bd);
            // 提取description子标签的值，description标签用于设置描述信息
            bd.setDescription(DomUtils.getChildElementValueByTagName(ele, DESCRIPTION_ELEMENT));

            // 解析meta子标签，description标签用于设置元数据
            parseMetaElements(ele, bd);
            // 解析lookup-method子标签
            parseLookupOverrideSubElements(ele, bd.getMethodOverrides());
            // 解析replaced-method子标签
            parseReplacedMethodSubElements(ele, bd.getMethodOverrides());
            // 解析构造方法参数
            parseConstructorArgElements(ele, bd);
            // 解析property子标签
            parsePropertyElements(ele, bd);
            // 解析qualifier子标签
            parseQualifierElements(ele, bd);

            bd.setResource(this.readerContext.getResource());
            bd.setSource(extractSource(ele));

            return bd;
        }
        catch (ClassNotFoundException ex) {
            error("Bean class [" + className + "] not found", ele, ex);
        }
        catch (NoClassDefFoundError err) {
            error("Class that bean class [" + className + "] depends on not found", ele, err);
        }
        catch (Throwable ex) {
            error("Unexpected failure during bean definition parsing", ele, ex);
        }
        finally {
            // 解析完了
            this.parseState.pop();
        }

        return null;
    }
}
```
