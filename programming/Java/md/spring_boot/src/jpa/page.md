# 分页

1. 接口

```java
package com.example;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.Repository;

public interface PersonRepository extends Repository<Person, Long> {

    Page<Person> findByName(Pageable pageable, String name);
}
```

2. 使用

```java
package com.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Component;

@Component
public class ConsoleApp implements CommandLineRunner {

    @Autowired
    private PersonRepository personRepository;

    @Override
    public void run(String... args) {
        // 页索引从0开始
        PageRequest pageRequest = PageRequest.of(0, 10);
        Page<Person> page = personRepository.findByName(pageRequest, "Alice");

        System.out.println(page.getTotalPages());
        System.out.println(page.getContent());
    }
}
```
