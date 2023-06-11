# ubuntu软件源配置

## 备份配置文件

```
sudo cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
```

## 修改sources.list文件

华为源

```
sudo sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
sudo sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
```

清华源

```
sudo sed -i "s@http://.*archive.ubuntu.com@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
sudo sed -i "s@http://.*security.ubuntu.com@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
```

## 更新
```
sudo apt update && sudo apt upgrade -y
```
