# 首个单词为单个字母时驼峰识别失效

当首个单词仅有一个字母，jackson 序列化时会加到后一个词，即 `tName` 变为 `tname`:

```java
@Data
public class Demo {
    private String tName;
}

public class JacksonDemo {

    public static void main(String[] args) {
        Demo demo = new Demo();
        demo.setTName("John");
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            String json = objectMapper.writeValueAsString(demo);
            System.out.println(json);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}
// 输出: {"tname":"John"}
```

## 解决

使用 `@JsonProperty` 手动指定:

```java
@Data
public class Demo {
    @JsonProperty("tName")
    private String tName;
}
```
