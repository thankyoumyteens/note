# 解析 bean 标签

把一个 bean 标签解析成 BeanDefinition 的过程：

1. spring 会为每个 bean 创建一个全局唯一的 beanName
2. 首先取出 id 属性和 name 属性，如果设置了 id，就把 id 作为 beanName
3. 如果没有设置 id，就把 name 作为 beanName，由于 name 属性可以设置多个(用逗号分隔)，spring 会把第一个 name 设置为 beanName，其他的 name 就当成这个 bean 的别名
4. 如果 id 和 name 都没有设置，spring 会自己生成一个唯一的 beanName
5. 然后 spring 会创建一个 BeanDefinition，并把 bean 标签的属性和子标签都存储到 BeanDefinition 中对应的字段上
6. 最后 spring 会把 BeanDefinition 封装到一个 BeanDefinitionHolder 中返回

```java
public class DefaultBeanDefinitionDocumentReader implements BeanDefinitionDocumentReader {

    protected void processBeanDefinition(Element ele, BeanDefinitionParserDelegate delegate) {

        // 把bean标签解析成BeanDefinition
        BeanDefinitionHolder bdHolder = delegate.parseBeanDefinitionElement(ele);
        if (bdHolder != null) {
            // 如果标签的子节点下再有自定义标签，还需要再次对自定义标签进行解析
            bdHolder = delegate.decorateBeanDefinitionIfRequired(ele, bdHolder);
            try {
                // 对解析后的bdHolder进行注册
                BeanDefinitionReaderUtils.registerBeanDefinition(bdHolder, getReaderContext().getRegistry());
            }
            catch (BeanDefinitionStoreException ex) {
                // ...
            }
            // 通知相关的监听器，这个bean已经加载完成了
            getReaderContext().fireComponentRegistered(new BeanComponentDefinition(bdHolder));
        }
    }
}

public class BeanDefinitionParserDelegate {

    public BeanDefinitionHolder parseBeanDefinitionElement(Element ele) {
        return parseBeanDefinitionElement(ele, null);
    }

    // 解析bean标签
    public BeanDefinitionHolder parseBeanDefinitionElement(
            Element ele, @Nullable BeanDefinition containingBean) {
        // 获取id属性
        String id = ele.getAttribute(ID_ATTRIBUTE);
        // 获取name属性
        String nameAttr = ele.getAttribute(NAME_ATTRIBUTE);
        // aliases用来存储bean的别名
        List<String> aliases = new ArrayList<>();
        // 是否设置了name属性
        if (StringUtils.hasLength(nameAttr)) {
            // name属性可以指定多个name，用逗号或者分号或者空格隔开，
            // 比如：<bean name="bean1,bean2;bean3" class="xxx">
            String[] nameArr = StringUtils.tokenizeToStringArray(nameAttr, MULTI_VALUE_ATTRIBUTE_DELIMITERS);
            // 先把所有name都作为别名
            aliases.addAll(Arrays.asList(nameArr));
        }
        // 把id作为beanName
        String beanName = id;
        // 如果没设置id属性，并且设置了name属性
        if (!StringUtils.hasText(beanName) && !aliases.isEmpty()) {
            // 把第一个name作为bean的唯一标识，并把它从别名中移除
            beanName = aliases.remove(0);
        }
        if (containingBean == null) {
            // 检查beanName是否唯一
            checkNameUniqueness(beanName, aliases, ele);
        }
        // 获取bean标签的其他属性，并创建BeanDefinition
        AbstractBeanDefinition beanDefinition = parseBeanDefinitionElement(ele, beanName, containingBean);
        // 判断BeanDefinition是否创建成功
        if (beanDefinition != null) {
            // 判断beanName有没有设置上
            if (!StringUtils.hasText(beanName)) {
                // beanName没有设置上，即bean标签没有设置id和name属性
                try {
                    // 如果bean标签没有设置id和name属性，
                    // 那么spring会自己生成一个beanName，值为其类全名
                    if (containingBean != null) {
                        // 为嵌套的bean生成beanName
                        // bean里可以嵌套bean，嵌套bean配置的对象仅作为setter方法的参数
                        // 嵌套bean不能被容器访问，因此无需指定id和name
                        beanName = BeanDefinitionReaderUtils.generateBeanName(
                                beanDefinition, this.readerContext.getRegistry(), true);
                    } else {
                        // 为普通的bean生成beanName
                        beanName = this.readerContext.generateBeanName(beanDefinition);
                        // 下面的代码用于解决Spring 1.2/2.0向后兼容性的问题：
                        // 首先获取bean的类名，然后检查这个类名是否与bean的名称相同，
                        // 并且这个类名没有被使用过，
                        // 如果满足这些条件，那么就将这个类名添加到别名列表中
                        String beanClassName = beanDefinition.getBeanClassName();
                        if (beanClassName != null &&
                                beanName.startsWith(beanClassName) &&
                                beanName.length() > beanClassName.length() &&
                                !this.readerContext.getRegistry().isBeanNameInUse(beanClassName)) {
                            aliases.add(beanClassName);
                        }
                    }
                } catch (Exception ex) {
                    error(ex.getMessage(), ele);
                    return null;
                }
            }
            String[] aliasesArray = StringUtils.toStringArray(aliases);
            // 将BeanDefinition封装到BeanDefinitionHolder中
            // BeanDefinitionHolder里面就3个字段：
            // private final BeanDefinition beanDefinition;
            // private final String beanName;
            // private final String[] aliases;
            return new BeanDefinitionHolder(beanDefinition, beanName, aliasesArray);
        }
        // 解析失败
        return null;
    }

    // 获取bean标签的其他属性，并创建BeanDefinition
    public AbstractBeanDefinition parseBeanDefinitionElement(
            Element ele, String beanName, @Nullable BeanDefinition containingBean) {
        // 记录正在处理的beanName
        this.parseState.push(new BeanEntry(beanName));
        // 获取class属性，CLASS_ATTRIBUTE = "class";
        String className = null;
        if (ele.hasAttribute(CLASS_ATTRIBUTE)) {
            className = ele.getAttribute(CLASS_ATTRIBUTE).trim();
        }
        // 获取parent属性，PARENT_ATTRIBUTE = "parent";
        String parent = null;
        if (ele.hasAttribute(PARENT_ATTRIBUTE)) {
            parent = ele.getAttribute(PARENT_ATTRIBUTE);
        }

        try {
            // 创建BeanDefinition
            AbstractBeanDefinition bd = createBeanDefinition(className, parent);
            // 获取bean的singleton、scope、abstract等其他属性
            parseBeanDefinitionAttributes(ele, beanName, containingBean, bd);
            // 解析description子标签，description标签用于设置bean的描述信息
            bd.setDescription(DomUtils.getChildElementValueByTagName(ele, DESCRIPTION_ELEMENT));
            // 解析meta子标签，meta标签用于设置bean的元数据
            parseMetaElements(ele, bd);
            // 解析lookup-method子标签
            parseLookupOverrideSubElements(ele, bd.getMethodOverrides());
            // 解析replaced-method子标签
            parseReplacedMethodSubElements(ele, bd.getMethodOverrides());
            // 解析constructor-arg子标签
            parseConstructorArgElements(ele, bd);
            // 解析property子标签
            parsePropertyElements(ele, bd);
            // 解析qualifier子标签
            parseQualifierElements(ele, bd);
            // 记录bean的来源xml文件
            bd.setResource(this.readerContext.getResource());
            bd.setSource(extractSource(ele));

            return bd;
        } catch (ClassNotFoundException ex) {
            // ...
        } finally {
            // 解析完了
            this.parseState.pop();
        }
        // 执行到这，表示抛异常了，解析失败
        return null;
    }
}
```
