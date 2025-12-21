# 将 class 文件转换为 ASM 代码

```java
package org.example;

import org.objectweb.asm.ClassReader;
import org.objectweb.asm.util.ASMifier;
import org.objectweb.asm.util.Printer;
import org.objectweb.asm.util.Textifier;
import org.objectweb.asm.util.TraceClassVisitor;

import java.io.IOException;
import java.io.PrintWriter;

public class ASMUtil {

    public static void printAsmCode(String fullClassName) throws IOException {
        Printer printer = new ASMifier();
        PrintWriter printWriter = new PrintWriter(System.out, true);
        TraceClassVisitor traceClassVisitor = new TraceClassVisitor(null, printer, printWriter);
        ClassReader classReader = new ClassReader(fullClassName);
        // 不打印栈帧和debug信息
        int parsingOptions = ClassReader.SKIP_FRAMES | ClassReader.SKIP_DEBUG;
        classReader.accept(traceClassVisitor, parsingOptions);
    }

    public static void printByteCode(String fullClassName) throws IOException {
        Printer printer = new Textifier();
        PrintWriter printWriter = new PrintWriter(System.out, true);
        TraceClassVisitor traceClassVisitor = new TraceClassVisitor(null, printer, printWriter);
        ClassReader classReader = new ClassReader(fullClassName);
        // 不打印栈帧和debug信息
        int parsingOptions = ClassReader.SKIP_FRAMES | ClassReader.SKIP_DEBUG;
        classReader.accept(traceClassVisitor, parsingOptions);
    }

    public static void main(String[] args) throws IOException {
        String className = "org.example.DemoObj";
        printAsmCode(className);
        printByteCode(className);
    }
}
```

## printAsmCode 的输出示例

```java
package asm.org.example;
import org.objectweb.asm.AnnotationVisitor;
import org.objectweb.asm.Attribute;
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.ConstantDynamic;
import org.objectweb.asm.FieldVisitor;
import org.objectweb.asm.Handle;
import org.objectweb.asm.Label;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.RecordComponentVisitor;
import org.objectweb.asm.Type;
import org.objectweb.asm.TypePath;
public class DemoObjDump implements Opcodes {

public static byte[] dump () throws Exception {

ClassWriter classWriter = new ClassWriter(0);
FieldVisitor fieldVisitor;
RecordComponentVisitor recordComponentVisitor;
MethodVisitor methodVisitor;
AnnotationVisitor annotationVisitor0;

classWriter.visit(V1_8, ACC_PUBLIC | ACC_SUPER, "org/example/DemoObj", null, "java/lang/Object", null);

{
methodVisitor = classWriter.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
methodVisitor.visitCode();
methodVisitor.visitVarInsn(ALOAD, 0);
methodVisitor.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
methodVisitor.visitInsn(RETURN);
methodVisitor.visitMaxs(1, 1);
methodVisitor.visitEnd();
}
{
methodVisitor = classWriter.visitMethod(ACC_PUBLIC, "populateFields", "(Ljava/util/List;)V", "(Ljava/util/List<Lorg/example/Demo;>;)V", null);
methodVisitor.visitCode();
methodVisitor.visitInsn(RETURN);
methodVisitor.visitMaxs(0, 2);
methodVisitor.visitEnd();
}
{
methodVisitor = classWriter.visitMethod(ACC_PUBLIC | ACC_STATIC, "main", "([Ljava/lang/String;)V", null, null);
methodVisitor.visitCode();
methodVisitor.visitInsn(RETURN);
methodVisitor.visitMaxs(0, 1);
methodVisitor.visitEnd();
}
classWriter.visitEnd();

return classWriter.toByteArray();
}
}
```

## printByteCode 的输出示例

```java
// class version 52.0 (52)
// access flags 0x21
public class org/example/DemoObj {


  // access flags 0x1
  public <init>()V
    ALOAD 0
    INVOKESPECIAL java/lang/Object.<init> ()V
    RETURN
    MAXSTACK = 1
    MAXLOCALS = 1

  // access flags 0x1
  // signature (Ljava/util/List<Lorg/example/Demo;>;)V
  // declaration: void populateFields(java.util.List<org.example.Demo>)
  public populateFields(Ljava/util/List;)V
    RETURN
    MAXSTACK = 0
    MAXLOCALS = 2

  // access flags 0x9
  public static main([Ljava/lang/String;)V
    RETURN
    MAXSTACK = 0
    MAXLOCALS = 1
}
```
