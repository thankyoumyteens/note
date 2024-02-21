# 获取字段信息

```java
public class FieldInfoVisitor extends FieldVisitor {

    private final FieldInfo fieldInfo;

    public FieldInfoVisitor(FieldInfo fieldInfo) {
        super(Opcodes.ASM4);
        this.fieldInfo = fieldInfo;
        this.fieldInfo.setAnnotations(new ArrayList<>());
    }

    /**
     * 获取字段的注解信息
     * classReader.accept方法中会调用
     */
    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        AnnotationInfo annotationInfo = new AnnotationInfo(desc, visible);
        fieldInfo.getAnnotations().add(annotationInfo);
        // 返回自定义字段Visitor, 用来获取注解的参数
        return new AnnotationInfoVisitor(annotationInfo);
    }
}
```
