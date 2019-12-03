# linux中git保存账户密码

1. 进入到用户家目录`cd ~`
2. 执行`git config --global credential.helper store`命令
3. 执行之后会在`.gitconfig`文件末尾追加两行: `[credential]`和`helper = store`
4. 之后到项目目录，执行`git pull`命令，会提示输入账号密码。输完这一次以后就不再需要，并且会在家目录生成一个`.git-credentials`文件
5. 之后pull/push代码都不再需要输入账号密码了
 