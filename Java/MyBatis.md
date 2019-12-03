# 入门

1. 在 pom.xml 文件中添加 Mybatis3.4.5 的坐标
    ```
    <dependency>
        <groupId>org.mybatis</groupId>
        <artifactId>mybatis</artifactId>
        <version>3.4.5</version>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>5.1.6</version>
        <scope>runtime</scope>
    </dependency>
    ```
2. 编写实体类
3. 编写持久层接口
    ```
    public interface IUserDao {
        /**
        * 查询所有用户
        * @return
        */
        List<User> findAll();
    }
    ```
4. 编写持久层接口的映射文件
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE mapper 
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
    <mapper namespace="com.test.dao.IUserDao">
        <!-- 配置查询所有操作 -->
        <select id="findAll" resultType="com.test.domain.User">
            select * from user
        </select>
    </mapper>
    ```
5. 编写 SqlMapConfig.xml 配置文件
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE configuration 
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN" 
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
    <configuration>
        <!-- 配置 mybatis 的环境 -->
        <environments default="mysql">
            <!-- 配置 mysql 的环境 -->
            <environment id="mysql">
                <!-- 配置事务的类型 -->
                <transactionManager type="JDBC"></transactionManager>
                <!-- 配置连接数据库的信息：用的是数据源(连接池) -->
                <dataSource type="POOLED">
                    <property name="driver" value="com.mysql.jdbc.Driver"/>
                    <property name="url" value="jdbc:mysql://localhost:3306/ee50"/>
                    <property name="username" value="root"/>
                    <property name="password" value="1234"/>
                </dataSource>
            </environment>
        </environments>
        <!-- 告知 mybatis 映射配置的位置 -->
        <mappers>
            <mapper resource="com.test/dao/IUserDao.xml"/>
        </mappers>
    </configuration>
    ```
6. 编写测试类
    ```
    public class MybatisTest {
        public static void main(String[] args)throws Exception {
            //1.读取配置文件
            InputStream in = Resources.getResourceAsStream("SqlMapConfig.xml");
            //2.创建 SqlSessionFactory 的构建者对象
            SqlSessionFactoryBuilder builder = new SqlSessionFactoryBuilder();
            //3.使用构建者创建工厂对象 SqlSessionFactory
            SqlSessionFactory factory = builder.build(in);
            //4.使用 SqlSessionFactory 生产 SqlSession 对象
            SqlSession session = factory.openSession();
            //5.使用 SqlSession 创建 dao 接口的代理对象
            IUserDao userDao = session.getMapper(IUserDao.class);
            //6.使用代理对象执行查询所有方法
            List<User> users = userDao.findAll();
            for(User user : users) {
                System.out.println(user);
            }
            //7.释放资源
            session.close();
            in.close();
        }
    }
    ```

# 增删改查

1. insert
    ```
    int saveUser(User user);
    
    <insert id="saveUser" parameterType="com.test.domain.User">
        insert into user(username,birthday,sex,address) 
        values(#{username},#{birthday},#{sex},#{address})
    </insert>
    ```
2. 新增用户后, 同时返回当前新增用户的 id
    ```
    int saveUser(User user);
    
    <insert id="saveUser" parameterType="com.test.domain.User">
        <!-- 获取插入的 id 并保存到传入的user对象中 -->
        <selectKey keyColumn="id" keyProperty="id" resultType="int">
            select last_insert_id();
        </selectKey>
        insert into user(username,birthday,sex,address) 
        values(#{username},#{birthday},#{sex},#{address})
    </insert>
    ```
3. delete
    ```
    int deleteUser(Integer userId);
    
    <delete id="deleteUser" parameterType="java.lang.Integer">
        delete from user where id = #{uid}
    </delete>
    ```
4. update
    ```
    int updateUser(User user);

    <update id="updateUser" parameterType="com.test.domain.User">
        update user set 
        username=#{username},
        birthday=#{birthday},
        sex=#{sex},
        address=#{address} where id=#{id}
    </update>
    ```
5. select
    ```
    User findById(Integer userId);
    
    <select id="findById" resultType="com.test.domain.User" parameterType="int">
        select * from user where id = #{uid}
    </select>
    ```

# \#{}与${}的区别

## \#{}表示一个占位符号
通过\#{}可以实现 preparedStatement 向占位符中设置值, 自动进行 java 类型和 jdbc 类型转换, 
\#{}可以有效防止 sql 注入。 
\#{}可以接收简单类型值或 pojo 属性值。 如果 parameterType 传输单个简单类型值, \#{}括号中可以是 value 或其它任意名称。
## ${}表示拼接 sql 串
通过${}可以将 parameterType 传入的内容拼接在 sql 中且不进行 jdbc 类型转换,  
${}可以接收简单类型值或 pojo 属性值, 如果 parameterType 传输单个简单类型值, ${}括号中只能是 value。

