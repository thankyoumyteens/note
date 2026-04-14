# 极其关键的准备工作（必做）

在拉取镜像之前，你必须修改宿主机（你的 Linux 服务器）的一个内核参数。ES 底层使用 mmap 机制进行目录映射，Linux 默认的限制太小，会导致 ES 内存溢出并启动失败。

在你的宿主机终端执行以下命令：

```sh
# 1. 临时修改（立即生效）
sudo sysctl -w vm.max_map_count=262144

# 2. 写入配置文件（保证服务器重启后依然有效）
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```
