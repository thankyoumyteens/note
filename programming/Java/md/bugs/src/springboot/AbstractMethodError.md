# java.lang.AbstractMethodError

项目部署后报错: 

```
org.springframework.web.util.NestedServletException: Handler dispatch failed; nested exception is java.lang.AbstractMethodError: Method com/xxx/event/EventSignStatusChanged.getAgentUUID()Ljava/lang/String; is abstract
        at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1055)
        at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:943)
        at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006)
        at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:909)
        at javax.servlet.http.HttpServlet.service(HttpServlet.java:517)
        at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883)
        at javax.servlet.http.HttpServlet.service(HttpServlet.java:584)
        at io.undertow.servlet.handlers.ServletHandler.handleRequest(ServletHandler.java:74)
        at io.undertow.servlet.handlers.FilterHandler$FilterChainImpl.doFilter(FilterHandler.java:129)
        at com.alibaba.druid.support.http.WebStatFilter.doFilter(WebStatFilter.java:124)
        at io.undertow.servlet.core.ManagedFilter.doFilter(ManagedFilter.java:61)
        at io.undertow.servlet.handlers.FilterHandler$FilterChainImpl.doFilter(FilterHandler.java:131)
        at com.xxx.boss.base.boot.request.BossRequestFilter.doFilter(BossRequestFilter.java:34)
        at io.undertow.servlet.core.ManagedFilter.doFilter(ManagedFilter.java:61)
        at io.undertow.servlet.handlers.FilterHandler$FilterChainImpl.doFilter(FilterHandler.java:131)
        at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100)
        at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
        at io.undertow.servlet.core.ManagedFilter.doFilter(ManagedFilter.java:61)
        at io.undertow.servlet.handlers.FilterHandler$FilterChainImpl.doFilter(FilterHandler.java:131)
        at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93)
        at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
        at io.undertow.servlet.core.ManagedFilter.doFilter(ManagedFilter.java:61)
        at io.undertow.servlet.handlers.FilterHandler$FilterChainImpl.doFilter(FilterHandler.java:131)
        at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201)
        at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
        at io.undertow.servlet.core.ManagedFilter.doFilter(ManagedFilter.java:61)
        at io.undertow.servlet.handlers.FilterHandler$FilterChainImpl.doFilter(FilterHandler.java:131)
```

## 原因

发现是将实体类转成json时报的错, 本地没问题, 部署到服务器上就报错。

本地查找EventSignStatusChanged.getAgentUUID()方法, 没找到。

把服务器上的jar包下载下来查找EventSignStatusChanged.getAgentUUID()方法, 发现在EventSignStatusChanged的父类的父类Event类里。

把线上的Event类与本地的Event类对比, 发现内容不一致。

```java
// 本地的
package com.xxx.cti;

import java.util.Map;

public interface Event extends Message {
  long getReferenceID();
  
  void setReferenceID(long paramLong);
  
  String getCompanyId();
  
  Map<String, String> getAttachedData();
}
```

```java
// 线上的
package com.xxx.cti;

import java.util.Map;

public interface Event extends Message {
  Map<String, String> getAttachedData();
  
  String getAgentUUID();
  
  void setAgentUUID(String paramString);
  
  String getThisDN();
  
  void setThisDN(String paramString);
}
```

原因: 本地和线上用的不同的maven仓库, 下载的jar包不一样。
