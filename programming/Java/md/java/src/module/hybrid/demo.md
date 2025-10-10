# 使用传统的类路径

下面的 3 个 jar 文件并不是模块, 没有模块描述符。虽然第三方库并不在我们的直接控制之下，但我们却可以控制 src 下的代码, 所以这些代码是迁移时所需要重点关注的。

这是一个非常常见的迁移情况, 将自己的代码转移到模块上, 而不用迁移库。

### 1. 目录结构

```
.
├── lib
│   ├── jackson-annotations-2.8.8.jar
│   ├── jackson-core-2.8.8.jar
│   └── jackson-databind-2.8.8.jar
└── src
    ├── Main.java
    └── Person.java
```

### 2. Main.java

```java
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Main {

    public static void main(String[] args) throws JsonProcessingException {
        Person person = new Person();
        person.setName("张三");
        person.setAge(18);

        ObjectMapper objectMapper = new ObjectMapper();
        String json = objectMapper.writeValueAsString(person);
        System.out.println(json);
    }
}
```

### 3. Person.java

```java
public class Person {

    private String name;
    private Integer age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
```

### 4. 编译

```sh
mkdir target

# 编译命令：将src下的Java文件编译到target目录
# 并把lib中的jar包添加到类路径
javac -d target -cp "lib/*" src/*.java
```

### 5. 运行

```sh
java -cp "target:lib/*" Main
```
