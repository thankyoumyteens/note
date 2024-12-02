# 刷新当前页面

```py
driver = webdriver.Chrome(options=opt, service=ser)

driver.get('http://www.example.com')

# 刷新当前页面
driver.refresh()

driver.quit()
```
