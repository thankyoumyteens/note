import os
import subprocess
from pathlib import Path
import shutil

dist_path = Path(os.path.abspath(os.path.dirname(__file__)))
note_app_path = dist_path.parent / "note_app"
books_path = note_app_path / "assets" / "books"
pubspec_path = note_app_path / "pubspec.yaml"
assets_list = []


def copy_files(source_path, book_name):
    dest_path = books_path / book_name
    assets_prefix = "assets/books/" + book_name
    if dest_path.exists():
        shutil.rmtree(str(dest_path))
    subprocess.call(["mdbook", "build"], cwd=source_path)
    book_path = source_path / "book"
    for file_path in book_path.glob("**/*"):
        if file_path.is_file():
            simple_path = file_path.relative_to(book_path)
            simple_path = str(simple_path).replace("\\", "/")
            assets_list.append(assets_prefix + "/" + simple_path)
    shutil.copytree(str(book_path), str(dest_path))


# jvm
jvm_path = dist_path / "programming" / "Java" / "md" / "jvm"
copy_files(jvm_path, "jvm")

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
