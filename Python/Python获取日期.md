# python获取当前时间
```
import datetime
now_time = datetime.datetime.now()
```
# 日期格式化
字符串转datetime
```
string = '2014-01-08 11:59:58'
time1 = datetime.datetime.strptime(string,'%Y-%m-%d %H:%M:%S')
# 2014-01-08 11:59:58
```
datetime转字符串
```
time1_str = datetime.datetime.strftime(time1,'%Y-%m-%d %H:%M:%S')
# 2014-01-08 11:59:58
```

# 获取年月日时分秒
```
print ("当前的年份是 %s" %i.year)
print ("当前的月份是 %s" %i.month)
print ("当前的日期是 %s" %i.day)
print ("当前小时是 %s" %i.hour)
print ("当前分钟是 %s" %i.minute)
print ("当前秒是 %s" %i.second)
```
