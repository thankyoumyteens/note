# git设置代理

```
# 设置当前代理
git config http.proxy http://127.0.0.1:2334

# 取消当前代理
git config --unset http.proxy

#设置全局代理
git config --global http.proxy http://127.0.0.1:7890

#取消全局代理
git config --global --unset http.proxy

#设置socks5代理
git config http.proxy socks5://127.0.0.1:10809
```
