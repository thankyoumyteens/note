import os
import re
from pathlib import Path
import shutil

dist_path = Path(os.path.abspath(os.path.dirname(__file__)))
note_app_path = dist_path.parent / 'note_app'
books_path = note_app_path / 'assets' / 'books'
pubspec_path = note_app_path / 'pubspec.yaml'
assets_list = []

def copy_files(base_path, book_name):
    book_path = books_path / book_name
    shutil.rmtree(str(book_path))
    book_path.mkdir(parents=True)
    assets_path = 'assets/books/' + book_name
    file_list = []
    summary_info = []
    # 提取SUMMARY.md文件中的信息
    summary_path = base_path / 'SUMMARY.md'
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
                file_list.append({
                    'src_path' : base_path / relative_path,
                    'dst_path' : book_path / relative_path,
                })
    # 复制SUMMARY.md文件
    assets_list.append(assets_path + '/SUMMARY.md')
    with open(book_path / 'SUMMARY.md', 'w', encoding='utf-8') as f:
        for info in summary_info:
            assets_list.append(info["path"])
            f.write(f'{info["spaces"]}- [{info["title"]}]({info["path"]})\n')
            f.flush()
    # 复制图片
    img_path = base_path / 'img'
    dst_img_path = book_path / 'img'
    if not dst_img_path.exists():
        dst_img_path.mkdir(parents=True)
    for img in img_path.glob('*'):
        shutil.copy(img, dst_img_path)
    # 复制其他md文件
    for file in file_list:
        with file['src_path'].open('r', encoding='utf-8') as f:
            if not file['dst_path'].parent.exists():
                file['dst_path'].parent.mkdir(parents=True)
            with file['dst_path'].open('w', encoding='utf-8') as fw:
                for line in f:
                    m = re.match(r'(\s*)!\[(.*)\]\((.*)\)', line)
                    if m:
                        spaces = m.group(1)
                        img_alt = m.group(2)
                        img_path = m.group(3)
                        img_path = re.sub(r'^(\.*/)*', '', img_path)
                        assets_list.append(f'{assets_path}/{img_path}')
                        fw.write(f'{spaces}![{img_alt}](resource:{assets_path}/{img_path})\n')
                    else:
                        fw.write(line)
                fw.write(f'\n[返回目录]({assets_path}/SUMMARY.md)\n')
                fw.flush()

# jvm

jvm_path = dist_path / 'programming' / 'Java' / 'md' / 'jvm' / 'src'
copy_files(jvm_path, 'jvm')

with pubspec_path.open('w', encoding='utf-8') as f:
    f.write('name: note_app\n')
    f.write('description: "A new Flutter project."\n')
    f.write("publish_to: 'none'\n")
    f.write('version: 1.0.0+1\n')
    f.write('environment:\n')
    f.write("  sdk: '>=3.2.6 <4.0.0'\n")
    f.write('dependencies:\n')
    f.write('  flutter:\n')
    f.write('    sdk: flutter\n')
    f.write('  flutter_markdown: ^0.6.18+3\n')
    f.write('  cupertino_icons: ^1.0.2\n')
    f.write('dev_dependencies:\n')
    f.write('  flutter_test:\n')
    f.write('    sdk: flutter\n')
    f.write('  flutter_lints: ^2.0.0\n')
    f.write('flutter:\n')
    f.write('  uses-material-design: true\n')
    f.write('  assets:\n')
    for assests in assets_list:
        f.write(f'    - {assests}\n')
    f.flush()


input('Press Enter to continue...')
