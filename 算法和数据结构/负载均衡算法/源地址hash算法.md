# 源地址hash算法

使同一个客户端多次的请求落在同一台服务器

源地址hash算法的思路就是对客户端的ip进行hash，然后用hash值与服务器的数量进行取模，得到需要访问的服务器的ip。只要客户端ip不变，那hash后的值就是固定的

```java
int index = Math.abs(getHash(clientIp)) % SERVER_IP_LIST.size();
String serverIp = SERVER_IP_LIST.get(index);
System.out.println(clientIp + "请求的服务器ip为" + serverIp);
```

问题: 服务器数量一旦变化，那源地址hash之后取模的值可能就变化，获取到的服务器的ip自然就也会发生变化
