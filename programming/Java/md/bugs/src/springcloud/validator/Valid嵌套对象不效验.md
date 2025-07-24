# @Valid 嵌套对象不效验

```java
@Data
public class UserParam {
    @NotBlank(message = "name不能为空")
    private String name;
    @NotBlank(message = "phone不能为空")
    private String phone;

    private Address address;
}

@Data
public class Address{
    @NotBlank(message = "province不能为空")
    private String province;
    @NotBlank(message = "city不能为空")
    private String city;
}

@PostMapping("/test")
public String test(@Valid @RequestBody UserParam param) {
    return param.toString();
}
```

传入 json:

```json
{
  "name": "test",
  "phone": "12345678901",
  "address": {
    "province": "",
    "city": ""
  }
}
```

结果可以正常进入 controller, address 中的 province 和 city 的非空校验没有生效。

## 解决方案

给 UserParam 类中的 Address 上加@Valid 注解:

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
```
