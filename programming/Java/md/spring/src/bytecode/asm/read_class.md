# 获取类信息

继承 ClassVisitor, 重写 visit 方法来获取类的信息, 重写 visitAnnotation 方法来获取类的注解信息, 重写 visitField 方法来获取类的字段信息, 重写 visitMethod 方法来获取类的方法信息。

visitField 方法内只会获取字段和方法的基本信息, 如果要获取更多信息, 比如字段上有哪些注解, 就需要写一个自定义类继承 FieldVisitor 并重写它的相关方法, 作为 visitField 方法的返回值。visitMethod 方法同理。

```java
@Getter
public class ClassInfoVisitor extends ClassVisitor {

    public final ClassInfo classInfo;

    public ClassInfoVisitor() {
        super(Opcodes.ASM4);
        classInfo = new ClassInfo();
        classInfo.setFields(new ArrayList<>());
        classInfo.setMethods(new ArrayList<>());
        classInfo.setAnnotations(new ArrayList<>());
    }

    /**
     * 获取类的信息
     * classReader.accept方法中会调用
     */
    @Override
    public void visit(int version, int access, String name, String signature, String superName, String[] interfaces) {
        // 记录类信息
        classInfo.setInternalName(name);
        classInfo.setVersion(version);
        classInfo.setAccessFlags(access);
        classInfo.setSignature(signature);
        classInfo.setSuperClassInternalName(superName);
        classInfo.setInterfaceNames(Arrays.asList(interfaces));
    }

    /**
     * 获取类的注解信息
     * classReader.accept方法中会调用
     */
    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        AnnotationInfo annotationInfo = new AnnotationInfo(desc, visible);
        classInfo.getAnnotations().add(annotationInfo);
        // 返回自定义字段Visitor, 用来获取注解的参数
        return new AnnotationInfoVisitor(annotationInfo);
    }

    /**
     * 获取类的字段信息
     * classReader.accept方法中会调用, 每有一个字段就会调用一次
     */
    @Override
    public FieldVisitor visitField(int access, String name, String desc, String signature, Object value) {
        FieldInfo fieldInfo = new FieldInfo();
        fieldInfo.setName(name);
        fieldInfo.setDesc(desc);
        fieldInfo.setAccessFlags(access);
        fieldInfo.setSignature(signature);
        fieldInfo.setInitialValue(value);
        classInfo.getFields().add(fieldInfo);
        // 返回自定义字段Visitor, 用来获取字段注解
        return new FieldInfoVisitor(fieldInfo);
    }

    /**
     * 获取类的方法信息
     * classReader.accept方法中会调用, 每有一个方法就会调用一次
     */
    @Override
    public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
        MethodInfo methodInfo = new MethodInfo();
        methodInfo.setName(name);
        methodInfo.setDesc(desc);
        methodInfo.setAccessFlags(access);
        methodInfo.setSignature(signature);
        if (exceptions != null) {
            methodInfo.setExceptions(Arrays.asList(exceptions));
        }
        classInfo.getMethods().add(methodInfo);
        // 返回自定义方法Visitor, 用来获取方法注解, 指令等信息
        return new MethodInfoVisitor(methodInfo);
    }
}
```
