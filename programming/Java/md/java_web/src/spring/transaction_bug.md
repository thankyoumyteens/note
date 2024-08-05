# 事务失效的场景

## 异常捕获处理

事务失效:

```java
@Transactional
public void buy(Acount account, Product product) {
    try {
        accountMapper.updateAccount(account);
        // 异常
        int e = 1 / 0;
        productMapper.updateProduct(product);
    } catch (Exception e) {
        log.error("failed", e);
    }
}
```

原因: @Transactional 只有捕获到目标抛出的异常, 才会进行回滚。如果目标自己处理掉了异常, @Transactional 就无法捕获到异常了。

解决:

```java
@Transactional
public void buy(Acount account, Product product) {
    try {
        accountMapper.updateAccount(account);
        int e = 1 / 0;
        productMapper.updateProduct(product);
    } catch (Exception e) {
        log.error("failed", e);
        // 手动抛出异常
        throw new RuntimeException("failed");
    }
}
```

## 抛出非运行时异常

事务失效:

```java
@Transactional
public void buy(Acount account, Product product) throws FileNtFoundException {
    accountMapper.updateAccount(account);
    // 异常
    new FileInputStream("不存在的文件");
    productMapper.updateProduct(product);
}
```

原因: @Transactional 只会回滚运行时异常。

解决:

```java
// 配置成只要有异常就回滚
@Transactional(rollbackFor = Exception.class)
public void buy(Acount account, Product product) throws FileNtFoundException {
    accountMapper.updateAccount(account);
    new FileInputStream("不存在的文件");
    productMapper.updateProduct(product);
}
```

## 非 public 方法

事务失效:

```java
@Transactional
void buy(Acount account, Product product) {
    accountMapper.updateAccount(account);
    // 异常
    throw new RuntimeException("failed");
    productMapper.updateProduct(product);
}
```

原因: @Transactional 无法为非 public 方法添加代理。

解决: 改成 public。

## 方法嵌套调用

事务失效:

```java
public class Demo {

    public void A() {
        B();
    }

    @Transactional
    public void B() {
        // ...
    }
}
```

原因: 只有当事务方法被当前类以外的代码调用时, 才会由 Spring 生成的代理对象来管理。

解决:

```java
public class Caller {
    @Autowired
    Callee ee;

    public void A() {
        ee.B();
    }
}

public class Callee {
    @Transactional
    public void B() {
        // ...
    }
}
```

或者:

```java
public class Demo {

    @Transactional
    public void A() {
        B();
    }

    public void B() {
        // ...
    }
}
```
