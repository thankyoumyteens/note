# 读取并修改 class 信息

读取并修改 class 信息与只读取 class 信息类似, 只是需要使用两个参数的构造方法。

如果只是要在原本的方法内容执行前插入自己的代码, 只需要重写 visitCode 方法。如果要完全替换原本的方法, 就需要重写方法体中用到的所有 visitXxxInsn 方法。

## 自定义 ClassVisitor

```java
public class ClassEditor extends ClassVisitor implements Opcodes {

    /**
     * 如果要修改class内容, 必须要调用父类的带ClassVisitor参数的构造方法
     *
     * @param api          ASM版本
     * @param classVisitor 传入的ClassVisitor(关键),
     *                     传入用来生成新类的ClassWriter
     */
    protected ClassEditor(int api, ClassVisitor classVisitor) {
        super(api, classVisitor);
    }
}
```
