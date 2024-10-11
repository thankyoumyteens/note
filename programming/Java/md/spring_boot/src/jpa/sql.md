# 手写 sql

## 查询

```java
package com.example;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.Repository;
import org.springframework.data.repository.query.Param;

public interface PersonRepository extends Repository<Person, Long> {

    @Query(value = "select * from person where name = :name", nativeQuery = true)
    Page<Person> findByName(Pageable pageable, @Param("name") String name);
}
```

## 非查询

```java
package com.example;

import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.Repository;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;

public interface PersonRepository extends Repository<Person, Long> {

    @Transactional
    @Modifying
    @Query(value = "update person set name = :#{#p.name} where id = :#{#p.id}", nativeQuery = true)
    int update(@Param("p") Person person);
}
```
