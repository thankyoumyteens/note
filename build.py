import os
import re
import subprocess
from pathlib import Path
import shutil

dist_path = Path(os.path.abspath(os.path.dirname(__file__)))
note_app_path = dist_path.parent / "note_app"
books_path = note_app_path / "assets" / "books"
pubspec_path = note_app_path / "pubspec.yaml"
assets_list = []

def get_script(url):
    # 向flutter发送当前页面的url
    return "<script>\n" \
           f"UrlLogger.postMessage('{url}');\n" \
           "</script>\n"

def is_html(path):
    if path.endswith(".html"):
        return True
    return False

def handle_html(source_path, dest_path, simple_path):
    with source_path.open("r", encoding="utf-8") as f:
        with dest_path.open("w", encoding="utf-8") as fw:
            for line in f:
                body_match = re.match('^\s*</body>$', line)
                if body_match:
                    fw.write(get_script(simple_path) + "</body>\n")
                else:
                    fw.write(line)
            fw.flush()

def copy_files(source_path, book_name):
    dest_path = books_path / book_name
    assets_prefix = "assets/books/" + book_name
    if dest_path.exists():
        shutil.rmtree(str(dest_path))
    dest_path.mkdir(parents=True, exist_ok=True)
    subprocess.call(["mdbook", "build"], cwd=source_path)
    book_path = source_path / "book"
    for file_path in book_path.glob("**/*"):
        simple_path = file_path.relative_to(book_path)
        simple_path = str(simple_path).replace("\\", "/")
        if file_path.is_file():
            assets_list.append(assets_prefix + "/" + simple_path)
            print(simple_path)
            if is_html(simple_path):
                handle_html(file_path, dest_path / simple_path, simple_path)
                continue
            shutil.copy(str(file_path), str(dest_path / simple_path))
        else:
            # 创建文件夹
            dest_dir = dest_path / simple_path
            dest_dir.mkdir(parents=True, exist_ok=True)


# jvm
jvm_path = dist_path / "programming" / "Java" / "md" / "jvm"
copy_files(jvm_path, "jvm")
# jvm
jvm_path = dist_path / "programming" / "Java" / "md" / "gc"
copy_files(jvm_path, "gc")

with pubspec_path.open("w", encoding="utf-8") as f:
    f.write("name: note_app\n")
    f.write('description: "A new Flutter project."\n')
    f.write("publish_to: 'none'\n")
    f.write("version: 1.0.0+1\n")
    f.write("environment:\n")
    f.write("  sdk: '>=3.2.6 <4.0.0'\n")
    f.write("dependencies:\n")
    f.write("  flutter:\n")
    f.write("    sdk: flutter\n")
    # f.write("  flutter_markdown: ^0.6.18+3\n")
    f.write("  jaguar: ^3.1.3\n")
    f.write("  jaguar_flutter_asset: ^3.0.0\n")
    f.write("  webview_flutter: ^4.7.0\n")
    f.write("  shared_preferences: ^2.2.2\n")
    f.write("  cupertino_icons: ^1.0.2\n")
    f.write("dev_dependencies:\n")
    f.write("  flutter_test:\n")
    f.write("    sdk: flutter\n")
    f.write("  flutter_lints: ^2.0.0\n")
    f.write("flutter:\n")
    f.write("  uses-material-design: true\n")
    f.write("  assets:\n")
    for assests in assets_list:
        f.write(f"    - {assests}\n")
    f.flush()


input("Press Enter to continue...")
