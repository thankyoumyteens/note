# Hibernate Validator

添加依赖:

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

## 校验字段

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
        try (ValidatorFactory factory = Validation.buildDefaultValidatorFactory()) {
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

## 校验方法

```java
public class Demo {

    private String str;

    @Pattern(regexp = "^[a-zA-Z]*$", message = "must be a string")
    public String getStr() {
        return null;
    }

    public void setStr(@Pattern(regexp = "^[a-zA-Z]*$", message = "must be a string") String str) {
        this.str = str;
    }
}

public class ValidatorDemo {

    public static void main(String[] args) throws NoSuchMethodException {
        try (ValidatorFactory factory = Validation.buildDefaultValidatorFactory()) {
            Demo demo = new Demo();
            ExecutableValidator validator = factory.getValidator().forExecutables();

            // 验证方法参数
            Method method = Demo.class.getMethod("setStr", String.class);
            Object[] parameterValues = {"123"};
            Set<ConstraintViolation<Demo>> validate = validator.validateParameters(demo, method, parameterValues);

            // 验证方法返回值
            Method getter = Demo.class.getMethod("getStr");
            Set<ConstraintViolation<Demo>> returnValue = validator.validateReturnValue(demo, getter, "123");

            // 输出错误信息
            validate.forEach(constraintViolation -> System.out.println(constraintViolation.getMessage()));
            returnValue.forEach(constraintViolation -> System.out.println(constraintViolation.getMessage()));
        }
    }
}
```
