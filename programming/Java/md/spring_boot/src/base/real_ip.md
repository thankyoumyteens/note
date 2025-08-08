# 获取客户端 ip

## 通过 REMOTE_ADDR 获取

表示发出请求的远程主机的 IP 地址，remote_addr 代表客户端的 IP，但它的值不是由客户端提供的，而是服务端根据请求方的 ip 指定的。当你的浏览器访问某个网站时，假设中间没有任何代理，那么网站的 web 服务器就会把 remote_addr 设为你的机器 IP。如果你用了某个代理，那么你的浏览器会先访问这个代理，然后再由这个代理转发到网站，这样 web 服务器就会把 remote_addr 设为这台代理机器的 IP。

## 通过 HTTP 请求头中的 X-Real-IP 获取

当有多个代理时候，可以在第一个反向代理上增加配置, 以获取真实客户端 IP。

### Nginx 中的配置

```conf
proxy_set_header    X-Real-IP $remote_addr;
```

## 通过 HTTP 请求头中的 X-Forwarded-For 获取

格式:

```
X-Forwarded-For: <client>, <proxy1>, <proxy2>
```

X-Forwarded-For 记录着从客户端发起请求后访问过的每一个 IP 地址, 各 IP 地址间由英文逗号+空格分隔。

比如:

```
X-Forwarded-For: 1.1.1.1, 2.2.2.2, 3.3.3.3
```

代表请求由 1.1.1.1 发出，第一层代理是 2.2.2.2，第二层代理是 3.3.3.3。

### Nginx 中的配置

```conf
proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
```
