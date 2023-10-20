# 获取bean的其他属性

获取bean标签的各种属性。

```java
public class BeanDefinitionParserDelegate {

    public AbstractBeanDefinition parseBeanDefinitionAttributes(Element ele, String beanName,
            @Nullable BeanDefinition containingBean, AbstractBeanDefinition bd) {

        // 获取scope属性
        if (ele.hasAttribute(SINGLETON_ATTRIBUTE)) {
            // singleton属性不再被支持，需要使用scope属性替代
            error("Old 1.x 'singleton' attribute in use - upgrade to 'scope' declaration", ele);
        } else if (ele.hasAttribute(SCOPE_ATTRIBUTE)) {
            // 获取scope属性
            bd.setScope(ele.getAttribute(SCOPE_ATTRIBUTE));
        } else if (containingBean != null) {
            // 如果是内嵌bean，则使用上级bean的scope值
            bd.setScope(containingBean.getScope());
        }

        // 获取abstract属性
        if (ele.hasAttribute(ABSTRACT_ATTRIBUTE)) {
            bd.setAbstract(TRUE_VALUE.equals(ele.getAttribute(ABSTRACT_ATTRIBUTE)));
        }

        // 获取lazy-init属性
        String lazyInit = ele.getAttribute(LAZY_INIT_ATTRIBUTE);
        if (isDefaultValue(lazyInit)) {
            // 若没有设置或者设置成其他字符都会被设置为默认值false
            lazyInit = this.defaults.getLazyInit();
        }
        bd.setLazyInit(TRUE_VALUE.equals(lazyInit));

        // 获取autowire属性
        String autowire = ele.getAttribute(AUTOWIRE_ATTRIBUTE);
        bd.setAutowireMode(getAutowireMode(autowire));

        // 获取depends-on属性
        if (ele.hasAttribute(DEPENDS_ON_ATTRIBUTE)) {
            String dependsOn = ele.getAttribute(DEPENDS_ON_ATTRIBUTE);
            bd.setDependsOn(StringUtils.tokenizeToStringArray(dependsOn, MULTI_VALUE_ATTRIBUTE_DELIMITERS));
        }

        // 获取autowire-candidate属性，该属性为false代表该bean不会被选为自动注入的对象
        String autowireCandidate = ele.getAttribute(AUTOWIRE_CANDIDATE_ATTRIBUTE);
        if (isDefaultValue(autowireCandidate)) {
            String candidatePattern = this.defaults.getAutowireCandidates();
            if (candidatePattern != null) {
                String[] patterns = StringUtils.commaDelimitedListToStringArray(candidatePattern);
                bd.setAutowireCandidate(PatternMatchUtils.simpleMatch(patterns, beanName));
            }
        } else {
            // 默认为true
            bd.setAutowireCandidate(TRUE_VALUE.equals(autowireCandidate));
        }

        // 获取primary属性
        if (ele.hasAttribute(PRIMARY_ATTRIBUTE)) {
            bd.setPrimary(TRUE_VALUE.equals(ele.getAttribute(PRIMARY_ATTRIBUTE)));
        }

        // 获取init-method属性
        if (ele.hasAttribute(INIT_METHOD_ATTRIBUTE)) {
            String initMethodName = ele.getAttribute(INIT_METHOD_ATTRIBUTE);
            bd.setInitMethodName(initMethodName);
        } else if (this.defaults.getInitMethod() != null) {
            // 如果bean没有指定init-method属性，
            // 但beans标签指定了default-init-method属性，
            // 则会使用该属性
            bd.setInitMethodName(this.defaults.getInitMethod());
            bd.setEnforceInitMethod(false);
        }

        // 获取destroy-method属性
        if (ele.hasAttribute(DESTROY_METHOD_ATTRIBUTE)) {
            String destroyMethodName = ele.getAttribute(DESTROY_METHOD_ATTRIBUTE);
            bd.setDestroyMethodName(destroyMethodName);
        } else if (this.defaults.getDestroyMethod() != null) {
            // 如果bean没有指定destroy-method属性，
            // 但beans标签指定了default-destroy-method属性，
            // 则会使用该属性
            bd.setDestroyMethodName(this.defaults.getDestroyMethod());
            bd.setEnforceDestroyMethod(false);
        }

        // 获取factory-method属性
        if (ele.hasAttribute(FACTORY_METHOD_ATTRIBUTE)) {
            bd.setFactoryMethodName(ele.getAttribute(FACTORY_METHOD_ATTRIBUTE));
        }

        // 获取factory-bean属性
        if (ele.hasAttribute(FACTORY_BEAN_ATTRIBUTE)) {
            bd.setFactoryBeanName(ele.getAttribute(FACTORY_BEAN_ATTRIBUTE));
        }

        return bd;
    }
}
```
