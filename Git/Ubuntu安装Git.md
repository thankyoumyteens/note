# Ubuntu安装Git

```sh
sudo add-apt-repository ppa:git-core/ppa
sudo apt-get update
sudo apt-get install -y git
git --version
git config --global user.name "zhaosz"
git config --global user.email "iloveyesterday@outlook.com"
```

# 源码安装

```
sudo apt-get install dh-autoreconf libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev -y
sudo apt-get install asciidoc xmlto docbook2x -y
sudo apt-get install install-info -y
wget https://github.com/git/git/archive/refs/tags/v2.33.0.tar.gz
tar -zxf v2.33.0.tar.gz
cd git-2.33.0
make configure
./configure --prefix=/usr
make all doc info
sudo make install install-doc install-html install-info
```
