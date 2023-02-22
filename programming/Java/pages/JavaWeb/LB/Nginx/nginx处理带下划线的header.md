# nginx处理带下划线的header

## 问题描述： 

通过nginx反向代理到tomcat，自定义Header中，其中带下划线的Hdader在tomcat应用中获取不到，类似于n_name/cookie_sig这样的名称； 

## 处理办法： 

1. 配置中http部分 增加`underscores_in_headers on;` 配置 
2. 用减号-替代下划线符号_，避免这种变态问题。nginx默认忽略掉下划线可能有些原因。 
