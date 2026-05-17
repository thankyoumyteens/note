# 定位元素

Python Playwright 里定位元素主要靠 **Locator**。入门阶段记住一句话：

```text
优先用用户可见语义定位，最后才用 CSS / XPath。
```

推荐顺序：

```text
get_by_role()
get_by_text()
get_by_label()
get_by_placeholder()
get_by_alt_text()
get_by_title()
get_by_test_id()
locator("css")
locator("xpath=...")
```
