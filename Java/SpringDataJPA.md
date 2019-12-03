# ORM概述

ORM（Object-Relational Mapping） 表示对象关系映射。在面向对象的软件开发中, 通过ORM, 就可以把对象映射到关系型数据库中。只要有一套程序能够做到建立对象与数据库的关联, 操作对象就可以直接操作数据库数据, 就可以说这套程序实现了ORM对象关系映射

简单的说：ORM就是建立实体类和数据库表之间的关系, 从而达到操作实体类就相当于操作数据库表的目的。

# hibernate与JPA的概述

JPA和Hibernate的关系就像JDBC和JDBC驱动的关系, JPA是规范, Hibernate除了作为ORM框架之外, 它也是一种JPA实现。JPA怎么取代Hibernate呢？JDBC规范可以驱动底层数据库吗？答案是否定的, 也就是说, 如果使用JPA规范进行数据库操作, 底层需要hibernate作为其实现类完成数据持久化工作。

# JPA快速入门

## 导入依赖
```
<dependencies>
    <!-- junit -->
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.12</version>
        <scope>test</scope>
    </dependency>

    <!-- hibernate对jpa的支持包 -->
    <dependency>
        <groupId>org.hibernate</groupId>
        <artifactId>hibernate-entitymanager</artifactId>
        <version>${project.hibernate.version}</version>
    </dependency>

    <!-- c3p0 -->
    <dependency>
        <groupId>org.hibernate</groupId>
        <artifactId>hibernate-c3p0</artifactId>
        <version>${project.hibernate.version}</version>
    </dependency>

    <!-- log日志 -->
    <dependency>
        <groupId>log4j</groupId>
        <artifactId>log4j</artifactId>
        <version>1.2.17</version>
    </dependency>

    <!-- Mysql and MariaDB -->
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>5.1.6</version>
    </dependency>
</dependencies>
```

## 编写实体类和数据库表的映射配置

```
//声明实体类
@Entity 
//建立实体类和表的映射关系
@Table(name="cst_customer") 
public class Customer {
	//声明当前私有属性为主键
	@Id
	//配置主键的生成策略
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	//指定和表中cust_id字段的映射关系
	@Column(name="cust_id") 
	private Long custId;
	
	@Column(name="cust_name")
	private String custName;
	
	@Column(name="cust_source")
	private String custSource;
	
	@Column(name="cust_industry")
	private String custIndustry;
	
	@Column(name="cust_level")
	private String custLevel;
	
	@Column(name="cust_address")
	private String custAddress;
	
	@Column(name="cust_phone")
	private String custPhone;
	
	// getter and setter
}
```

## 配置JPA的核心配置文件

在java工程的src路径下创建一个名为META-INF的文件夹, 在此文件夹下创建一个名为persistence.xml的配置文件

```
<?xml version="1.0" encoding="UTF-8"?>
<persistence xmlns="http://java.sun.com/xml/ns/persistence"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://java.sun.com/xml/ns/persistence  
    http://java.sun.com/xml/ns/persistence/persistence_2_0.xsd"
	version="2.0">
	<!--配置持久化单元 
		name：持久化单元名称 
		transaction-type：事务类型
		 	RESOURCE_LOCAL：本地事务管理 
		 	JTA：分布式事务管理 -->
	<persistence-unit name="myJpa" transaction-type="RESOURCE_LOCAL">
		<!--配置JPA规范的服务提供商 -->
		<provider>org.hibernate.jpa.HibernatePersistenceProvider</provider>
		<properties>
			<!-- 数据库驱动 -->
			<property name="javax.persistence.jdbc.driver" value="com.mysql.jdbc.Driver" />
			<!-- 数据库地址 -->
			<property name="javax.persistence.jdbc.url" value="jdbc:mysql://localhost:3306/ssh" />
			<!-- 数据库用户名 -->
			<property name="javax.persistence.jdbc.user" value="root" />
			<!-- 数据库密码 -->
			<property name="javax.persistence.jdbc.password" value="111111" />

			<!--jpa提供者的可选配置：我们的JPA规范的提供者为hibernate, 所以jpa的核心配置中兼容hibernate的配 -->
			<property name="hibernate.show_sql" value="true" />
			<property name="hibernate.format_sql" value="true" />
			<property name="hibernate.hbm2ddl.auto" value="create" />
		</properties>
	</persistence-unit>
</persistence>
```