# resultMap 定义实体类中的属性和数据库列名的对应关系

建立 User 实体和数据库表的对应关系
- type 属性：指定实体类的全限定类名
- id 属性：给定一个唯一标识, 是给查询 select 标签引用用的。
- id 标签：用于指定主键字段
- result 标签：用于指定非主键字段
- column 属性：用于指定数据库列名
- property 属性：用于指定实体类属性名称
```
<resultMap type="com.test.domain.User" id="userMap">
    <id column="id" property="userId"/>
    <result column="username" property="userName"/>
    <result column="sex" property="userSex"/>
    <result column="address" property="userAddress"/>
    <result column="birthday" property="userBirthday"/>
</resultMap>
```
使用resultMap
```
<select id="findAll" resultMap="userMap">
    select * from user
</select>
```

# 动态SQL标签

## if 标签
   
if标签通常用于WHERE语句、UPDATE语句、INSERT语句中, 
通过判断参数值来决定是否使用某个查询条件、判断是否更新某一个字段、
判断是否插入某个字段的值。

```
<if test="name != null and name != ''">
         and NAME = #{name}
</if>
```

## foreach 标签

foreach标签主要用于构建in条件, 可在sql中对集合进行迭代。
也常用到批量删除、添加等操作中。

属性介绍：

- collection：collection属性的值有三个分别是list、array、map三种, 分别对应的参数类型为：List、数组、map集合。
- item ：表示在迭代过程中每一个元素的别名
- index ：表示在迭代过程中每次迭代到的位置（下标）
- open ：前缀
- close ：后缀
- separator ：分隔符, 表示迭代时每个元素之间以什么分隔

```
<!-- in查询所有, 不分页 -->
<select id="selectIn" resultMap="BaseResultMap">
    select name,hobby from student where id in
    <foreach item="item" index="index" collection="list" open="(" separator="," close=")">
        #{item}
    </foreach>
</select>
```

## where标签

where标签会知道如果它包含的标签中有返回值的话, 它就插入一个‘where’。
此外, 如果标签返回的内容是以AND 或OR 开头的, 则它会剔除掉。

```
<select id="getStudentListWhere" parameterType="Object" resultMap="BaseResultMap">     
    SELECT * from STUDENT      
       <where>   
         <if test="name!=null and name!='' ">     
            NAME LIKE CONCAT(CONCAT('%', #{name}),'%')      
         </if>     
         <if test="hobby!= null and hobby!= '' ">     
            AND hobby = #{hobby}      
         </if>  
       </where>        
</select>    
```

## set标签

当在update语句中使用if标签时, 如果最后的if没有执行, 则或导致逗号多余错误。
使用set标签可以将动态的配置set关键字, 和剔除追加到条件末尾的任何不相关的逗号。

```
<update id="updateStudent" parameterType="Object">     
    UPDATE STUDENT      
    <set>     
        <if test="name!=null and name!='' ">     
            NAME = #{name},      
        </if>     
        <if test="hobby!=null and hobby!='' ">     
            MAJOR = #{major},      
        </if> 
        <if test="hobby!=null and hobby!='' ">     
            HOBBY = #{hobby},  
        </if>     
    </set>     
    WHERE ID = #{id};      
</update>  
```

## trim标签

一般用于去除sql语句中多余的and关键字, 逗号, 或者给sql语句前拼接
“where“、“set“以及“values(“ 等前缀, 或者添加“)“等后缀, 
可用于选择性插入、更新、删除或者条件查询等操作。

trim属性主要有以下四个

- prefix：给sql语句拼接的前缀
- suffix：给sql语句拼接的后缀
- prefixOverrides：去除sql语句前面的关键字或者字符, 该关键字或者字符由prefixOverrides属性指定, 假设该属性指定为"AND", 当sql语句的开头为"AND", trim标签将会去除该"AND"
- suffixOverrides：去除sql语句后面的关键字或者字符, 该关键字或者字符由suffixOverrides属性指定

```
<insert id="insert" parameterType="Object">
    insert into student    
    <trim prefix="(" suffix=")" suffixOverrides=",">
        <if test="name != null">
            NAME,
        </if>
        <if test="hobby != null">
            HOBBY,
        </if>    
    </trim>    
    <trim prefix="values(" suffix=")" suffixOverrides=",">  
        <if test="name != null">
            #{name},
        </if>
        <if test="hobby != null">
            #{hobby},
        </if>
    </trim>
</insert>
```

## sql标签

定义常量

```
<sql id="Base_Column_List">
    ID,MAJOR,BIRTHDAY,AGE,NAME,HOBBY
</sql>
```

## include标签

用于引用定义的常量

```
<select id="selectAll" resultMap="BaseResultMap">
    SELECT
    <include refid="Base_Column_List" />
    FROM student
</select>
```

