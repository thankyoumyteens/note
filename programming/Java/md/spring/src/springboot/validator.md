# Hibernate Validator

如果是 Spring Boot 项目，那么 spring-boot-starter-web 中就已经依赖 hibernate-validator 了。

其它项目手动引入:

```xml
<dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>8.0.1.Final</version>
</dependency>
<dependency>
    <groupId>org.glassfish.expressly</groupId>
    <artifactId>expressly</artifactId>
    <version>5.0.0</version>
</dependency>
```

## 校验 bean

```java
@Data
public class Demo {

    @Pattern(regexp = "^[a-zA-Z]*$", message = "must be a string")
    private String str;

    @Max(value = 10, message = "must be less than 10")
    private Integer number;
}

public class ValidatorDemo {

    public static void main(String[] args) {
        Demo demo = new Demo();
        demo.setStr("123");
        demo.setNumber(11);
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        Validator validator = factory.getValidator();

        // 验证所有字段
        Set<ConstraintViolation<Demo>> validate = validator.validate(demo);

        // 验证单个字段
        Set<ConstraintViolation<Demo>> str = validator.validateProperty(demo, "str");

        // 输出错误信息
        validate.forEach(constraintViolation -> System.out.println(constraintViolation.getMessage()));
        str.forEach(constraintViolation -> System.out.println(constraintViolation.getMessage()));
    }
}
```

## 嵌套对象校验

如果 bean 中包含其它对象, 需要在字段上添加 `@Valid` 注解:

```java
@Data
public class UserParam {
    @NotBlank(message = "name不能为空")
    private String name;
    @NotBlank(message = "phone不能为空")
    private String phone;
    @Valid
    private Address address;
}

@Data
public class Address{
    @NotBlank(message = "province不能为空")
    private String province;
    @NotBlank(message = "city不能为空")
    private String city;
}
```
