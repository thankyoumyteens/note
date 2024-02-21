# 获取方法信息

```java
public class MethodInfoVisitor extends MethodVisitor {

    private final MethodInfo methodInfo;

    public MethodInfoVisitor(MethodInfo methodInfo) {
        super(Opcodes.ASM4);
        this.methodInfo = methodInfo;
        this.methodInfo.setAnnotations(new ArrayList<>());
    }

    /**
     * 获取方法的注解信息
     * classReader.accept方法中会调用
     */
    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        AnnotationInfo annotationInfo = new AnnotationInfo(desc, visible);
        methodInfo.getAnnotations().add(annotationInfo);
        // 返回自定义字段Visitor, 用来获取注解的参数
        return new AnnotationInfoVisitor(annotationInfo);
    }
}
```
