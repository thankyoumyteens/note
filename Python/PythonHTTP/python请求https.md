# SSL: CERTIFICATE_VERIFY_FAILED

原因分析: Python 2.7.9 之后版本, 当urllib.urlopen一个 https 的时候会验证一次 SSL 证书 ，当目标使用的是自签名的证书时就会爆出该错误消息。

解决办法: 在全局添加如下代码：
```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```
