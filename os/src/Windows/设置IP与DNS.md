# 设置动态获取IP地址(DHCP)

```
netsh interface ip set address name="本地连接" source=dhcp
```

# 设置固定IP

```
netsh interface ip set address name="本地连接" source=static addr=192.168.0.3 mask=255.255.255.0 gateway=192.168.0.1 gwmetric=auto
```

- name: 网络连接名称, 一般为"本地连接"。可以在"控制面板"->"网络连接"中看到。
- source: 获取IP的途径。动态获取, 则为dhcp, 手动设置, 则为static。
- addr: 要设置的IP地址。
- mask: 子网掩码。
- gateway: 网关地址。
- gwmetric: 网关跃点数, 可以设置为整型数值, 也可以设置为auto。

# 自动获取DNS

```
netsh interface ip set dns name="本地连接" source=dhcp
```

# 设置DNS

设置首选DNS
```
netsh interface ip set dns name="本地连接" source=static addr=218.85.157.99 register=primary
```

设置备用DNS
```
netsh interface ip add dns name="本地连接" source=static addr=202.101.98.55 index=2
```

- name: 网络连接名称, 一般为"本地连接"。可以在"控制面板"->"网络连接"中看到。
- source: 获取dns的途径。动态获取, 则为dhcp, 手动设置, 则为static。
- addr: 要设置的dns地址。
- register=none: 禁用动态 DNS 注册。
- register=primary: 只在主 DNS 后缀下注册。
- register=both: 在主 DNS 后缀下注册, 也在特定连接后缀下注册。
- index: 设置的DNS的顺序号。
