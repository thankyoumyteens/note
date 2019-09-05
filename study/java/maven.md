# 将项目发布到私服

第一步：需要在客户端即部署 ssm_dao 工程的电脑上配置 maven环境，并修改 settings.xml
文件，配置连接私服的用户和密码 。
此用户名和密码用于私服校验，因为私服需要知道上传的账号和密码是否和私服中的账号和
密码一致

```
<server>
    <id>releases</id>
    <username>admin</username>
    <password>admin123</password>
</server>
<server>
    <id>snapshots</id>
    <username>admin</username>
    <password>admin123</password>
</server>
```

第二步： 配置项目 pom.xml 
配置私服仓库的地址，本公司的自己的 jar 包会上传到私服的宿主仓库，根据工程的版本号
决定上传到哪个宿主仓库，如果版本为 release 则上传到私服的 release 仓库，如果版本为
snapshot 则上传到私服的 snapshot 仓库

注意：pom.xml 这里<id> 和 settings.xml 配置 <id> 对应！

```
<distributionManagement>
    <repository>
        <id>releases</id>
        <url>http://localhost:8081/nexus/content/repositories/releases/</url>
    </repository>
    <snapshotRepository>
        <id>snapshots</id>
        <url>http://localhost:8081/nexus/content/repositories/snapshots/</url>
    </snapshotRepository>
</distributionManagement>
```

第三步： 执行mvn deploy命令

# 从私服下载 jar 包

在maven的 setting.xml 中配置私服的仓库，由于 setting.xml 中没有 repositories 的配置
标签需要使用 profile 定义仓库。
```
<profile> 
    <!--profile 的 id-->
    <id>dev</id> 
    <repositories> 
        <repository> 
            <!--仓库 id，repositories 可以配置多个仓库，保证 id 不重复-->
            <id>nexus</id> 
            <!--仓库地址，即 nexus 仓库组的地址-->
            <url>http://localhost:8081/nexus/content/groups/public/</url> 
            <!--是否下载 releases 构件-->
            <releases> 
                <enabled>true</enabled> 
            </releases> 
            <!--是否下载 snapshots 构件-->
            <snapshots> 
                <enabled>true</enabled> 
            </snapshots> 
        </repository> 
    </repositories> 
    <pluginRepositories> 
        <!-- 插件仓库，maven 的运行依赖插件，也需要从私服下载插件 -->
        <pluginRepository> 
        <!-- 插件仓库的 id 不允许重复，如果重复后边配置会覆盖前边 -->
            <id>public</id> 
            <name>Public Repositories</name> 
            <url>http://localhost:8081/nexus/content/groups/public/</url> 
        </pluginRepository> 
    </pluginRepositories> 
</profile> 
```
使用 profile 定义仓库需要激活才可生效。
```
<activeProfiles>
    <activeProfile>dev</activeProfile>
</activeProfiles>
```

# 把第三方 jar 包放入本地仓库或私服

## 导入本地库

`mvn install:install-file 
-DgroupId=com.alibaba 
-DartifactId=fastjson 
-Dversion=1.1.37 
-Dfile= fastjson-1.1.37.jar 
-Dpackaging=jar`

## 导入私服

需要在 maven 软件的核心配置文件 settings.xml 中配置第三方仓库的 server 信息
```
<server> 
    <id>thirdparty</id> 
    <username>admin</username>
    <password>admin123</password> 
</server>
```
才能执行一下命令
`mvn deploy:deploy-file
-DgroupId=com.alibaba 
-DartifactId=fastjson 
-Dversion=1.1.37 
-Dpackaging=jar 
-Dfile=fastjson-1.1.37.jar 
-Durl=http://localhost:8081/nexus/content/repositories/thirdparty/ 
-DrepositoryId=thirdparty`
