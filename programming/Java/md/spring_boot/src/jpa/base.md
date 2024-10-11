# 常规用法

1. 定义实体

```java
package com.example;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
// 实体
@Entity
@NoArgsConstructor
@AllArgsConstructor
// 表名
@Table(name = "person")
public class Person {

    // 主键
    @Id
    // 自增
    @GeneratedValue
    private Long id;

    @Column(name = "name", nullable = false, length = 100)
    private String name;

    @Column(name = "age", nullable = false)
    private Integer age;
}
```

2. 创建 XxxRepository 接口

```java
package com.example;

import org.springframework.data.repository.Repository;

// 继承Repository接口, 泛型传入实体类和主键的类型
// 不用写实现类
public interface PersonRepository extends Repository<Person, Long> {

    Person save(Person person);

    void update(Person person);

    void deleteById(Long id);

    Person findById(Long id);
}
```

3. 使用

```java
package com.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class ConsoleApp implements CommandLineRunner {

    @Autowired
    private PersonRepository personRepository;

    @Override
    public void run(String... args) {
        personRepository.save(new Person(null, "Alice", 23));

        System.out.println(personRepository.findById(1L));
    }
}
```

## 接口命名规则

```java
package com.example;

import org.springframework.data.repository.Repository;

import java.util.List;

public interface PersonRepository extends Repository<Person, Long> {

    List<Person> findByNameAndAge(String name, Integer age);

    List<Person> findByNameAndAgeIgnoreCase(String name, Integer age);

    List<Person> findByNameAndAgeOrderByNameDesc(String name, Integer age);

    long countByName(String name);
}
```
