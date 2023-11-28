解决的问题: 在service类中获取request和response

RequestContextHolder这个类里面有两个ThreadLocal保存当前线程下的request和response

RequestContextHolder的使用
```java
RequestAttributes requestAttributes = RequestContextHolder.getRequestAttributes();
// 从session里面获取对应的值
String str = (String) requestAttributes.getAttribute("name", RequestAttributes.SCOPE_SESSION);

HttpServletRequest request = ((ServletRequestAttributes)requestAttributes).getRequest();
HttpServletResponse response = ((ServletRequestAttributes)requestAttributes).getResponse();
```
