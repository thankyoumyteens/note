# 选择文件对话框

- getOpenFileName: 打开单个文件
- getOpenFileNames: 打开多个文件
- getExistingDirectory: 打开文件夹

```py
from PySide6.QtWidgets import QFileDialog

# parent: 父组件
# caption: 对话框的标题
# dir: 默认路径
# filter: 话框的后缀名过滤器
#         filter="office文件(*.docx;)"
#         filter="office文件(*.docx;*.xlsx)"
#         filter="所有文件(*.*)"
file_path, filetype = QFileDialog.getOpenFileName(parent=self,
                                                  caption='选择文件',
                                                  dir="",
                                                  filter="docx文件(*.docx)")

dir_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "",
                                            QFileDialog.Option.ShowDirsOnly)
```
