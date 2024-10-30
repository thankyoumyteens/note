# ls 结果显示颜色

```sh
vim ~/.zshrc

# 添加下面内容
export LS_OPTIONS='--color'
alias ls='ls $LS_OPTIONS'
alias ll='ls $LS_OPTIONS -l'
alias l='ls $LS_OPTIONS -lA'

# 使配置生效
source ~/.zshrc
```