# 多表查询

## 一对一查询(多对一)

### 表

用户表

列名|类型|约束
-|-|-
i d|int|主键
用户名|varchar(20)|
性别|varchar(10)|
出生日期|date|
地址|varchar(60)|

账户表

列名|类型|约束
-|-|-
i d|int|主键
用户id|int|外键
金额|double|

### 定义账户实体类

```
public class Account {
    private Integer id;
    private Integer uid;
    private Double money;
    
    private User user;
}
```

### Mapper.xml

```
List<Account> findAll();

<mapper namespace="com.test.dao.IAccountDao">
    <!-- 建立对应关系 -->
    <resultMap type="account" id="accountMap">
        <id column="aid" property="id"/>
        <result column="uid" property="uid"/>
        <result column="money" property="money"/>
        <!-- 它是用于指定从表方的引用实体属性的 -->
        <association property="user" javaType="user">
            <id column="id" property="id"/>
            <result column="username" property="username"/>
            <result column="sex" property="sex"/>
            <result column="birthday" property="birthday"/>
            <result column="address" property="address"/>
        </association>
    </resultMap>
    <select id="findAll" resultMap="accountMap">
        select u.*,a.id as aid,a.uid,a.money 
        from account a,user u where a.uid =u.id;
    </select>
</mapper>
```

## 一对多查询

### 表

用户表

列名|类型|约束
-|-|-
i d|int|主键
用户名|varchar(20)|
性别|varchar(10)|
出生日期|date|
地址|varchar(60)|

账户表

列名|类型|约束
-|-|-
i d|int|主键
用户id|int|外键
金额|double|

### 定义用户实体类

```
public class User {
    private Integer id;
    private String username;
    private Date birthday;
    private String sex;
    private String address;
    
    private List<Account> accounts;
}
```

### Mapper.xml

collection部分定义了用户关联的账户信息。表示关联查询结果集

property="accList"：关联查询的结果集存储在 User 对象的上哪个属性。

ofType="account"：指定关联查询的结果集中的对象类型即List中的对象类型。此处可以使用别名, 也可以使用全限定名

```
List<User> findAll();

<mapper namespace="com.test.dao.IUserDao">
    <resultMap type="user" id="userMap">
        <id column="id" property="id"></id>
        <result column="username" property="username"/>
        <result column="address" property="address"/>
        <result column="sex" property="sex"/>
        <result column="birthday" property="birthday"/>

        <collection property="accounts" ofType="account">
            <id column="aid" property="id"/>
            <result column="uid" property="uid"/>
            <result column="money" property="money"/>
        </collection>
    </resultMap>
    <!-- 配置查询所有操作 -->
    <select id="findAll" resultMap="userMap">
        select u.*,a.id as aid ,a.uid,a.money 
        from user u left outer join account a 
        on u.id =a.uid
    </select>
</mapper>
```

## 多对多查询

### 表

用户表

列名|类型|约束
-|-|-
i d|int|主键
用户名|varchar(20)|
性别|varchar(10)|
出生日期|date|
地址|varchar(60)|

角色表

列名|类型|约束
-|-|-
i d|int|主键
角色名称|varchar(20)|
角色描述|varchar(20)|

用户角色中间表

列名|类型|约束
-|-|-
用户id|int|外键
角色id|int|外键

### 定义实体类
```
public class Role implements Serializable {
    private Integer roleId;
    private String roleName;
    private String roleDesc;
    //多对多的关系映射：一个角色可以赋予多个用户
    private List<User> users;
}
```

### Mapper.xml

```
List<Role> findAll();

<mapper namespace="com.test.dao.IRoleDao">
    <!--定义 role 表的 ResultMap-->
    <resultMap id="roleMap" type="role">
        <id property="roleId" column="rid"></id>
        <result property="roleName" column="role_name"></result>
        <result property="roleDesc" column="role_desc"></result>
        <collection property="users" ofType="user">
            <id column="id" property="id"></id>
            <result column="username" property="username"></result>
            <result column="address" property="address"></result>
            <result column="sex" property="sex"></result>
            <result column="birthday" property="birthday"></result>
        </collection>
    </resultMap>
    <!--查询所有-->
    <select id="findAll" resultMap="roleMap">
        select u.*,r.id as rid,r.role_name,r.role_desc 
        from role r left outer join user_role ur 
        on r.id = ur.rid
        left outer join user u 
        on u.id = ur.uid
    </select>
</mapper>
```

# 缓存

## 什么是缓存

存在于内存中的临时数据

## 为什么使用缓存

减少和数据库的交互次数, 提高执行效率

## 什么样的数据适合缓存

1. 经常查询并且不经常改变的数据
2. 数据的正确与否对最终结果影响不大的数据

## 什么样的数据不适合缓存
   
