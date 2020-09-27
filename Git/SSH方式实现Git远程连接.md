# 使用SSH方式实现Git远程连接GitHub

复制ssh地址
```
git@github.com:thankyoumyteens/note.git
```
输入命令
```
ssh-keygen -t rsa
```
连续三次回车

复制~/.ssh文件夹下id_rsa.pub文件的所有内容

到github右上角账户管理-Setting下面找到左侧SSH and GPG keys菜单, 接着点击Add SSH key, 在title栏输入一个自己喜欢的标题, key栏中粘贴刚刚复制的公钥内容, 最后点击Add key按钮

# SSH-keygen用法

```
ssh-keygen -t rsa -C "your_email@example.com"
```
代码参数含义：

- -t 指定密钥类型，默认是 rsa ，可以省略。
- -C 设置注释文字，比如邮箱。
- -f 指定密钥文件存储文件名。
