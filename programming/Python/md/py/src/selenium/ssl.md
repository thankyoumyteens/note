# 不支持安全连接问题

```py
# 忽略证书错误
opt.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=opt, service=ser)
```
