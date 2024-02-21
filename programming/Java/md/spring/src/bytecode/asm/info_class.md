# 定义存储类信息的实体类

类信息:

```java
@Data
public class ClassInfo {

    /**
     * 类内部名
     */
    private String internalName;
    /**
     * 类的编译版本号
     */
    private int version;
    /**
     * 类的访问标志
     */
    private int accessFlags;
    /**
     * 类的泛型信息
     */
    private String signature;
    /**
     * 父类内部名
     */
    private String superClassInternalName;
    /**
     * 实现的接口名
     */
    private List<String> interfaceNames;
    /**
     * 类的注解
     */
    private List<AnnotationInfo> annotations;

    /**
     * 字段
     */
    private List<FieldInfo> fields;
    /**
     * 方法
     */
    private List<MethodInfo> methods;
}
```

字段信息:

```java
@Data
public class FieldInfo {

    /**
     * 字段名
     */
    private String name;
    /**
     * 字段的描述符
     */
    private String desc;
    /**
     * 字段的访问标志
     */
    private int accessFlags;
    /**
     * 字段的泛型信息
     */
    private String signature;
    /**
     * static+final字段的初始值
     */
    private Object initialValue;
    /**
     * 字段的注解
     */
    private List<AnnotationInfo> annotations;
}
```

方法信息:

```java
@Data
public class MethodInfo {

    /**
     * 字段名
     */
    private String name;
    /**
     * 字段的描述符
     */
    private String desc;
    /**
     * 字段的访问标志
     */
    private int accessFlags;
    /**
     * 字段的泛型信息
     */
    private String signature;
    /**
     * 手动抛出的异常
     */
    private List<String> exceptions;
    /**
     * 方法的注解
     */
    private List<AnnotationInfo> annotations;
}
```

注解信息:

```java
@Data
public class AnnotationInfo {

    /**
     * 注解的描述符
     */
    private String desc;
    /**
     * 注解是否运行时可见
     */
    private boolean visibleAtRuntime;
    /**
     * 注解值
     */
    private Map<String, Object> values;

    public AnnotationInfo(String desc, boolean visibleAtRuntime) {
        this.desc = desc;
        this.visibleAtRuntime = visibleAtRuntime;
        this.values = new HashMap<>();
    }
}
```
