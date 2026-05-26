# 自定义 SSH 端口

SSH 可以同时监听多个端口。核心是在 `sshd_config` 里写多行 `Port`，然后放行防火墙端口，最后重启 `sshd`。

下面以 Debian 上同时开放 `22` 和 `22222` 为例。

## 1. 编辑 SSH 服务端配置

```bash
sudo vim /etc/ssh/sshd_config
```

找到：

```sshconfig
#Port 22
```

改成：

```sshconfig
Port 22
Port 22222
```

注意：多个端口要写成多行

## 2. 检查配置语法

```bash
sudo sshd -t
```

没有输出就表示配置语法没问题。

## 3. 放行新端口

如果你用的是 `ufw`：

```bash
sudo ufw allow 22222/tcp
sudo ufw reload
sudo ufw status
```

如果你用的是 `iptables`，可以先查看现有规则：

```bash
sudo iptables -L -n
```

临时放行：

```bash
sudo iptables -A INPUT -p tcp --dport 22222 -j ACCEPT
```

如果你的 VPS 面板有安全组/防火墙，比如云厂商防火墙，也要在面板里放行 `22222/tcp`。

## 4. 重启 SSH

Debian 通常服务名是 `ssh`：

```bash
sudo systemctl restart ssh
```

查看状态：

```bash
sudo systemctl status ssh
```

## 5. 检查监听端口

```bash
sudo ss -tulpn | grep ssh
```

正常应该能看到类似：

```text
0.0.0.0:22
0.0.0.0:22222
[::]:22
[::]:22222
```

## 6. 本地测试新端口

**不要关闭当前 SSH 窗口。**
在本地新开一个终端测试：

```bash
ssh -p 22222 root@你的服务器IP
```

如果你用密钥：

```bash
ssh -i ~/.ssh/id_ed25519 -p 22222 root@你的服务器IP
```

确认新端口能登录后，再考虑是否关闭 `22`。

## 7. 如果后续想关闭 22

先确认 `22222` 稳定可登录，然后编辑：

```bash
sudo vim /etc/ssh/sshd_config
```

改成只保留：

```sshconfig
Port 22222
```

检查并重启：

```bash
sudo sshd -t
sudo systemctl restart ssh
```

然后删除防火墙里的 22，前提是你真的不需要它了：

```bash
sudo ufw delete allow 22/tcp
sudo ufw reload
```
