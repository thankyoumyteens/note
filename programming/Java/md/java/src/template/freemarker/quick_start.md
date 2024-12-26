# 基本使用

### 1. 依赖

```xml
<dependency>
    <groupId>org.freemarker</groupId>
    <artifactId>freemarker</artifactId>
    <version>2.3.33</version>
</dependency>
```

### 2. 创建模版 /tmp/demo.ftl

```ftl
<#ftl attributes={"content_type":"text/html; charset=UTF-8"}>
message: ${msg}
```

### 3. 渲染模版

```java
package com.example;

import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.HashMap;
import java.util.Map;

public class App {
    public static void main(String[] args) throws IOException, TemplateException {
        String templateDir = "/tmp";
        String outputFile = "/tmp/demo.txt";

        Map<String, Object> params = new HashMap<>();
        params.put("msg", "hello");

        Configuration configuration = new Configuration(Configuration.DEFAULT_INCOMPATIBLE_IMPROVEMENTS);
        configuration.setDirectoryForTemplateLoading(new File(templateDir));
        configuration.setDefaultEncoding("utf-8");

        Template template = configuration.getTemplate("demo.ftl");
        Writer out = new FileWriter(outputFile);
        template.process(params, out);
        out.close();
    }
}
```
