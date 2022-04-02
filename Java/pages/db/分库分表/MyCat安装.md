# 安装

```
wget https://github.com/MyCATApache/Mycat-Server/releases/download/Mycat-server-1675-release/Mycat-server-1.6.7.5-release-20200422133810-linux.tar.gz
tar -zxvf Mycat-server-1.6.7.5-release-20200422133810-linux.tar.gz
```

# 配置文件

conf目录下

- service.xml 主要配置mycat服务的参数，比如端口号，myact用户名和密码使用的逻辑数据库等
- rule.xml 主要配置路由策略，主要有分片的片键，拆分的策略（取模还是按区间划分等）
- schema.xml 主要配置数据库的信息，例如逻辑数据库名称，物理上真实的数据源以及表和数据源之间的对应关系和路由策略等。

## server.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mycat:server SYSTEM "server.dtd">
<mycat:server xmlns:mycat="http://io.mycat/">
    <system>
        <property name="defaultSqlParser">druidparser</property>
        <property name="mutiNodeLimitType">1</property>
        <property name="serverPort">8066</property>
        <property name="managerPort">9066</property>
    </system>
    <!-- 任意设置登陆 mycat 的用户名,密码,数据库  -->
    <user name="test">
            <property name="password">test</property>
            <!-- schema.xml 中的逻辑数据库名称 -->
            <property name="schemas">TESTDB</property>
    </user>  
    <user name="user">
        <property name="password">user</property>
        <property name="schemas">TESTDB</property>
        <property name="readOnly">true</property>
    </user>
</mycat:server>
```

## rule.xml

```xml
<!DOCTYPE mycat:rule SYSTEM "rule.dtd">
<mycat:rule xmlns:mycat="http://io.mycat/">

    <tableRule name="rule1">
        <rule>
            <columns>id</columns>
            <algorithm>mod-long</algorithm>
        </rule>
    </tableRule>

    <function name="mod-long" class="io.mycat.route.function.PartitionByMod">
        <!-- how many data nodes -->
        <property name="count">2</property>
    </function>
</mycat:rule>
```

## schema.xml

```xml
<?xml version="1.0"?>
<!DOCTYPE mycat:schema SYSTEM "schema.dtd">
<mycat:schema xmlns:mycat="http://io.mycat/">
    <!-- 设置表的存储方式.schema name="TESTDB" 与 server.xml中的 TESTDB 设置一致  -->
    <schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100">
        <table name="users" primaryKey="id"  dataNode="node_db01" />
        <table name="item" primaryKey="id" dataNode="node_db02,node_db03" rule="rule1" />
    </schema>
    <!-- 设置dataNode 对应的数据库,及 mycat 连接的地址dataHost -->
    <dataNode name="node_db01" dataHost="dataHost01" database="db01" />
    <dataNode name="node_db02" dataHost="dataHost01" database="db02" />
    <dataNode name="node_db03" dataHost="dataHost01" database="db03" />
    <!-- mycat 逻辑主机dataHost对应的物理主机.其中也设置对应的mysql登陆信息 -->
    <dataHost name="dataHost01" maxCon="1000" minCon="10" balance="0" writeType="0" dbType="mysql" dbDriver="native">
            <heartbeat>select user()</heartbeat>
            <writeHost host="server1" url="127.0.0.1:3306" user="root" password="123456"/>
    </dataHost>
</mycat:schema>
```

# 启动

```
bin/startup_nowrap.sh
```

# 连接mycat

```
mysql -utest -ptest -h127.0.0.1 -P8066 -DTESTDB
```
