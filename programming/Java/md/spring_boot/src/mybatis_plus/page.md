# 分页

1. 配置

```java
import com.baomidou.mybatisplus.annotation.DbType;
import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.PaginationInnerInterceptor;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@MapperScan("com.example.mapper")
public class MybatisPlusConfig {
    /**
     * 添加分页插件
     */
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.SQLITE));
        return interceptor;
    }
}
```

2. 使用

```java
@PostMapping("/queryPage")
public R<IPage<MyData>> queryPage(@RequestBody MyParams params) {
    Integer pageNum = params.getPageNum();
    Integer pageSize = params.getPageSize();
    IPage<MyData> page = demoMapper.selectPage(
            new Page<>(pageNum, pageSize),
            Wrappers.<MyData>query()
    );
    return R.success(page);
}
```
