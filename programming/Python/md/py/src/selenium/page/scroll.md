# 控制滚动条

```py
# 滚动到指定位置
driver.execute_script('document.documentElement.scrollTop=100')
```

## 控制网页内嵌div中的滚动条

```py
# 控制纵向滚动条位置
js='document.querySelector("div1").scrollTop=10000'
# 控制横向滚动条位置
# js='document.querySelector("div1").scrollLeft=10000'
driver.execute_script(js)
```
