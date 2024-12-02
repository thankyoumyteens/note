# 浏览器窗口大小

```py
driver = webdriver.Chrome(options=opt, service=ser)

# 设置浏览器窗口大小
driver.set_window_size(1024, 768)

driver.get('http://www.example.com')

driver.quit()
```
