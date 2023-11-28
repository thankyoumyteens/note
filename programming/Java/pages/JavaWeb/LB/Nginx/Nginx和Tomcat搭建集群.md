# 配置文件

```conf
http {
    server {
        listen 80
        server_name www.test.com;
        location / {
            # 转发到负载均衡服务器
            proxy_pass http://backserver;
        }
    }

    # 负载均衡配置
    upstream backserver {
        server 192.168.0.14;
        server 192.168.0.15;
    } 
}
```

# 轮询（默认）

```conf
upstream backserver { 
    server 192.168.0.14; 
    server 192.168.0.15; 
} 
```

# 指定权重

指定轮询几率, weight和访问比率成正比, 用于后端服务器性能不均的情况。

```conf
upstream backserver { 
    server 192.168.0.14 weight=1; 
    server 192.168.0.15 weight=10; 
}
```

# ip hash

```conf
upstream backserver { 
    ip_hash; 
    server 192.168.0.14:88; 
    server 192.168.0.15:80; 
} 
```
