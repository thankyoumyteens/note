# SpringBoot 集成

1. 添加依赖:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

2. 配置类:

```java
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import org.hibernate.validator.HibernateValidator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ValidatorConfig {

    @Bean
    public Validator validator() {
        ValidatorFactory factory = Validation.byProvider(HibernateValidator.class)
                // failFast: 快速失败模式,
                // 在校验过程中, 当遇到第一个不满足条件的参数时就立即返回, 不再继续后面参数的校验
                .configure().failFast(true).buildValidatorFactory();
        return factory.getValidator();
    }
}
```

3. 全局异常处理:

```java
package org.example.validator;

import org.springframework.http.HttpStatus;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

@RestControllerAdvice
public class GlobalExceptionHandler {

    // http状态码返回400
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseBody
    public Result<Void> validateErrorHandler(MethodArgumentNotValidException e) {
        ObjectError error = e.getBindingResult().getAllErrors().getFirst();
        return Result.fail(ResultCode.PARAMS_INVALID, error.getDefaultMessage());
    }
}
```

4. controller:

```java
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/validator")
public class ValidatorController {

     @PostMapping("/demo")
     public Map<String, String> demo(@Valid @RequestBody Demo demo) {
         return new HashMap<>(){{
             put("message", "success");
         }};
     }
}
```
