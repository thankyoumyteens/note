# 引入依赖
```xml
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-context</artifactId>
  <version>5.0.2.RELEASE</version>
</dependency>
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-tx</artifactId>
  <version>5.0.2.RELEASE</version>
</dependency>
<dependency>
  <groupId>mysql</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>5.1.6</version>
</dependency>
<dependency>
  <groupId>org.aspectj</groupId>
  <artifactId>aspectjweaver</artifactId>
  <version>1.8.7</version>
</dependency>
```

# 配置文件
```xml
<!-- 配置事务管理器 -->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
  <!-- 配置数据源-->
  <property name="dataSource" ref="dataSource"/>
</bean>
<!-- 配置事务的通知-->
<tx:advice id="txAdvice" transaction-manager="transactionManager">
  <!-- 配置事务的属性 -->
  <tx:attributes>
    <tx:method name="transfer" propagation="REQUIRED" read-only="false"/>
    <tx:method name="find*" propagation="SUPPORTS" read-only="true"/>
  </tx:attributes>
</tx:advice>
<!-- 配置aop-->
<aop:config>
  <!-- 配置切入点表达式-->
  <aop:pointcut id="pt1" expression="execution(* com.test.service.impl.*.*(..))"/>
  <!--建立切入点表达式和事务通知的对应关系 -->
  <aop:advisor advice-ref="txAdvice" pointcut-ref="pt1"/>
</aop:config>
```
