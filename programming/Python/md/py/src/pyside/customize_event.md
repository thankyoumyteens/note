# 自定义事件

以自定义支持拖拽的 LineEdit 组件为例, 要实现的功能: 鼠标拖动文件到文本框上松开, 文本框设置成拖拽的文件的路径, 并把路径发送给主窗口。

自定义组件:

```py
from PySide6 import QtWidgets
from PySide6.QtCore import Signal


class LineEditWithDragEvent(QtWidgets.QLineEdit):
    # 自定义事件, 必须定义在这里
    # 事件参数以字符串为例
    pathModifiedSignal = Signal(str)

    def __init__(self, parent=None):
        super(LineEditWithDragEvent, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(LineEditWithDragEvent, self).dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            self.setText(url.toLocalFile())
            # 触发自定义事件
            self.pathModifiedSignal.emit(url.toLocalFile())
        else:
            super(LineEditWithDragEvent, self).dropEvent(event)
```

在 QT Designer 中把自定义组件放置到主窗口, 并命名为 dir_path。

主窗口:

```py
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 监听自定义事件
        self.dir_path.pathModifiedSignal.connect(self.choose_dir_by_drag)

    def choose_dir_by_drag(self, dir_path):
        print("path:" + dir_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec())
```
