- <a href="linuxCmd.md">Linux命令</a>
- <a href="vim.md">Vim</a>

# profile和bashrc文件的区别

1. /etc/profile 用来设置系统环境变量，比如$PATH. 这里面的环境变量是对系统内所有用户生效的。
2. /etc/bashrc  这个文件设置系统-bash shell相关的，对系统内所有用户生效。只要用户运行bash命令，那么这里面的东西就在起作用。
3. ~/.bash_profile: 用来设置一些环境变量，功能和/etc/profile 类似，但是这个是用户级别来设定的，也就是说，你在/home/{username}/.bash_profile 中设定了环境变量，那么这个环境变量只针对这个用户生效.
4. ~/.bashrc: 作用类似于/etc/bashrc, 只是针对当前用户有效，不对其他用户生效。 
5. 另外/etc/profile中设定的变量是全局的可以作用于任何用户，
6. ~/.bashrc等中设定的变量是局部只能继承/etc/profile中的变量，他们是"父子"关系。
7. ~/.bash_profile 是交互式、login 方式进入 bash 运行的意思是只有用户登录时才会生效。
8. ~/.bashrc 是交互式 non-login 方式进入 bash 运行的，用户不一定登录，只要以该用户身份运行命令行就会读取该文件。

# 在ubuntu上搭建ss

通过如下命令安装：
```
apt-get install python-pip
pip install shadowsocks
```
通过文件配置的方式。新建一个 /etc/ssConfig.json 文件，内容如下：
```
{
    "server": "your_droplet_ip",
    "server_port": 8388,
    "local_address": "127.0.0.1",
    "local_port": 1080,
    "password": "your_password",
    "timeout": 300,
    "method": "aes-256-cfb",
    "fast_open": false
}
```
接下来使用下面的指令启动服务：
```
ssserver -c /etc/ssConfig.json
```
或者在后台运行
```
ssserver -c /etc/ssConfig.json -d start
ssserver -c /etc/ssConfig.json -d stop
```

## 解决undefined symbol: EVP_CIPHER_CTX_cleanup错误

这个问题是由于在openssl1.1.0版本中，废弃了EVP_CIPHER_CTX_cleanup函数

解决：

用vim打开文件：vim /usr/local/lib/python2.7/dist-packages/shadowsocks/crypto/openssl.py (该路径请根据自己的系统情况自行修改，如果不知道该文件在哪里的话，可以使用find命令查找文件位置)

跳转到52行（shadowSocks2.8.2版本，其他版本搜索一下cleanup）

进入编辑模式
将第52行`libcrypto.EVP_CIPHER_CTX_cleanup.argtypes = (c_void_p,)`
改为`libcrypto.EVP_CIPHER_CTX_reset.argtypes = (c_void_p,)`

再次搜索cleanup（全文件共2处，此处位于111行），
将`libcrypto.EVP_CIPHER_CTX_cleanup(self._ctx)` 
改为`libcrypto.EVP_CIPHER_CTX_reset(self._ctx)`
保存并退出

问题解决

## 解决pip install时unsupported locale setting错误

其实是语言配置错误导致的：

```
# locale -a
locale: Cannot set LC_CTYPE to default locale: No such file or directory
C
C.UTF-8
en_AG
en_AG.utf8
en_AU.utf8
en_BW.utf8
en_CA.utf8
en_DK.utf8
en_GB.utf8
en_HK.utf8
en_IE.utf8
...
```

解决方案：
```
# export LC_ALL=C
```
