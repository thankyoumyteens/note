# 访问者模式

Visitor 模式是一种行为型设计模式，用来把“数据结构”与“对结构中元素的操作”分离。

核心点：

- 数据结构稳定（经常不变）
- 操作经常需要新增 / 变化

那就：

- 在数据结构中提供“接受访问者”的入口
- 每种操作封装成一个 Visitor
- 增加新操作 = 增加一个 Visitor 类，而不用修改原来的结构类

## 用一个极简 Java 例子感受一下

### 1. 元素接口和具体元素（结构）

```java
// 被访问的元素接口
interface Element {
    void accept(Visitor visitor);
}

// 具体元素 A
class ElementA implements Element {
    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void doSomethingA() {
        System.out.println("ElementA doSomethingA");
    }
}

// 具体元素 B
class ElementB implements Element {
    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void doSomethingB() {
        System.out.println("ElementB doSomethingB");
    }
}
```

### 2. 访问者接口 & 不同访问者

```java
// 访问者接口
interface Visitor {
    void visit(ElementA a);
    void visit(ElementB b);
}

// 一种访问者：打印日志
class LogVisitor implements Visitor {
    @Override
    public void visit(ElementA a) {
        System.out.println("LogVisitor visit ElementA");
        a.doSomethingA();
    }

    @Override
    public void visit(ElementB b) {
        System.out.println("LogVisitor visit ElementB");
        b.doSomethingB();
    }
}

// 另一种访问者：做统计
class StatsVisitor implements Visitor {
    @Override
    public void visit(ElementA a) {
        System.out.println("StatsVisitor count A");
    }

    @Override
    public void visit(ElementB b) {
        System.out.println("StatsVisitor count B");
    }
}
```

### 3. 使用

```java
public class VisitorDemo {
    public static void main(String[] args) {
        Element[] elements = { new ElementA(), new ElementB() };

        Visitor logVisitor = new LogVisitor();
        Visitor statsVisitor = new StatsVisitor();

        // 使用日志访问者
        for (Element e : elements) {
            e.accept(logVisitor);
        }

        // 使用统计访问者
        for (Element e : elements) {
            e.accept(statsVisitor);
        }
    }
}
```

结构（ElementA / ElementB）没动，我们只是换了两种“访问者”，就实现了两套完全不同的逻辑。

## ASM 世界里的“结构”和“访问者”

结构（被访问的东西）：

- class 文件整体（类名、访问标志、父类、接口）
- 字段
- 方法
- 方法里的字节码指令

访问者（你写的逻辑）：

- 你自己实现/继承的 ClassVisitor
- 在里面返回你包装过的 MethodVisitor
- 在这些 Visitor 中的 visitXxx 方法里做事：
  - 读取信息
  - 修改 / 插入字节码
  - 打印、分析、统计…
