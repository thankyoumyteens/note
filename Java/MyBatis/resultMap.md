# 定义实体类中的属性和数据库列名的对应关系

建立 User 实体和数据库表的对应关系
- type 属性:指定实体类的全限定类名
- id 属性:给定一个唯一标识, 是给查询 select 标签引用用的。
- id 标签:用于指定主键字段
- result 标签:用于指定非主键字段
- column 属性:用于指定数据库列名
- property 属性:用于指定实体类属性名称
```xml
<resultMap type="com.test.domain.User" id="userMap">
	<id column="id" property="userId"/>
	<result column="username" property="userName"/>
	<result column="sex" property="userSex"/>
	<result column="address" property="userAddress"/>
	<result column="birthday" property="userBirthday"/>
</resultMap>
```
使用resultMap
```xml
<select id="findAll" resultMap="userMap">
	select * from user
</select>
```