1. 经常改变的数据
2. 数据的正确与否对最终结果影响很大的数据

## MyBatis中的一级缓存

它指的是MyBatis中SqlSession对象的缓存

当我们执行查询后, 查询的结果会同时存入SqlSession提供的一块区域中,
该区域的结构是Map, 当我们再次查询同样的数据, 
MyBatis会先去SqlSession中查询, 有的话直接拿来用

当SqlSession对象消失后, 一级缓存也消失了

一级缓存中保存的是Java对象, 查询缓存会取出相同的对象

当调用 SqlSession 的修改, 添加, 删除, commit(), close()等方法时, 就会清空一级缓存

## MyBatis中的二级缓存

它指的是MyBatis中SqlSessionFactory对象的缓存, 
由同一个SqlSessionFactory对象创建的SqlSession对象会共享
SqlSessionFactory对象的缓存

二级缓存中保存的不是Java对象, 而是序列化后的数据, 
查询缓存会创建新对象, 并把数据赋值给新对象

### 开启二级缓存

1. 在 SqlMapConfig.xml 文件开启二级缓存
    ```
    <settings>
        <!-- 开启二级缓存的支持 -->
        <setting name="cacheEnabled" value="true"/>
    </settings>
    ```
2. 配置要使用缓存的 Mapper 映射文件
    ```
    <mapper namespace="com.test.dao.IUserDao">
        <!-- 开启二级缓存的支持 -->
        <cache/>
    </mapper>
    ```
3. 配置 statement 上面的 useCache 属性
    ```
    <!-- 根据 id 查询 -->
    <select id="findById" resultType="user" parameterType="int" useCache="true">
        select * from user where id = #{uid}
    </select>
    ```

### 注意

当我们在使用二级缓存时, 所缓存的类一定要实现 java.io.Serializable 接口, 这种就可以使用序列化
方式来保存对象

# 延迟加载

就是在需要用到数据时才进行加载, 不需要用到数据时就不加载数据。延迟加载也称懒加载.
好处：先从单表查询, 需要时再从关联表去关联查询, 大大提高数据库性能, 因为查询单表要比关联查询多张表速
度要快

## 配置 SqlMapConfig.xml 文件打开延迟加载

```
<settings>
    <setting name="lazyLoadingEnabled" value="true"/>
    <setting name="aggressiveLazyLoading" value="false"/>
</settings>

```

## 使用 association 实现延迟加载


```
List<Account> findAll();

<mapper namespace="com.test.dao.IAccountDao">
    <!-- 建立对应关系 -->
    <resultMap type="account" id="accountMap">
        <id column="aid" property="id"/>
        <result column="uid" property="uid"/>
        <result column="money" property="money"/>
        <!-- 它是用于指定从表方的引用实体属性的 -->
        <!-- select： 填写我们要调用的 select 映射的 id  -->
        <!-- column ： 填写我们要传递给 select 映射的参数 -->
        <association property="user" javaType="user"
            select="com.test.dao.IUserDao.findById"
            column="uid"/>
    </resultMap>
    <select id="findAll" resultMap="accountMap">
        select * from account
    </select>
</mapper>
```
com.test.dao.IUserDao
```
User findById(Integer userId);

<mapper namespace="com.test.dao.IUserDao">
    <!-- 根据 id 查询 -->
    <select id="findById" resultType="user" parameterType="int" >
        select * from user where id = #{uid}
    </select>
</mapper>
```

## 使用 Collection 实现延迟加载

```
List<User> findAll();

<mapper>
    <resultMap type="user" id="userMap">
        <id column="id" property="id"></id>
        <result column="username" property="username"/>
        <result column="address" property="address"/>
        <result column="sex" property="sex"/>
        <result column="birthday" property="birthday"/>
        <!-- 
            collection 是用于建立一对多中集合属性的对应关系
            ofType 用于指定集合元素的数据类型
            select 是用于指定查询账户的唯一标识（账户的 dao 全限定类名加上方法名称）
            column 是用于指定使用哪个字段的值作为条件查询
            collection标签：
            主要用于加载关联的集合对象
            select 属性：
            用于指定查询 account 列表的 sql 语句, 所以填写的是该 sql 映射的 id
            column 属性：
            用于指定 select 属性的 sql 语句的参数来源, 上面的参数来自于 user 的 id 列, 所以就写成 id 这一
            个字段名了
        -->
        <collection property="accounts" ofType="account"
            select="com.test.dao.IAccountDao.findByUid"
            column="id"/>
    </resultMap>
    <!-- 配置查询所有操作 -->
    <select id="findAll" resultMap="userMap">
        select * from user
    </select>
</mapper>
```
com.test.dao.IAccountDao
```
<!-- 根据用户 id 查询账户信息 -->
<select id="findByUid" resultType="account" parameterType="int">
    select * from account where uid = #{uid}
</select>
```
