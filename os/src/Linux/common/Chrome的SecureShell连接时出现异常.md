# 解决Chrome的secure shell连接openwrt时出现的“WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!”
使用chromebook secure shell 连接 openwrt时出现如下问题:
```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
dd:3b:ad:5f:c5:5c:fc:09:58:21:df:ca:f5:23:3d:be.
Please contact your system administrator.
Add correct host key in /.ssh/known_hosts to get rid of this message.
Offending RSA key in /.ssh/known_hosts:3
RSA host key for 192.168.1.1 has changed and you have requested strict checking.
Host key verification failed.
NaCl plugin exited with status code 255.
(R)econnect, (C)hoose another connection, or E(x)it?
```
解决方法如下: 
1. 打开secure shell；
2. 尝试登录openwrt；
3. 按 ctrl+shift+j 组合键, 调出控制台；
4. 输入如下命令: 
```
term_.command.removeAllKnownHosts()
```
回车后, 可以看见 true

重新连接openwrt, 出现
Are you sure you want to continue connecting (yes/no)?
时, 输入yes

问题解决
