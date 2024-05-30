# JWT 令牌结构

一个 JWT 由三部分组成:

- Header: base64 编码的 Json 字符串, Header 通常由两部分组成: 令牌的类型, 即 JWT, 以及使用的签名算法, 例如 HMAC、SHA256 或 RSA。
- Payload: base64 编码的 Json 字符串, payload 由声明(claims)组成。声明就是保存的数据。
- Signature: 使用指定算法对 Header 和 Payload 加盐计算得到的字符串, 保证 token 在传输的过程中没有被篡改或者损坏。

各部分以`.`分割, 如: `eyJhbGciOiJIUzUxMiJ9.eyJjcnQiOjE1MjgzNDM4OTgyNjgsImV4cCI6MTUyODM0MzkxOCwidXNlcm5hbWUiOiJ0b20ifQ.E-0jxKxLICWgcFEwNwQ4pfhdMzchcHmsd8G_BTsWgkUmVwPzDd7jJlf94cAdtbwTLMm27ouYYzTTxMXq7W1jvQ`

## header

Header 通常由两部分组成: 令牌的类型, 即 JWT, 以及使用的签名算法, 例如 HMAC SHA256 或 RSA。

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

typ: token 的类型, 这里固定为 JWT

alg: 使用的 hash 算法, 例如: HMAC SHA256 或者 RSA

## payload

JWT 的第二部分是有效载荷, 其中包含声明( claims)。

声明包含实体(通常是用户)和其他自定义信息。

声明有三种类型

- registered claims 这是一组预定义声明, 不是强制性的, 但建议使用。
- public claims: 这些可以由使用 JWT 的人随意定义。但为避免冲突, 应在 IANA JSON Web Token Register 中定义它们, 或者将其定义为包含防冲突命名空间的 URI。
- private claims: 这个指的就是自定义的 claim, 用于在同意使用这些声明的各方之间共享信息, 这些信息既没有注册也没有公开声明。

registered claims 包括

- iss: jwt 签发者
- sub: jwt 所面向的用户
- aud: 接收 jwt 的一方
- exp: jwt 的过期时间, 这个过期时间必须要大于签发时间
- nbf: 定义在什么时间之前, 该 jwt 都是不可用的.
- iat: jwt 的签发时间
- jti: jwt 的唯一身份标识, 主要用来作为一次性 token,从而回避重放攻击。

## signature

对 header 和 payload 部分进行签名, 保证 token 在传输的过程中没有被篡改或者损坏

# JWT 工作原理

客户端通过请求将用户名和密码传给服务端, 服务端将用户名和密码进行核对, 核对成功后将用户 id 等其他信息作为 jwt 的有效载荷(payload)与头部进行 base64 编码形成 jwt(字符串), 后端将这段字符串作为登陆成功的返回结果返回给前端。前端将其保存在 localstroage 或 sessionstroage 里, 退出登录时, 删除 JWT 字符串就可以。

每次请求, 前端都会把 JWT 作为 authorization 请求头传给后端, 后端进行检查。

# JWT+RefreshToken

客户端将用户名和密码传给服务端进行登陆, 服务端核对成功后将用户信息作为 jwt 的 payload 生成有效时间较短的 JWT 字符串作为 AccessToken, 并生成有效时间较长的 RefreshToken, 一起返回给客户端。客户端将其保存, 每次请求时都会携带 AccessToken, 如果 AccessToken 过期, 则客户端使用 RefreshToken 向刷新接口申请新的 AccessToken。退出登录时, 删除 JWT 字符串就可以。

由于 RefreshToken 不会在客户端请求业务接口时验证, 所以将 RefreshToken 存储在数据库中, 不会对业务接口的响应时间造成影响。当用户需要登出或禁用用户时, 只需要将服务端的 RefreshToken 禁用或删除, 用户就会在 AccessToken 过期后无法访问需要认证的接口。这样的方式虽然会有一定的窗口期, 但是结合用户登出时客户端删除 AccessToken 的操作, 基本上可以适应常规情况下对用户认证鉴权的精度要求。
