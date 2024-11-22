# 弹框

```python
import pyautogui

# 返回字符串: OK
pyautogui.alert('显示带有确定按钮的文本')

# 返回字符串: OK/Cancel
pyautogui.confirm('显示带有确定和取消按钮的文本')

# 返回: 输入的字符串
txt = pyautogui.prompt('用户可以输入一个字符串, 然后按确定')
```
