# 基本用法

maven

```xml
<!-- https://mvnrepository.com/artifact/org.ow2.asm/asm-all -->
<dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm-all</artifactId>
    <version>5.2</version>
</dependency>
```

生成 class 文件:

```java
package org.example;

import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.FieldVisitor;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;

import java.io.*;

public class AsmDemo {

    /**
     * 生成接口
     */
    public static void genInterface() {
        ClassWriter writer = new ClassWriter(ClassWriter.COMPUTE_FRAMES);

        int interfaceDescriptor = Opcodes.ACC_PUBLIC + Opcodes.ACC_ABSTRACT + Opcodes.ACC_INTERFACE;
        String objectClass = "java/lang/Object";

        writer.visit(Opcodes.V1_8, interfaceDescriptor, "org/example/PersonGender",
                null, objectClass, new String[]{});

        int constDescriptor = Opcodes.ACC_PUBLIC + Opcodes.ACC_FINAL + Opcodes.ACC_STATIC;

        FieldVisitor male = writer.visitField(constDescriptor, "MALE", "I",
                null, 1);
        male.visitEnd();

        FieldVisitor female = writer.visitField(constDescriptor, "FEMALE", "I",
                null, 0);
        female.visitEnd();

        writer.visitEnd();

        byte[] byteArray = writer.toByteArray();

        writeToFile(byteArray, "PersonGender.class");
    }

    /**
     * 生成类
     */
    public static void genClass() {
        ClassWriter writer = new ClassWriter(ClassWriter.COMPUTE_FRAMES);

        int classDescriptor = Opcodes.ACC_PUBLIC + Opcodes.ACC_SUPER;
        String objectClass = "java/lang/Object";

        writer.visit(Opcodes.V1_8, classDescriptor, "org/example/Person",
                null, objectClass, new String[]{});

        int fieldDescriptor = Opcodes.ACC_PUBLIC;

        FieldVisitor gender = writer.visitField(fieldDescriptor, "gender", "I",
                null, null);
        gender.visitEnd();

        int methodDescriptor = Opcodes.ACC_PUBLIC;

        MethodVisitor method = writer.visitMethod(methodDescriptor, "<init>", "()V",
                null, null);
        method.visitCode();
        // 构造器必须先调用父类构造器
        // 0: aload_0
        // 1: invokespecial #1  // Method java/lang/Object."<init>":()V
        // 4: return
        method.visitVarInsn(Opcodes.ALOAD, 0);
        method.visitMethodInsn(Opcodes.INVOKESPECIAL, "java/lang/Object",
                "<init>", "()V", false);
        method.visitInsn(Opcodes.RETURN);
        // visitMaxs用于设置 max stacks 和 max locals
        // 由于ClassWriter构造方法使用了ClassWriter.COMPUTE_FRAMES
        // ASM会自动计算这两个值, 这里的设置会失效
        // 但是如果不写visitMaxs, 在用到Person类时就会抛异常:
        // Exception in thread "main" java.lang.VerifyError: Operand stack overflow
        // 这里的visitMaxs只起到标记Code属性结束的作用
        method.visitMaxs(-1, -1);
        method.visitEnd();

        writer.visitEnd();

        byte[] byteArray = writer.toByteArray();

        writeToFile(byteArray, "Person.class");
    }

    private static void writeToFile(byte[] byteArray, String fileName) {
        try (ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
             FileOutputStream fileOutputStream = new FileOutputStream(fileName)) {
            outputStream.write(byteArray);
            outputStream.writeTo(fileOutputStream);
            fileOutputStream.flush();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws ClassNotFoundException {
        genInterface();
        genClass();
    }
}
```