## 实现保存操作

```
@Test
public void test() {
    /**
     * 创建实体管理类工厂, 借助Persistence的静态方法获取
     * 		其中传递的参数为持久化单元名称, 需要jpa配置文件中指定
     */
    EntityManagerFactory factory = Persistence.createEntityManagerFactory("myJpa");
    //创建实体管理类
    EntityManager em = factory.createEntityManager();
    //获取事务对象
    EntityTransaction tx = em.getTransaction();
    //开启事务
    tx.begin();
    Customer c = new Customer();
    c.setCustName("传智播客");
    //保存操作
    em.persist(c);
    //提交事务
    tx.commit();
    //释放资源
    em.close();
    factory.close();
}
```

# Spring Data JPA的快速入门

## 引入Spring Data JPA的坐标
```
<dependencies>
    <!-- spring -->
    <dependency>
        <groupId>org.aspectj</groupId>
        <artifactId>aspectjweaver</artifactId>
        <version>1.6.8</version>
    </dependency>

    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-aop</artifactId>
        <version>${spring.version}</version>
    </dependency>

    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
        <version>${spring.version}</version>
    </dependency>

    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context-support</artifactId>
        <version>${spring.version}</version>
    </dependency>

    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-orm</artifactId>
        <version>${spring.version}</version>
    </dependency>

    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-beans</artifactId>
        <version>${spring.version}</version>
    </dependency>

    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>${spring.version}</version>
    </dependency>
    
    <!-- spring end -->

    <!-- hibernate -->
    <dependency>
        <groupId>org.hibernate</groupId>
        <artifactId>hibernate-core</artifactId>
        <version>${hibernate.version}</version>
    </dependency>
    <dependency>
        <groupId>org.hibernate</groupId>
        <artifactId>hibernate-entitymanager</artifactId>
        <version>${hibernate.version}</version>
    </dependency>
    <dependency>
        <groupId>org.hibernate</groupId>
        <artifactId>hibernate-validator</artifactId>
        <version>5.2.1.Final</version>
    </dependency>
    <!-- hibernate end -->

    <!-- c3p0 -->
    <dependency>
        <groupId>c3p0</groupId>
        <artifactId>c3p0</artifactId>
        <version>${c3p0.version}</version>
    </dependency>
    <!-- c3p0 end -->

    <!-- log -->
    <dependency>
        <groupId>log4j</groupId>
        <artifactId>log4j</artifactId>
        <version>${log4j.version}</version>
    </dependency>

    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
        <version>${slf4j.version}</version>
    </dependency>

    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-log4j12</artifactId>
        <version>${slf4j.version}</version>
    </dependency>
    <!-- log end -->

    
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>${mysql.version}</version>
    </dependency>

    <dependency>
        <groupId>org.springframework.data</groupId>
        <artifactId>spring-data-jpa</artifactId>
        <version>1.9.0.RELEASE</version>
    </dependency>

    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-test</artifactId>
        <version>4.2.4.RELEASE</version>
    </dependency>
    
    <!-- el 使用spring data jpa 必须引入 -->
    <dependency>  
        <groupId>javax.el</groupId>  
        <artifactId>javax.el-api</artifactId>  
        <version>2.2.4</version>  
    </dependency>  
      
    <dependency>  
        <groupId>org.glassfish.web</groupId>  
        <artifactId>javax.el</artifactId>  
        <version>2.2.4</version>  
    </dependency> 
    <!-- el end -->
</dependencies>
```

