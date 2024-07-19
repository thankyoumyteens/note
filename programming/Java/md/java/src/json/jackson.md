# Jackson

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-core</artifactId>
    <version>2.17.1</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.17.1</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-annotations</artifactId>
    <version>2.17.1</version>
</dependency>
```

## json 转对象

```java
String json = "{\"name\":\"John\", \"age\":30}";
ObjectMapper objectMapper = new ObjectMapper();
try {
    Demo demo = objectMapper.readValue(json, Demo.class);
    System.out.println(demo);
} catch (JsonProcessingException e) {
    throw new RuntimeException(e);
}
```

## 对象转 json

```java
Demo demo = new Demo();
demo.setName("John");
demo.setAge(30);
ObjectMapper objectMapper = new ObjectMapper();
try {
    String json = objectMapper.writeValueAsString(demo);
    System.out.println(json);
} catch (JsonProcessingException e) {
    throw new RuntimeException(e);
}
```
