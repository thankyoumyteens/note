# 缓存

mybatis 的缓存保存在本地, 基于 PerpetualCache, 本质是一个 HashMap。

## 一级缓存

基于 PerpetualCache 的 HashMap 本地缓存, 作用域是 sqlSession。当 sqlSession 执行插入, 更新, 删除或 close 之后, 缓存清空。

一级缓存默认开启。

```java
public void testCache1() throws Exception{
    SqlSessionsqlSession = sqlSessionFactory.openSession();
    UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
    User user1 = userMapper.findUserById(1);
    System.out.println(user1);
    User user2 = userMapper.findUserById(1);
    System.out.println(user2);
    sqlSession.close();
}
```

## 二级缓存

基于 PerpetualCache 的 HashMap 本地缓存, 作用域是 namespace, 一个 namespace 对应一个二级缓存。

二级缓存需要手动开启。

1. 在 MyBatis 配置文件（一般是 mybatis-config.xml）中开启二级缓存

```xml
<setting name="cacheEnabled" value="true"/>
```

2. 到对应的 xxxMapper.xml 中配置二级缓存

```xml
<cache/>
```

3. 配置之后, xxxMapper.xml 文件中的 select 语句将会被缓存, 而 insert、update、delete 则会刷新缓存。
