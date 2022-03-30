# Tunnel模式

IP隧道技术又称为IP封装技术，它可以将带有源和目标IP地址的数据报文使用新的源和目标IP进行二次封装，这样这个报文就可以发送到一个指定的目标主机上。

隧道模式下，调度器和后端服务器组之间使用IP隧道技术。当客户端发送的请求（CIP–>VIP）被director接收后，director修改该报文，加上IP隧道两端的IP地址作为新的源和目标地址，并将请求转发给后端被选中的一个目标。

当后端服务器接收到报文后，首先解封该报文原有的CIP—>VIP,该后端服务器发现自身配置了VIP，因此接受该数据包。当请求处理完成后，结果将不会重新交给director，而是直接返回给客户端。此时响应数据包的源IP为VIP，目标IP为CIP。

# 环境

- LVS：VIP=10.211.102.47 DIP=172.16.100.10
- Nginx1：172.16.100.20
- Nginx2：172.16.100.30

# 负载均衡服务器配置

安装 ipvsadm 并执行相关配置
```
yum install ipvsadm
vim lvs_tunnel.sh
```
内容如下
```sh
vip=10.211.102.47
rs1=172.16.100.20
rs2=172.16.100.30
/sbin/ipvsadm -C
/sbin/ipvsadm -A -t $vip:8088 -s rr
/sbin/ipvsadm -a -t $vip:8088 -r $rs1:8088 -i
/sbin/ipvsadm -a -t $vip:8088 -r $rs2:8088 -i
```
执行脚本
```
/bin/bash lvs_tunnel.sh
```

查看服务配置信息
```
ipvsadm -ln
```
输出
```
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  10.211.102.47:8088 rr
  -> 172.16.100.20:8088           Tunnel  1      0          0
  -> 172.16.100.30:8088           Tunnel  1      0          0
```

# 后端服务器配置

```
vim rs_tunnel.sh
```
如下内容
```sh
vip=10.211.102.47
modprobe ipip
ifconfig tunl0 $vip broadcast $vip netmask 255.255.255.255 up
echo "0" > /proc/sys/net/ipv4/ip_forward
echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce
echo "0" > /proc/sys/net/ipv4/conf/all/rp_filter
echo "0" > /proc/sys/net/ipv4/conf/tunl0/rp_filter
```
执行脚本（两个rs都需要执行）
```
/bin/bash rs_tunnel.sh
```