## 整合Spring Data JPA与Spring
```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:aop="http://www.springframework.org/schema/aop"
	xmlns:context="http://www.springframework.org/schema/context"
	xmlns:jdbc="http://www.springframework.org/schema/jdbc" xmlns:tx="http://www.springframework.org/schema/tx"
	xmlns:jpa="http://www.springframework.org/schema/data/jpa" xmlns:task="http://www.springframework.org/schema/task"
	xsi:schemaLocation="
		http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
		http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd
		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
		http://www.springframework.org/schema/jdbc http://www.springframework.org/schema/jdbc/spring-jdbc.xsd
		http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx.xsd
		http://www.springframework.org/schema/data/jpa 
		http://www.springframework.org/schema/data/jpa/spring-jpa.xsd">
	
	<!-- 1.dataSource 配置数据库连接池-->
	<bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
		<property name="driverClass" value="com.mysql.jdbc.Driver" />
		<property name="jdbcUrl" value="jdbc:mysql://localhost:3306/jpa" />
		<property name="user" value="root" />
		<property name="password" value="111111" />
	</bean>
	
	<!-- 2.配置entityManagerFactory -->
	<bean id="entityManagerFactory" class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean">
		<property name="dataSource" ref="dataSource" />
		<property name="packagesToScan" value="com.test.entity" />
		<property name="persistenceProvider">
			<bean class="org.hibernate.jpa.HibernatePersistenceProvider" />
		</property>
		<!--JPA的供应商适配器-->
		<property name="jpaVendorAdapter">
			<bean class="org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter">
				<property name="generateDdl" value="false" />
				<property name="database" value="MYSQL" />
				<property name="databasePlatform" value="org.hibernate.dialect.MySQLDialect" />
				<property name="showSql" value="true" />
			</bean>
		</property>
		<property name="jpaDialect">
			<bean class="org.springframework.orm.jpa.vendor.HibernateJpaDialect" />
		</property>
	</bean>
    
	
	<!-- 3.事务管理器-->
	<!-- JPA事务管理器  -->
	<bean id="transactionManager" class="org.springframework.orm.jpa.JpaTransactionManager">
		<property name="entityManagerFactory" ref="entityManagerFactory" />
	</bean>
	
	<!-- 整合spring data jpa-->
	<jpa:repositories base-package="com.test.dao"
		transaction-manager-ref="transactionManager"
		entity-manager-factory-ref="entityManagerFactory"></jpa:repositories>
		
	<!-- 4.txAdvice-->
	<tx:advice id="txAdvice" transaction-manager="transactionManager">
		<tx:attributes>
			<tx:method name="save*" propagation="REQUIRED"/>
			<tx:method name="insert*" propagation="REQUIRED"/>
			<tx:method name="update*" propagation="REQUIRED"/>
			<tx:method name="delete*" propagation="REQUIRED"/>
			<tx:method name="get*" read-only="true"/>
			<tx:method name="find*" read-only="true"/>
			<tx:method name="*" propagation="REQUIRED"/>
		</tx:attributes>
	</tx:advice>
	
	<!-- 5.aop-->
	<aop:config>
		<aop:pointcut id="pointcut" expression="execution(* com.test.service.*.*(..))" />
		<aop:advisor advice-ref="txAdvice" pointcut-ref="pointcut" />
	</aop:config>
	
	<context:component-scan base-package="com.test"></context:component-scan>
		
	<!--组装其它 配置文件-->
	
</beans>
```

## 使用JPA注解配置映射关系

```
//声明实体类
@Entity 
//建立实体类和表的映射关系
@Table(name="cst_customer") 
public class Customer {
	//声明当前私有属性为主键
	@Id
	//配置主键的生成策略
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	//指定和表中cust_id字段的映射关系
	@Column(name="cust_id") 
	private Long custId;
	
	@Column(name="cust_name")
	private String custName;
	
	@Column(name="cust_source")
	private String custSource;
	
	@Column(name="cust_industry")
	private String custIndustry;
	
	@Column(name="cust_level")
	private String custLevel;
	
	@Column(name="cust_address")
	private String custAddress;
	
	@Column(name="cust_phone")
	private String custPhone;
	
	// getter and setter
}
```

