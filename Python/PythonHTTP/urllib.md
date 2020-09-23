# urllib和urllib2

模块urllib和urllib2的功能差不多，简单来说urllib2是urllib的增强——urllib2更好一些，但是urllib中有urllib2中所没有的函数。在Python2.x中主要为urllib和urllib2，这两个标准库是不可相互替代的。但是在Python3.x中将urllib2合并到了urllib。因此Python2.x中，urllib和urllib2两者搭配使用。

# 发起GET请求
在urlopen()方法中传入字符串格式的url地址，则此方法会访问目标网址，然后返回访问的结果。

## python3
Python3中urlopen()函数返回的是http.client.HTTPResponse对象：
http.client.HTTPResponse对象大概包括read()、readinto()、getheader()、getheaders()、fileno()、msg、version、status、reason、debuglevel和closed函数，其实一般而言使用read()函数后还需要decode()函数，这里一个巨大的优势就是：返回的网页内容实际上是没有被解码的，在read()得到内容后通过指定decode()函数参数，可以使用对应的解码方式。

```python
from urllib import request

params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
resp = request.urlopen("http://www.musi-cal.com/cgi-bin/query?%s" % params)
print(resp.read().decode('gbk'))
```
## python2
Python2中urlopen()函数返回的是addinfourl对象：
addinfourl对象实际上是一个类似于文件的对象，大概包括read()、readline()、readlines()、fileno()、close()、info()、getcode()和geturl()函数，其实这里隐藏了一个巨大的缺陷：返回的网页内容实际上已经被默认解码了，而不是由自己决定如何解码。
```python
import urllib
params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
f = urllib.urlopen("http://www.musi-cal.com/cgi-bin/query?%s" % params)
print f.read()
```

# 发起POST请求

## python3
urlopen()默认的访问方式是GET，当在urlopen()方法中传入data参数时，则会发起POST请求。注意：传递的data数据需要为bytes格式。timeout参数还可以设置超时时间，如果请求时间超出，那么就会抛出异常。

```python
from urllib import request

resp = request.urlopen('http://httpbin.org/post', data=b'word=hello', timeout=10)
print(resp.read().decode('gbk'))
```
## python2
```python
import urllib
params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
f = urllib.urlopen("http://www.musi-cal.com/cgi-bin/query", params)
print f.read()
```

# url编码解码

## python3
```python
from urllib import parse

keyword = '南北'
parse.quote(keyword)
# '%E5%8D%97%E5%8C%97'

parse.unquote(r'%E5%8D%97%E5%8C%97')
# '南北'
```

# 添加Headers

通过urllib发起的请求会有默认的一个Headers："User-Agent":"Python-urllib/3.6"，指明请求是由urllib发送的。
所以遇到一些验证User-Agent的网站时，我们需要自定义Headers，而这需要借助于urllib.request中的Request对象。
## python3
```python
from urllib import request

url = 'http://httpbin.org/get'
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

# 需要使用url和headers生成一个Request对象，
# 然后将其传入urlopen方法中
req = request.Request(url, headers=headers)
resp = request.urlopen(req)
print(resp.read().decode())
```
## python2
```python
import urllib2
 
# 设置浏览器请求头
ua_headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
}
#建立请求内容
request=urllib2.Request("http://baidu.com/",headers=ua_headers)
#获取响应
response=urllib2.urlopen(request)
#页面内容
html=response.read()
```

## Request对象
如上所示，urlopen()方法中不止可以传入字符串格式的url，也可以传入一个Request对象来扩展功能，Request对象如下所示。
```python
class urllib.request.Request(url, data=None, headers={},
                             origin_req_host=None,
                             unverifiable=False, method=None)
```
构造Request对象必须传入url参数，data数据和headers都是可选的。
最后，Request方法可以使用method参数来自由选择请求的方法，如PUT，DELETE等等，默认为GET。

#  添加Cookie

为了在请求时能带上Cookie信息，我们需要重新构造一个opener。
使用request.build_opener方法来进行构造opener，将我们想要传递的cookie配置到opener中，然后使用这个opener的open方法来发起请求。
```python
from http import cookiejar
from urllib import request

url = 'https://www.baidu.com'
# 创建一个cookiejar对象
cookie = cookiejar.CookieJar()
# 使用HTTPCookieProcessor创建cookie处理器
cookies = request.HTTPCookieProcessor(cookie)
# 并以它为参数创建Opener对象
opener = request.build_opener(cookies)
# 使用这个opener来发起请求
resp = opener.open(url)
# 查看之前的cookie对象，则可以看到访问百度获得的cookie
for i in cookie:
    print(i)
```
或者也可以把这个生成的opener使用install_opener方法来设置为全局的，之后使用urlopen方法发起请求时，都会带上这个cookie：
```python
# 将这个opener设置为全局的opener
request.install_opener(opener)
resp = request.urlopen(url)
```

# 设置Proxy代理

```python
from urllib import request

url = 'http://httpbin.org/ip'
proxy = {'http':'218.18.232.26:80','https':'218.18.232.26:80'}
# 创建代理处理器
proxies = request.ProxyHandler(proxy)
# 创建opener对象
opener = request.build_opener(proxies)
resp = opener.open(url)
print(resp.read().decode())
```

# 下载文件

在我们进行网络请求时常常需要保存图片或音频等数据到本地，一种方法是使用python的文件操作，将read()获取的数据保存到文件中。
而urllib提供了一个urlretrieve()方法，可以简单的直接将请求获取的数据保存成文件。
```python
from urllib import request

url = 'http://python.org/'
# urlretrieve()方法传入的第二个参数为文件保存的位置，以及文件名。
request.urlretrieve(url, 'python.html')
```
注：urlretrieve()方法是Python2.x直接移植过来的方法，以后有可能在某个版本中弃用。

