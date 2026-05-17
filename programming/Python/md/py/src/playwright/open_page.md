# 打开网页

新建：

```text
demo.py
```

写入：

```python
from playwright.sync_api import sync_playwright


def main():
    # 直接指定浏览器路径
    CHROME_PATH = '/Users/walter/walter/software/chrome-133.0.6871.0/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'

    with sync_playwright() as p:
        # 启动 Chromium
        browser = p.chromium.launch(
            # 如果不传, 就会使用默认路径
            executable_path=CHROME_PATH,
            headless=False
        )
        page = browser.new_page()
        # 打开百度
        page.goto("https://www.baidu.com")
        # 等待 3 秒
        page.wait_for_timeout(3000)
        # 打印页面标题
        print(page.title())
        # 关闭浏览器
        browser.close()


if __name__ == "__main__":
    main()
```

运行：

```bash
python demo.py
```

注意：这里的 `wait_for_timeout(3000)` 只是入门演示，真实脚本里不要依赖固定 sleep。
