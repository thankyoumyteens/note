# 备份配置文件

```sh
sudo cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
```

# 修改sources.list文件

华为源

```sh
sudo sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
sudo sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
```

清华源

```sh
sudo sed -i "s@http://.*archive.ubuntu.com@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
sudo sed -i "s@http://.*security.ubuntu.com@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
```

# 更新

```sh
sudo apt update && sudo apt upgrade -y
```
