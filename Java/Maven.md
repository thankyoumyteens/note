# 设置私服
修改maven的配置文件settings.xml
```xml
<!-- 添加私服 -->
<profiles>
	<profile> 
		<id>dev</id> 
		<repositories>
			<repository>
				<id>public</id>
				<url>http://xxx.com/content/repositories/public/</url> 
				<releases> 
					<enabled>true</enabled> 
				</releases> 
				<snapshots> 
					<enabled>true</enabled> 
				</snapshots> 
			</repository> 
		</repositories> 
	</profile>
</profiles>
<!-- 激活私服 -->
<activeProfiles>
	<activeProfile>dev</activeProfile>
</activeProfiles>
```

# 把第三方 jar 包导入本地仓库
```shell
mvn install:install-file 
-DgroupId=com.alibaba 
-DartifactId=fastjson 
-Dversion=1.1.37 
-Dfile=fastjson-1.1.37.jar 
-Dpackaging=jar
```
# 设置maven项目使用Java8
## 方法1:配置settings.xml
```xml
<profiles>
	<profile>	
	<id>jdk-1.8</id>	
	<activation>	
		<activeByDefault>true</activeByDefault>	
		<jdk>1.8</jdk>	
	</activation>	
	<properties>	
		<maven.compiler.source>1.8</maven.compiler.source>	
		<maven.compiler.target>1.8</maven.compiler.target>	
		<maven.compiler.compilerVersion>1.8</maven.compiler.compilerVersion>	
	</properties>	
	</profile>
</profiles>
```
## 方法2:配置pom.xml文件
```xml
<build>
	<plugins>
	<plugin>
		<groupId>org.apache.maven.plugins</groupId>
		<artifactId>maven-compiler-plugin</artifactId>
		<configuration>
		<source>1.8</source>
		<target>1.8</target>
		</configuration>
	</plugin>
	</plugins>
</build>
```