## 编写符合Spring Data JPA规范的Dao层接口
Spring Data JPA是spring提供的一款对于数据访问层（Dao层）的框架, 使用Spring Data JPA, 只需要按照框架的规范提供dao接口, 不需要实现类就可以完成数据库的增删改查、分页查询等方法的定义, 极大的简化了我们的开发过程。
1. 创建一个Dao层接口, 并实现JpaRepository和JpaSpecificationExecutor
2. 提供相应的泛型
```
/**
 * JpaRepository<实体类类型, 主键类型>：用来完成基本CRUD操作
 * JpaSpecificationExecutor<实体类类型>：用于复杂查询（分页等查询操作）
 */
public interface CustomerDao extends JpaRepository<Customer, Long>, JpaSpecificationExecutor<Customer> {
}
```

## 完成基本CRUD操作
```
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations="classpath:applicationContext.xml")
public class CustomerDaoTest {

    @Autowired
    private CustomerDao customerDao;
    
    /**
     * 保存客户：调用save(obj)方法
     */
    @Test
    public void testSave() {
        Customer c = new Customer();
        c.setCustName("传智播客");
        customerDao.save(c);
    }
    
    /**
     * 修改客户：调用save(obj)方法
     *      对于save方法的解释：如果执行此方法是对象中存在id属性, 即为更新操作会先根据id查询, 再更新    
     *                      如果执行此方法中对象中不存在id属性, 即为保存操作
     *          
     */
    @Test
    public void testUpdate() {
        //根据id查询id为1的客户
        Customer customer = customerDao.findOne(1l);
        //修改客户名称
        customer.setCustName("传智播客顺义校区");
        //更新
        customerDao.save(customer);
    }
    
    /**
     * 根据id删除：调用delete(id)方法
     */
    @Test
    public void testDelete() {
        customerDao.delete(1l);
    }
    
    /**
     * 根据id查询：调用findOne(id)方法
     */
    @Test
    public void testFindById() {
        Customer customer = customerDao.findOne(2l);
        System.out.println(customer);
    }
}
```

# 使用JPQL的方式查询

```
public interface CustomerDao extends JpaRepository<Customer, Long>,JpaSpecificationExecutor<Customer> {    
    //@Query 使用jpql的方式查询。
    @Query(value="from Customer")
    public List<Customer> findAllCustomer();
    
    //@Query 使用jpql的方式查询。?1代表参数的占位符, 其中1对应方法中的参数索引
    @Query(value="from Customer where custName = ?1")
    public Customer findCustomer(String custName);
}
```

# 多表关系

@OneToMany: 
* 作用：建立一对多的关系映射
* 属性：
    * targetEntityClass：指定多的多方的类的字节码
    * mappedBy：指定从表实体类中引用主表对象的名称。
    * cascade：指定要使用的级联操作
    * fetch：指定是否采用延迟加载
    * orphanRemoval：是否使用孤儿删除

@ManyToOne: 
* 作用：建立多对一的关系
* 属性：
    * targetEntityClass：指定一的一方实体类字节码
    * cascade：指定要使用的级联操作
    * fetch：指定是否采用延迟加载
    * optional：关联是否可选。如果设置为false, 则必须始终存在非空关系。

@JoinColumn: 
* 作用：用于定义主键字段和外键字段的对应关系。
* 属性：
    * name：指定外键字段的名称
    * referencedColumnName：指定引用主表的主键字段名称
    * unique：是否唯一。默认值不唯一
    * nullable：是否允许为空。默认值允许。
    * insertable：是否允许插入。默认值允许。
    * updatable：是否允许更新。默认值允许。
    * columnDefinition：列的定义信息。

