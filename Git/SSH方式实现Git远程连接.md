# 使用SSH方式实现Git远程连接GitHub

1. 登录GitHub, 进入仓库, 点击Clone or download, 选择Use SSH, 复制ssh地址`git@github.com:thankyoumyteens/note.git`
2. 在git bash输入`git clone git@github.com:thankyoumyteens/note.git`, 显示没有权限（无公钥）
3. 输入`ssh-keygen -t rsa`, 连续三次回车（即不做任何输入）, 生成的密钥存放于家目录下的`.ssh`文件夹中
4. 复制`.ssh`文件夹下`id_rsa.pub`文件的所有内容
5. 到github右上角账户管理-Setting下面找到左侧SSH and GPG keys菜单, 接着点击Add SSH key, 在title栏输入一个自己喜欢的标题, key栏中粘贴刚刚复制的公钥内容, 最后点击Add key按钮
6. 再次clone远程库, 成功

