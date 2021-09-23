# JWT的构成

一个JWT由三部分组成：
- Header（头部）: base64编码的Json字符串
- Payload（载荷） : base64编码的Json字符串
- Signature（签名）: 使用指定算法，通过Header和Payload加盐计算的字符串

各部分以`.`分割，如：`eyJhbGciOiJIUzUxMiJ9.eyJjcnQiOjE1MjgzNDM4OTgyNjgsImV4cCI6MTUyODM0MzkxOCwidXNlcm5hbWUiOiJ0b20ifQ.E-0jxKxLICWgcFEwNwQ4pfhdMzchcHmsd8G_BTsWgkUmVwPzDd7jJlf94cAdtbwTLMm27ouYYzTTxMXq7W1jvQ`


## header

typ:token的类型，这里固定为JWT

alg：使用的hash算法，例如：HMAC SHA256或者RSA

## payload

存储需要传递的信息，如用户ID、用户名等, 还包含元数据，如过期时间、发布人等, 与header不同，payload可以加密

## signature

对header和payload部分进行签名, 保证token在传输的过程中没有被篡改或者损坏

# JWT工作原理

客户端通过请求将用户名和密码传给服务端，服务端将用户名和密码进行核对，核对成功后将用户id等其他信息作为jwt的有效载荷（payload）与头部进行base64编码形成jwt（字符串），后端将这段字符串作为登陆成功的返回结果返回给前端。前端将其保存在localstroage或sessionstroage里，退出登录时，删除JWT字符串就可以。

每次请求，前端都会把JWT作为authorization请求头传给后端，后端进行检查。

# JJWT

## 依赖

```xml
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt</artifactId>
    <version>0.9.0</version>
</dependency>
```

## 创建token


```java
// 过期时间为1分钟
long exp = System.currentTimeMillis() + 1000 * 60;

JwtBuilder builder = Jwts.builder()
    .setHeaderParam("typ", "JWT")
    .setId("111")
    .setSubject("小明")
    .setIssuedAt(newDate())
    .claim("role", "admin")
    .setExpiration(new Date(exp))
    .signWith(SignatureAlgorithm.HS256, "my_key");

String token = builder.compact();
```

### header

setHeader() 有两种参数形式，一种是Header接口的实现，一种是Map。

如果以Map作为参数，在setHeader的时候会生成默认的Header接口实现DefaultHeader对象。

两种参数形式调用setHeader()，都会令Header重新赋值。

setHeaderParam() 和 setHeaderParams() 向Header追加参数。

在生成jwt的时候，如果不设置签名，那么header中的alg默认为none。

### claims

载荷部分存在两个属性：payload和claims。两个属性均可作为载荷，jjwt中二者只能设置其一，如果同时设置，在终端方法compact() 中将抛出异常

JWT标准 7个保留声明(7个声明都是可选的，也就是说可以不用设置):

- setIssuer() 签发者
- setSubject() 主题
- setAudience() 接收方
- setExpiration() 到期时间
- setNotBefore() 在此之前不可用
- setIssuedAt() jwt的签发时间
- setId() jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。

设置自定义claims
```java
Map<String, Object> claims= new HashMap<>();
claims.put("username", username);
claims.put("create_time", new Date(System.currentTimeMillis()));

Jwts.builder().setClaims(claims);
```
或者
```java
Jwts.builder()
    .claim("username", username)
    .claim("create_time", new Date(System.currentTimeMillis()));
```

compressWith() 压缩方法。当载荷过长时可对其进行压缩。可采用jjwt实现的两种压缩方法CompressionCodecs.GZIP和CompressionCodecs.DEFLATE。如果使用压缩，生成时会将压缩算法写入header。

### signature

signWith() 签名方法。两个参数分别是签名算法和自定义的签名Key（盐）。生成时会将所使用签名算法写入header。

### compact

compact() 生成JWT。过程如下：

- 载荷校验。
- 获取key。
- 将所使用签名算法写入header。
- 将Json形式的header转为bytes，再Base64编码
- 将Json形式的claims转为bytes，如果需要压缩则压缩，再进行Base64编码
- 拼接header和claims。如果签名key为空，则不进行签名(末尾补分隔符" . ")；如果签名key不为空，以拼接的字符串作为参数，按照指定签名算法进行签名计算签名部分，签名部分同样也会进行Base64编码。
- 返回完整JWT

## 解析Token

从JWT Token中获取载荷

当未过期时可以正常读取

当过期时会引发 io.jsonwebtoken.ExpiredJwtException 异常

```java
Claims claims = Jwts.parser().setSigningKey("my_key").parseClaimsJws(token).getBody();
System.out.println("id:" + claims.getId());
System.out.println("subject:" + claims.getSubject());
System.out.println("IssuedAt:" + claims.getIssuedAt());
System.out.println("role:" + claims.get("role"));
```
