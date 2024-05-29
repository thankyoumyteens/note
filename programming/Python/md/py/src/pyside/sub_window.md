# 弹出子窗口

在 QT Designer 中为主窗口加一个按钮。然后再新建一个 widget。

```py
# 子窗口
class SubDialog(QWidget, Ui_SubDialog):
    # parent_params: 主窗口的传参
    def __init__(self, parent=None, parent_params=None):
        super(SubDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent_params = parent_params

# 主窗口
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        # 子窗口的引用
        self.sub_dialog = None

    # 按钮点击事件
    # 弹出子窗口
    def show_dialog(self):
        self.sub_dialog = SubDialog(None, {
            '参数': 'abc',
        })
        self.sub_dialog.show()
```
