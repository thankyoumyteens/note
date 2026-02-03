# 复制一个类的字段

### 1. 自定义 ClassLoader

```java
public class MyDynamicClassLoader extends ClassLoader {

    // 用当前线程的 context classloader
    public MyDynamicClassLoader() {
        super(Thread.currentThread().getContextClassLoader());
    }

    public MyDynamicClassLoader(ClassLoader parent) {
        super(parent);
    }

    /**
     * 把一段字节码定义成 Class 对象
     */
    public Class<?> defineClass(String className, byte[] bytes) {
        // 注意：这里直接调用 ClassLoader 自带的 protected defineClass 方法
        return super.defineClass(className, bytes, 0, bytes.length);
    }
}
```

### 2. 复制所有字段

```java
public class AsmUtil implements Opcodes {

    /**
     * 复制类的字段, 并生成一个新的类
     *
     * @param originalEntityName 要复制的类
     * @return 新类的字节码
     */
    public static byte[] copyFields(String originalEntityName) throws Exception {
        // 新类的内部名
        String internalName = originalEntityName.replaceAll("\\.", "/");
        internalName = internalName + "Copy";
        // 新类的类全名
        String targetName = internalName.replaceAll("/", ".");

        // 获取原始类的所有字段
        Class<?> originalClass = Class.forName(originalEntityName);
        Field[] declaredFields = originalClass.getDeclaredFields();
        List<Field> fieldList = new ArrayList<>(Arrays.asList(declaredFields));

        // 创建新类
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
        return byteArray;
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

### 3. 结合EasyExcel使用

```java
public static void main(String[] args) throws Exception {
    // ASM 生成的字节码
    byte[] bytes = AsmUtil.copyFields("com.example.ExcelModel");

    // 1. 创建自定义 ClassLoader（以当前线程的 context classloader 为父）
    MyDynamicClassLoader loader =
        new MyDynamicClassLoader(Thread.currentThread().getContextClassLoader());

    // 2. 加载类
    Class<?> modelClass = loader.defineClass(className, bytes);

    // 3. 很关键：把这个新的 loader 设成当前线程的 ContextClassLoader
    ClassLoader old = Thread.currentThread().getContextClassLoader();
    Thread.currentThread().setContextClassLoader(loader);
    try {
        // 4. 在这个上下文中调用 EasyExcel
        EasyExcel.write(outputStream, modelClass)
                .sheet("sheet1")
                .doWrite(dataList);  // dataList 里的对象类型要和 modelClass 对应
    } finally {
        // 5. 恢复原来的 ClassLoader，避免污染其他地方
        Thread.currentThread().setContextClassLoader(old);
    }
}
```
