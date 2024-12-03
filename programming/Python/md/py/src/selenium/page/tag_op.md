# 标签操作

| 方法                | 说明                   |
| ------------------- | ---------------------- |
| clear()             | 清除文本               |
| send_keys (value)   | 模拟按键输入           |
| click()             | 单击元素               |
| submit()            | 用于提交表单           |
| get_attribute(name) | 获取元素属性值         |
| is_displayed()      | 设置该元素是否用户可见 |
| size                | 返回元素的尺寸         |
| text                | 获取元素的文本         |

```py
e = WebDriverWait(driver, 100, 0.5).until(
    EC.presence_of_element_located(('id', 'input1'))
)
# 输入内容
e.send_keys('x^2')
```
