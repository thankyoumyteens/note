# word 转 pdf

### 1. 安装 libreoffice

[download-libreoffice](https://www.libreoffice.org/download/download-libreoffice/)

### 2. py

```py
import subprocess
import os
import platform


def word_to_pdf(input_file, output_file=None):
    # 获取输入文件所在目录
    input_dir = os.path.dirname(os.path.abspath(input_file))
    # 如果没有指定输出文件，就使用默认名称
    if not output_file:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(input_dir, f"{base_name}.pdf")

    # 根据不同操作系统确定 LibreOffice 可执行文件路径
    if platform.system() == "Windows":
        libreoffice_bin = r"C:\Program Files\LibreOffice\program\soffice.exe"
    elif platform.system() == "Darwin":  # macOS
        libreoffice_bin = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    else:  # Linux 及其他系统
        libreoffice_bin = "libreoffice"  # 假设已添加到 PATH

    # 检查可执行文件是否存在（Windows 和 macOS 需要检查）
    if platform.system() in ["Windows", "Darwin"] and not os.path.exists(libreoffice_bin):
        raise FileNotFoundError(f"未找到 LibreOffice 可执行文件: {libreoffice_bin}")

    try:
        # 构建命令
        cmd = [
            libreoffice_bin,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            input_dir,
            os.path.abspath(input_file)
        ]

        # 执行命令
        subprocess.run(cmd, check=True)
        print(f"成功将 {input_file} 转换为 {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e}")
    except FileNotFoundError as e:
        print(f"错误: 找不到 LibreOffice。请确保已安装并检查路径: {e}")


# 使用示例
if __name__ == "__main__":
    input_file = 'src.docx'
    output_file = 'dest.pdf'
    word_to_pdf(input_file, output_file)
```
