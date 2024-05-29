# 复制一个类的字段

```java
public class AsmUtil implements Opcodes {

    /**
     * 类加载器
     */
    public static class AsmUtilClassLoader extends ClassLoader {

        /**
         * 根据字节数组加载类
         *
         * @param fullClassName 类的全限定名
         * @param b             类的字节数组
         * @return class
         */
        public Class<?> load(String fullClassName, byte[] b) {
            return defineClass(fullClassName, b, 0, b.length);
        }
    }

    /**
     * 复制类的字段, 并生成一个新的类
     *
     * @param originalEntityName 要复制的类
     * @return 新的类
     */
    public static Class<?> copyFields(String originalEntityName) throws Exception {
        // 新类内部名
        String internalName = originalEntityName.replaceAll("\\.", "/");
        internalName = internalName.substring(0, internalName.length() - 2) + "Copy";
        // 新类全名
        String targetName = internalName.replaceAll("/", ".");

        // 获取原始类的所有字段
        Class<?> originalClass = Class.forName(originalEntityName);
        Field[] declaredFields = originalClass.getDeclaredFields();
        List<Field> fieldList = new ArrayList<>(Arrays.asList(declaredFields));

        // 创建类
        ClassWriter writer = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        writer.visit(V1_8, ACC_PUBLIC + ACC_SUPER,
                internalName, null, "java/lang/Object",
                null);
        // 添加构造方法
        addConstructor(writer);

        // 添加字段
        for (Field field : fieldList) {
            addField(field, writer, internalName);
        }

        writer.visitEnd();

        byte[] byteArray = writer.toByteArray();
        return new AsmUtilClassLoader().load(targetName, byteArray);
    }

    /**
     * 构造方法
     *
     * @param writer ClassWriter
     */
    private static void addConstructor(ClassWriter writer) {
        MethodVisitor init = writer.visitMethod(ACC_PUBLIC,
                "<init>", "()V", null, null);
        init.visitCode();
        init.visitVarInsn(ALOAD, 0);
        init.visitMethodInsn(INVOKESPECIAL,
                "java/lang/Object", "<init>", "()V", false);
        init.visitInsn(RETURN);
        init.visitMaxs(0, 0);
        init.visitEnd();
    }

    /**
     * 添加字段
     *
     * @param field        要添加的字段
     * @param writer       ClassWriter
     * @param internalName 类内部名
     */
    private static void addField(Field field, ClassWriter writer, String internalName) throws InvocationTargetException, IllegalAccessException {
        String fieldType = field.getType().getName().replaceAll("\\.", "/");
        String fieldName = field.getName();
        String pascalName = fieldName.substring(0, 1).toUpperCase() + fieldName.substring(1);
        // 字段描述符
        String fieldDesc = "L" + fieldType + ";";
        // 添加字段
        FieldVisitor fieldVisitor = writer.visitField(ACC_PRIVATE, fieldName,
                fieldDesc, null, null);
        // 字段的注解
        Annotation[] annotations = field.getAnnotations();
        for (Annotation annotation : annotations) {
            Class<? extends Annotation> annotationType = annotation.annotationType();
            String annotationDesc = "L" + annotationType.getName()
                    .replaceAll("\\.", "/") + ";";
            AnnotationVisitor annotationVisitor = fieldVisitor.visitAnnotation(annotationDesc, true);
            // 复制注解的属性
            Method[] methods = annotationType.getDeclaredMethods();
            for (Method method : methods) {
                String name = method.getName();
                Class<?> returnType = method.getReturnType();
                if (returnType.isArray()) {
                    AnnotationVisitor visitArray = annotationVisitor.visitArray(name);
                    Object[] r = (Object[]) method.invoke(annotation);
                    for (Object item : r) {
                        visitArray.visit(null, item);
                    }
                    visitArray.visitEnd();
                } else {
                    Object r = method.invoke(annotation);
                    if (r instanceof Class) {
                        // 注解的属性值是类时, 需要用Type包装
                        annotationVisitor.visit(name, Type.getType((Class<?>) r));
                    } else {
                        annotationVisitor.visit(name, r);
                    }
                }
            }
            annotationVisitor.visitEnd();
        }
        fieldVisitor.visitEnd();
        // getter
        MethodVisitor getter = writer.visitMethod(ACC_PUBLIC, "get" + pascalName,
                "()" + fieldDesc, null, null);
        getter.visitCode();
        getter.visitVarInsn(ALOAD, 0);
        getter.visitFieldInsn(GETFIELD, internalName, fieldName, fieldDesc);
        getter.visitInsn(ARETURN);
        getter.visitMaxs(1, 1);
        getter.visitEnd();
        // setter
        MethodVisitor setter = writer.visitMethod(ACC_PUBLIC, "set" + pascalName,
                "(" + fieldDesc + ")V", null, null);
        setter.visitCode();
        setter.visitVarInsn(ALOAD, 0);
        setter.visitVarInsn(ALOAD, 1);
        setter.visitFieldInsn(PUTFIELD, internalName, fieldName, fieldDesc);
        setter.visitInsn(RETURN);
        setter.visitMaxs(2, 2);
        setter.visitEnd();
    }
}
```

使用

```java
public static void main(String[] args) throws Exception {
    Class<?> klass = AsmUtil.copyFields("org.example.OriginEntity");
    System.out.println(klass);
}
```
