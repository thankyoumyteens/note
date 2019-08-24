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

