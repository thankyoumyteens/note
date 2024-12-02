# 设置代理

```py
# 设置代理
host='127.0.0.1'
port=1234
opt.add_argument(f'--proxy-server=http://{host}:{port}')

driver = webdriver.Chrome(options=opt, service=ser)

driver.get('http://www.example.com')

driver.quit()
```

## socks 代理

```py
opt.add_argument("--proxy-server=socks5://" + host + ":" + port)
opt.add_argument("--proxy-auth=" + socks5User + ":" + socks5Pass)
```
