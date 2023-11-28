# 使用方法

在springboot中不需要引入Hibernate Validator, 因为在引入的 spring-boot-starter-web（springbootweb启动器）依赖的时候中, 内部已经依赖了 hibernate-validator

```java
@Data
public class TestReqVO {
 
    @NotBlank(message = "name 不能为空")
    private String name;
 
    @NotNull(message = "age 不能为空")
    private Integer age;
 
    @NotEmpty(message = "id 集合不能为空")
    private List<String> ids;
}

@RestController
@RequestMapping("/test")
public class TestController {
    @PostMapping("/valid/error")
    public DataResult testvalidError(@RequestBody @Valid TestReqVO vo){
        return DataResult.ok();
    }
}

@ControllerAdvice
@ResponseBody
public class GlobalExceptionHandler {
    //捕获controller中的全局异常
    @ExceptionHandler(value = {BindException.class, MethodArgumentNotValidException.class})
    public Object validationExceptionHandler(Exception ex) {
        // ...
    }
}
```

# 常用的注解

| 注解                                       | 适用的数据类型                                                                                                                                      | 说明                                                                                                                          |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| @AssertFalse                                 | Boolean, boolean                                                                                                                                           | 验证注解的元素值是false                                                                                                |
| @AssertTrue                                  | Boolean, boolean                                                                                                                                           | 验证注解的元素值是true                                                                                                 |
| @DecimalMax（value=x）                     | BigDecimal, BigInteger, String, byte, short, int, long和原始类型的相应包装。HV额外支持: Number和CharSequence的任何子类型。   | 验证注解的元素值小于等于@ DecimalMax指定的value值                                                               |
| @DecimalMin（value=x）                     | BigDecimal, BigInteger, String, byte, short, int, long和原始类型的相应包装。HV额外支持: Number和CharSequence的任何子类型。   | 验证注解的元素值小于等于@ DecimalMin指定的value值                                                               |
| @Digits(integer=整数位数, fraction=小数位数) | BigDecimal, BigInteger, String, byte, short, int, long和原始类型的相应包装。HV额外支持: Number和CharSequence的任何子类型。   | 验证注解的元素值的整数位数和小数位数上限                                                                    |
| @Future                                      | java.util.Date, java.util.Calendar; 如果类路径上有Joda Time日期/时间API , 则由HV附加支持: ReadablePartial和ReadableInstant的任何实现。 | 验证注解的元素值（日期类型）比当前时间晚                                                                    |
| @Max（value=x）                            | BigDecimal, BigInteger, byte, short, int, long和原始类型的相应包装。HV额外支持: CharSequence的任何子类型（评估字符序列表示的数字值）, Number的任何子类型。 | 验证注解的元素值小于等于@Max指定的value值                                                                       |
| @Min（value=x）                            | BigDecimal, BigInteger, byte, short, int, long和原始类型的相应包装。HV额外支持: CharSequence的任何子类型（评估char序列表示的数值）, Number的任何子类型。 | 验证注解的元素值大于等于@Min指定的value值                                                                       |
| @NotNull                                     | 任意种类                                                                                                                                               | 验证注解的元素值不是null                                                                                              |
| @Null                                        | 任意种类                                                                                                                                               | 验证注解的元素值是null                                                                                                 |
| @Past                                        | java.util.Date, java.util.Calendar; 如果类路径上有Joda Time日期/时间API , 则由HV附加支持: ReadablePartial和ReadableInstant的任何实现。 | 验证注解的元素值（日期类型）比当前时间早                                                                    |
| @Pattern(regex=正则表达式, flag=)       | 串。HV额外支持: CharSequence的任何子类型。                                                                                                   | 验证注解的元素值与指定的正则表达式匹配                                                                       |
| @Size(min=最小值, max=最大值)          | 字符串, 集合, 映射和数组。HV额外支持: CharSequence的任何子类型。                                                                  | 验证注解的元素值的在min和max（包含）指定区间之内, 如字符长度、集合大小                          |
| @Valid                                       | Any non-primitive type（引用类型）                                                                                                                   | 验证关联的对象, 如账户对象里有一个订单对象, 指定验证订单对象                                      |
| @NotEmpty                                    | CharSequence,Collection, Map and Arrays                                                                                                                    | 验证注解的元素值不为null且不为空（字符串长度不为0、集合大小不为0）                                |
| @Range(min=最小值, max=最大值)         | CharSequence, Collection, Map and Arrays,BigDecimal, BigInteger, CharSequence, byte, short, int, long 以及原始类型各自的包装                    | 验证注解的元素值在最小值和最大值之间                                                                          |
| @NotBlank                                    | CharSequence                                                                                                                                               | 验证注解的元素值不为空（不为null、去除首位空格后长度为0）, 不同于@NotEmpty, @NotBlank只应用于字符串且在比较时会去除字符串的空格 |
| @Length(min=下限, max=上限)              | CharSequence                                                                                                                                               | 验证注解的元素值长度在min和max区间内                                                                             |
| @Email                                       | CharSequence                                                                                                                                               | 验证注解的元素值是Email, 也可以通过正则表达式和flag指定自定义的email格式                           |
