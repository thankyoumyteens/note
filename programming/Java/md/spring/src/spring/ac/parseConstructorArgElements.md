# 解析 constructor-arg 子标签

```java
public class BeanDefinitionParserDelegate {

    public void parseConstructorArgElements(Element beanEle, BeanDefinition bd) {
        // 遍历bean的子标签
        NodeList nl = beanEle.getChildNodes();
        for (int i = 0; i < nl.getLength(); i++) {
            Node node = nl.item(i);
            if (isCandidateElement(node) && nodeNameEquals(node, CONSTRUCTOR_ARG_ELEMENT)) {
                // 解析constructor-arg子标签
                parseConstructorArgElement((Element) node, bd);
            }
        }
    }

    public void parseConstructorArgElement(Element ele, BeanDefinition bd) {
        // 获取index属性
        String indexAttr = ele.getAttribute(INDEX_ATTRIBUTE);
        // 获取type属性
        String typeAttr = ele.getAttribute(TYPE_ATTRIBUTE);
        // 获取name属性
        String nameAttr = ele.getAttribute(NAME_ATTRIBUTE);
        if (StringUtils.hasLength(indexAttr)) {
            // 如果指定了index属性
            try {
                int index = Integer.parseInt(indexAttr);
                // index从0开始
                if (index < 0) {
                    error("'index' cannot be lower than 0", ele);
                } else {
                    try {
                        this.parseState.push(new ConstructorArgumentEntry(index));
                        // 解析constructor-arg的值
                        Object value = parsePropertyValue(ele, bd, null);
                        // 把constructor-arg的值、type属性、name属性封装到ValueHolder中
                        ConstructorArgumentValues.ValueHolder valueHolder = new ConstructorArgumentValues.ValueHolder(value);
                        if (StringUtils.hasLength(typeAttr)) {
                            valueHolder.setType(typeAttr);
                        }
                        if (StringUtils.hasLength(nameAttr)) {
                            valueHolder.setName(nameAttr);
                        }
                        valueHolder.setSource(extractSource(ele));
                        // index已存在, 不允许重复指定
                        if (bd.getConstructorArgumentValues().hasIndexedArgumentValue(index)) {
                            error("Ambiguous constructor-arg entries for index " + index, ele);
                        } else {
                            // 添加到BeanDefinition的constructorArgumentValues中
                            // index属性存储到indexedArgumentValues中
                            bd.getConstructorArgumentValues().addIndexedArgumentValue(index, valueHolder);
                        }
                    } finally {
                        this.parseState.pop();
                    }
                }
            } catch (NumberFormatException ex) {
                error("Attribute 'index' of tag 'constructor-arg' must be an integer", ele);
            }
        } else {
            // 如果没有指定index属性
            try {
                this.parseState.push(new ConstructorArgumentEntry());
                // 解析constructor-arg的值
                Object value = parsePropertyValue(ele, bd, null);
                // 把constructor-arg的值、type属性、name属性封装到ValueHolder中
                ConstructorArgumentValues.ValueHolder valueHolder = new ConstructorArgumentValues.ValueHolder(value);
                if (StringUtils.hasLength(typeAttr)) {
                    valueHolder.setType(typeAttr);
                }
                if (StringUtils.hasLength(nameAttr)) {
                    valueHolder.setName(nameAttr);
                }
                valueHolder.setSource(extractSource(ele));
                // 添加到BeanDefinition的constructorArgumentValues中
                // 没有指定index属性时, 把属性存储到genericArgumentValues中
                bd.getConstructorArgumentValues().addGenericArgumentValue(valueHolder);
            }
            finally {
                this.parseState.pop();
            }
        }
    }

    // 获取constructor-arg的值
    public Object parsePropertyValue(Element ele, BeanDefinition bd, @Nullable String propertyName) {
        String elementName = (propertyName != null ?
                "<property> element for property '" + propertyName + "'" :
                "<constructor-arg> element");
        /*
         * constructor-arg的值有两种配置形式
         *
         * 1. 使用value/ref属性: 
         * <bean class="test.Student">
         *   <constructor-arg name="name" value="张三"></constructor-arg>
         * </bean>
         *
         * 2. 使用value/ref/list/map等子标签: 
         * <bean class="test.Student">
         *   <constructor-arg name="num">
         *     <list>
         *       <value>1</value>
         *       <value>2</value>
         *     </list>
         *   </constructor-arg>
         * </bean>
         */

        // 获取子标签
        NodeList nl = ele.getChildNodes();
        Element subElement = null;
        for (int i = 0; i < nl.getLength(); i++) {
            Node node = nl.item(i);
            // 不解析description和meta标签
            if (node instanceof Element && !nodeNameEquals(node, DESCRIPTION_ELEMENT) &&
                    !nodeNameEquals(node, META_ELEMENT)) {
                // 每个constructor-arg只能有1个子标签
                if (subElement != null) {
                    error(elementName + " must not contain more than one sub-element", ele);
                }
                else {
                    subElement = (Element) node;
                }
            }
        }
        // 获取value/ref属性
        boolean hasRefAttribute = ele.hasAttribute(REF_ATTRIBUTE);
        boolean hasValueAttribute = ele.hasAttribute(VALUE_ATTRIBUTE);
        if ((hasRefAttribute && hasValueAttribute) ||
                ((hasRefAttribute || hasValueAttribute) && subElement != null)) {
            // 子标签、ref属性、value属性不能同时存在
            error(elementName +
                    " is only allowed to contain either 'ref' attribute OR 'value' attribute OR sub-element", ele);
        }

        if (hasRefAttribute) {
            // 如果constructor-arg指定了ref属性
            String refName = ele.getAttribute(REF_ATTRIBUTE);
            if (!StringUtils.hasText(refName)) {
                error(elementName + " contains empty 'ref' attribute", ele);
            }
            // 把ref属性封装成RuntimeBeanReference
            RuntimeBeanReference ref = new RuntimeBeanReference(refName);
            ref.setSource(extractSource(ele));
            return ref;
        } else if (hasValueAttribute) {
            // 如果constructor-arg指定了value属性
            // 把value属性封装成TypedStringValue
            TypedStringValue valueHolder = new TypedStringValue(ele.getAttribute(VALUE_ATTRIBUTE));
            valueHolder.setSource(extractSource(ele));
            return valueHolder;
        } else if (subElement != null) {
            // 如果指定了子标签, 就去解析子标签
            return parsePropertySubElement(subElement, bd);
        } else {
            error(elementName + " must specify a ref or value", ele);
            return null;
        }
    }

    /**
     * 解析constructor-arg的子标签
     */
    public Object parsePropertySubElement(Element ele, @Nullable BeanDefinition bd) {
        return parsePropertySubElement(ele, bd, null);
    }

    public Object parsePropertySubElement(Element ele, @Nullable BeanDefinition bd, @Nullable String defaultValueType) {
        if (!isDefaultNamespace(ele)) {
            // 自定义标签
            return parseNestedCustomElement(ele, bd);
        } else if (nodeNameEquals(ele, BEAN_ELEMENT)) {
            // bean标签
            BeanDefinitionHolder nestedBd = parseBeanDefinitionElement(ele, bd);
            if (nestedBd != null) {
                nestedBd = decorateBeanDefinitionIfRequired(ele, nestedBd, bd);
            }
            return nestedBd;
        } else if (nodeNameEquals(ele, REF_ELEMENT)) {
            // ref标签
            String refName = ele.getAttribute(BEAN_REF_ATTRIBUTE);
            boolean toParent = false;
            if (!StringUtils.hasLength(refName)) {
                // 去parent中查找bean
                refName = ele.getAttribute(PARENT_REF_ATTRIBUTE);
                toParent = true;
                if (!StringUtils.hasLength(refName)) {
                    error("'bean' or 'parent' is required for <ref> element", ele);
                    return null;
                }
            }
            if (!StringUtils.hasText(refName)) {
                error("<ref> element contains empty target attribute", ele);
                return null;
            }
            RuntimeBeanReference ref = new RuntimeBeanReference(refName, toParent);
            ref.setSource(extractSource(ele));
            return ref;
        } else if (nodeNameEquals(ele, IDREF_ELEMENT)) {
            // idref标签
            return parseIdRefElement(ele);
        } else if (nodeNameEquals(ele, VALUE_ELEMENT)) {
            // value标签
            return parseValueElement(ele, defaultValueType);
        } else if (nodeNameEquals(ele, NULL_ELEMENT)) {
            // null标签
            TypedStringValue nullHolder = new TypedStringValue(null);
            nullHolder.setSource(extractSource(ele));
            return nullHolder;
        } else if (nodeNameEquals(ele, ARRAY_ELEMENT)) {
            // array标签
            return parseArrayElement(ele, bd);
        } else if (nodeNameEquals(ele, LIST_ELEMENT)) {
            // list标签
            return parseListElement(ele, bd);
        } else if (nodeNameEquals(ele, SET_ELEMENT)) {
            // set标签
            return parseSetElement(ele, bd);
        } else if (nodeNameEquals(ele, MAP_ELEMENT)) {
            // map标签
            return parseMapElement(ele, bd);
        } else if (nodeNameEquals(ele, PROPS_ELEMENT)) {
            // props标签
            return parsePropsElement(ele);
        } else {
            error("Unknown property sub-element: [" + ele.getNodeName() + "]", ele);
            return null;
        }
    }
}
```