@ManyToMany: 
* 作用：用于映射多对多关系
* 属性：
    * cascade：配置级联操作。
    * fetch：配置是否采用延迟加载。
    * targetEntity：配置目标的实体类。映射多对多的时候不用写。

@JoinTable: 
* 作用：针对中间表的配置
* 属性：
    * nam：配置中间表的名称
    * joinColumns：中间表的外键字段关联当前实体类所对应表的主键字段			  			
    * inverseJoinColumn：中间表的外键字段关联对方表的主键字段

## 一对多关系
```
@Entity//表示当前类是一个实体类
@Table(name="cst_customer")//建立当前实体类和表之间的对应关系
public class Customer implements Serializable {
	
	@Id//表明当前私有属性是主键
	@GeneratedValue(strategy=GenerationType.IDENTITY)//指定主键的生成策略
	@Column(name="cust_id")//指定和数据库表中的cust_id列对应
	private Long custId;
	@Column(name="cust_name")//指定和数据库表中的cust_name列对应
	private String custName;
	@Column(name="cust_source")//指定和数据库表中的cust_source列对应
	private String custSource;
	@Column(name="cust_industry")//指定和数据库表中的cust_industry列对应
	private String custIndustry;
	@Column(name="cust_level")//指定和数据库表中的cust_level列对应
	private String custLevel;
	@Column(name="cust_address")//指定和数据库表中的cust_address列对应
	private String custAddress;
	@Column(name="cust_phone")//指定和数据库表中的cust_phone列对应
	private String custPhone;
	
    //配置客户和联系人的一对多关系
  	@OneToMany(targetEntity=LinkMan.class)
	@JoinColumn(name="lkm_cust_id",referencedColumnName="cust_id")
	private Set<LinkMan> linkmans = new HashSet<>();
}
```
```
@Entity
@Table(name="cst_linkman")
public class LinkMan implements Serializable {
	@Id
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	@Column(name="lkm_id")
	private Long lkmId;
	@Column(name="lkm_name")
	private String lkmName;
	@Column(name="lkm_gender")
	private String lkmGender;
	@Column(name="lkm_phone")
	private String lkmPhone;
	@Column(name="lkm_mobile")
	private String lkmMobile;
	@Column(name="lkm_email")
	private String lkmEmail;
	@Column(name="lkm_position")
	private String lkmPosition;
	@Column(name="lkm_memo")
	private String lkmMemo;

	//多对一关系映射：多个联系人对应客户
	@ManyToOne(targetEntity=Customer.class)
	@JoinColumn(name="lkm_cust_id",referencedColumnName="cust_id")
	private Customer customer;//用它的主键, 对应联系人表中的外键
}
```

## 多对多关系
```
@Entity
@Table(name="sys_user")
public class SysUser implements Serializable {
	
	@Id
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	@Column(name="user_id")
	private Long userId;
	@Column(name="user_code")
	private String userCode;
	@Column(name="user_name")
	private String userName;
	@Column(name="user_password")
	private String userPassword;
	@Column(name="user_state")
	private String userState;
	
	//多对多关系映射
	@ManyToMany(mappedBy="users")
	private Set<SysRole> roles = new HashSet<>();
}
```
```
@Entity
@Table(name="sys_role")
public class SysRole implements Serializable {
    	
    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    @Column(name="role_id")
    private Long roleId;
    @Column(name="role_name")
    private String roleName;
    @Column(name="role_memo")
    private String roleMemo;
    
    //多对多关系映射
    @ManyToMany
    @JoinTable(name="user_role_rel",//中间表的名称
        //中间表user_role_rel字段关联sys_role表的主键字段role_id
        joinColumns={@JoinColumn(name="role_id",referencedColumnName="role_id")},
        //中间表user_role_rel的字段关联sys_user表的主键user_id
        inverseJoinColumns={@JoinColumn(name="user_id",referencedColumnName="user_id")}
    )
    private Set<SysUser> users = new HashSet<>();
}
```
