# 获取注解信息

```java
public class AnnotationInfoVisitor extends AnnotationVisitor {

    private final AnnotationInfo annotationInfo;

    public AnnotationInfoVisitor(AnnotationInfo annotationInfo) {
        super(Opcodes.ASM4);
        this.annotationInfo = annotationInfo;
    }

    @Override
    public void visit(String name, Object value) {
        // 比如: @Service(value = "demo")
        // name = value
        // value = demo
        annotationInfo.getValues().put(name, value);
    }
}
```
