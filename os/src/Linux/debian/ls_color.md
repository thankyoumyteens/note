# ls 结果显示颜色

```sh
sudo vim ~/.bashrc

# 把下面内容解除注释
export LS_OPTIONS='--color=auto'
eval "$(dircolors)"
alias ls='ls $LS_OPTIONS'
alias ll='ls $LS_OPTIONS -l'
alias l='ls $LS_OPTIONS -lA'

# 使配置生效
source ~/.bashrc
```
