# 浏览器窗口大小

```py
driver = webdriver.Chrome(options=opt, service=ser)
# 设置浏览器窗口大小
driver.set_window_size(1024, 768)
```

## 最大化窗口

```py
driver = webdriver.Chrome(options=opt, service=ser)
# 最大化浏览器窗口大小
driver.maximize_window()
```

## 缩放页面

```py
driver = webdriver.Chrome(options=opt, service=ser)
# 打开网页
driver.get('https://www.example.com')
# 缩小页面, 相当于 CTRL 与 - 的组合键
zoom_out = "document.body.style.zoom='0.5'"
driver.execute_script(zoom_out)
# 放大页面, 相当于 CTRL 与 + 的组合键
zoom_out = "document.body.style.zoom='1.5'"
driver.execute_script(zoom_out)
```
