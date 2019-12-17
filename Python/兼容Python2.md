# python2 报错：UnicodeDecodeError: 'ascii' codec can't decode byte 0xe8 in position 0: ordinal not in range(128)

解决方法

```
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
```

# write() argument 1 must be unicode, not str 

```
import codecs
fpred = codecs.open('pred_res.txt', 'w', 'utf-8')
fpred.write('abc\n'.decode('utf-8'))
fpred.close()
```

# TypeError: 'encoding' is an invalid keyword argument for this function

```
data_file = open("F:\\MyPro\\data.yaml", "r", encoding='utf-8')
```
运行的时候报错 `TypeError: 'encoding' is an invalid keyword argument for this function`

网上查找一番后, 改成如下这样就可以搞定
```
import io
data_file = io.open("F:\\MyPro\\data.yaml", "r", encoding='utf-8')
```
