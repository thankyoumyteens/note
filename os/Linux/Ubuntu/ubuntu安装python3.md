# ubuntu安装python3

不要轻易删除python3及其依赖，由于系统中很多软件都是依赖python3，所以卸载了python3会导致系统崩溃。

```sh
cd ~/src_pack
sudo apt-get install -y zlib1g-dev libbz2-dev libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev tk-dev libgdbm-dev libdb-dev libpcap-dev xz-utils libexpat1-dev liblzma-dev libffi-dev libc6-dev
wget https://repo.huaweicloud.com/python/3.7.9/Python-3.7.9.tgz
tar -zxvf Python-3.7.9.tgz
cd Python-3.7.9
./configure prefix=/usr/local/python3
sudo make
sudo make install
ln -s /usr/local/python3/bin/python3.7 /usr/bin/python37
ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip37
python37 -V
pip37 -V
```
