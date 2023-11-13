# import 绝对路径

```python
import importlib.util
my_util_spec = importlib.util.spec_from_file_location('my_util', "C:/my_util.py")
my_util = importlib.util.module_from_spec(my_util_spec)
my_util_spec.loader.exec_module(my_util)

print(my_util.test())
```
