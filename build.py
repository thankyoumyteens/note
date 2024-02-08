import os
import re
from pathlib import Path

dist_path = Path(os.path.abspath(os.path.dirname(__file__)))
note_app_path = dist_path.parent / 'note_app'
books_path = note_app_path / 'assets' / 'books'
# pubspec_path = note_app_path / 'pubspec.yaml'


def copy_files(base_path, book_name):
    book_path = books_path / book_name
    assets_path = 'assets/books/' + book_name
    summary_path = base_path / 'SUMMARY.md'
    file_list = []
    summary_info = []
    # 提取SUMMARY.md文件中的信息
    with summary_path.open('r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'(\s*)-\s*\[(.*)\]\((.*)\)', line)
            if m:
                spaces = m.group(1)
                title = m.group(2)
                relative_path = m.group(3)
                relative_path = re.sub(r'^\.*/', '', relative_path)
                summary_info.append({
                    'title': title,
                    'path': assets_path + '/' + relative_path,
                    'spaces': spaces,
                })
                file_path = base_path / relative_path
                file_list.append(file_path)
    # 复制SUMMARY.md文件
    with open(book_path / 'SUMMARY.md', 'w', encoding='utf-8') as f:
        for info in summary_info:
            f.write(f'{info["spaces"]}- [{info["title"]}]({info["path"]})\n')
            f.flush()
    # 复制其他文件

# jvm

jvm_path = dist_path / 'programming' / 'Java' / 'md' / 'jvm' / 'src'
copy_files(jvm_path, 'jvm')


input('Press Enter to continue...')
