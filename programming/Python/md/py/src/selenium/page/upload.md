# 文件上传

对于通过 input 标签实现的上传功能, 可以将其看作是一个输入框, 即通过 send_keys()指定本地文件路径的方式实现文件上传。

```py
# 定位上传按钮, 添加本地文件
driver.find_element_by_name("file").send_keys('D:\\myfile.txt')
```
