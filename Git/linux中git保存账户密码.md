# linux中git保存账户密码

```
cd ~
git config --global credential.helper store
```
再输入密码后,密码会保存在.git-credentials文件中
