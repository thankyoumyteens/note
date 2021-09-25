# 过滤规则

## 比较运算

- `==` 等于
- `!=` 不等于
- `>` 大于
- `<` 小于
- `>=` 大于等于
- `<=` 小于等于

## 逻辑运算

- `&&` 与
- `||` 或
- `^^` 异或
- `!` 非

## 协议过滤

- `tcp` 只看tcp数据包
- `udp` 只看udp数据包
- `http` 只看http数据包
- `udp && !dns` 只看是udp且不是dns的数据包

## ip地址过滤

- `ip.src == 192.168.2.0/24` 源ip属于192.168.2.1~192.168.2.254的数据包
- `ip.dst == 192.168.2.1` 目的ip属于192.168.2.1的数据包
- `ip.addr == 192.168.2.1` 源ip或目的ip属于192.168.2.1的数据包

## 端口过滤

- `tcp.dstport == 80` 目的端口是80的tcp数据包
- `tcp.dstport == 80 || tcp.dstport == 80` 目的端口是80或443的tcp数据包
- `udp.port > 33758` 源端口或目的端口大于33758的udp数据包

## 内容过滤

- `contains` 匹配字符串, 如: `http.request.uri contains "static"`
- `matches` 匹配正则表达式, 如: `http.request.uri matches "^/static"`
