# 增加多语言文件

在resources中, 新增static/i18n文件夹, 在里面新建新建三个文件: 

- messages.properties（默认的多语言文件）
- messages_zh_CN.properties(中文语言文件)
- messages_en_US.properties（英文语言文件）

在里面添加上相同键的不同语言翻译值；如zh_CN中: 
```
user.appname=中文语言
```
en_US中: 
```
user.appname=English Language
```

# IDEA中设置文件的编码为utf-8

File->Settings->Editor->File Encodings

File->Other Settings->Default Settings ->Editor->File Encodings

将项目中的.idea文件夹中的encodings.xml文件中的编码格式改为uft-8

File->Settings->Build,Execution,Deployment -> Compiler -> Java Compiler, 
设置 Additional command line parameters选项为 -encoding utf-8

打开Run/Debug Configuration,选择你的tomcat, 
然后在  Server > VM options 设置为 -Dfile.encoding=UTF-8 , 重启tomcat

# 配置文件增加配置

```yml
#i18n语言国际化配置
spring:
  messages:
    encoding: utf-8
    basename: static/i18n/messages
```

# 增加拦截器对语言参数进行拦截和设置语言环境

```java
@Configuration
public class LocalConfig {

    /**
     * 默认解析器 其中locale表示默认语言
     */
    @Bean
    public LocaleResolver localeResolver() {
        SessionLocaleResolver localeResolver = new SessionLocaleResolver();
        localeResolver.setDefaultLocale(Locale.CHINA);
        return localeResolver;
    }

    /**
     * 默认拦截器 其中lang表示切换语言的参数名
     */
    @Bean
    public WebMvcConfigurer localeInterceptor() {
        return new WebMvcConfigurer() {
            @Override
            public void addInterceptors(InterceptorRegistry registry) {
                LocaleChangeInterceptor localeInterceptor = new LocaleChangeInterceptor();
                localeInterceptor.setParamName("lang");  //拦截lang参数
                registry.addInterceptor(localeInterceptor);
            }
        };
    }
}
```

# 获取相应语言环境中的值的工具类

```java
@Component
public class LocalUtil
{

    private static MessageSource messageSource;

    public LocalUtil(MessageSource messageSource)
    {
        LocalUtil.messageSource = messageSource;
    }

    /**
     * 获取单个国际化翻译值
     */
    public static String get(String msgKey)
    {
        try
        {
            return messageSource.getMessage(msgKey, null, LocaleContextHolder.getLocale());
        }
        catch (Exception e)
        {
            return msgKey;
        }
    }
}
```

# 使用

注意: 在调用接口时, 如果不传lang参数, 会获取默认解析器的语言, 如果传入了lang, 就使用lang参数传入的语言

```java
@GetMapping("/getmsg")
public String language() {
    String message =LocalUtil.get("user.appname");  //调用
    return message;
}
```
