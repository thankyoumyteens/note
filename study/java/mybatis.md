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
    <mapper namespace="com.itheima.dao.IUserDao">
        <!-- 配置查询所有操作 -->
        <select id="findAll" resultType="com.itheima.domain.User">
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
            <mapper resource="com/itheima/dao/IUserDao.xml"/>
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
    
    <insert id="saveUser" parameterType="com.itheima.domain.User">
        insert into user(username,birthday,sex,address) 
        values(#{username},#{birthday},#{sex},#{address})
    </insert>
    ```
2. 新增用户后，同时返回当前新增用户的 id
    ```
    int saveUser(User user);
    
    <insert id="saveUser" parameterType="com.itheima.domain.User">
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

    <update id="updateUser" parameterType="com.itheima.domain.User">
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
    
    <select id="findById" resultType="com.itheima.domain.User" parameterType="int">
        select * from user where id = #{uid}
    </select>
    ```

# \#{}与${}的区别

## \#{}表示一个占位符号
通过\#{}可以实现 preparedStatement 向占位符中设置值，自动进行 java 类型和 jdbc 类型转换，
\#{}可以有效防止 sql 注入。 
\#{}可以接收简单类型值或 pojo 属性值。 如果 parameterType 传输单个简单类型值，\#{}括号中可以是 value 或其它任意名称。
## ${}表示拼接 sql 串
通过${}可以将 parameterType 传入的内容拼接在 sql 中且不进行 jdbc 类型转换， 
${}可以接收简单类型值或 pojo 属性值，如果 parameterType 传输单个简单类型值，${}括号中只能是 value。

# resultMap 定义实体类中的属性和数据库列名的对应关系

建立 User 实体和数据库表的对应关系
- type 属性：指定实体类的全限定类名
- id 属性：给定一个唯一标识，是给查询 select 标签引用用的。
- id 标签：用于指定主键字段
- result 标签：用于指定非主键字段
- column 属性：用于指定数据库列名
- property 属性：用于指定实体类属性名称
```
<resultMap type="com.itheima.domain.User" id="userMap">
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

