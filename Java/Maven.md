# 国内源
```xml
<!-- 本地仓库路径 -->
<localRepository>C:\utils\lib\maven-local</localRepository>
<mirrors>
	<!-- 阿里云仓库 -->
	<mirror>
		<id>alimaven</id>
		<mirrorOf>central</mirrorOf>
		<name>aliyun maven</name>
		<url>http://maven.aliyun.com/nexus/content/repositories/central/</url>
	</mirror>
	<!-- 中央仓库1 -->
	<mirror>
		<id>repo1</id>
		<mirrorOf>central</mirrorOf>
		<name>Human Readable Name for this Mirror.</name>
		<url>http://repo1.maven.org/maven2/</url>
	</mirror>
	<!-- 中央仓库2 -->
	<mirror>
		<id>repo2</id>
		<mirrorOf>central</mirrorOf>
		<name>Human Readable Name for this Mirror.</name>
		<url>http://repo2.maven.org/maven2/</url>
	</mirror>
</mirrors>
```

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
或者
```xml
<profile>
	<activation>
		<activeByDefault>
			true
		</activeByDefault>
	</activation>
	<repositories>
		<repository>
			<id>public</id>
			<url>http://127.0.0.1:9000/content/groups/public/</url>
			<releases><enabled>true</enabled></releases>
			<snapshots><enabled>true</enabled></snapshots>
		</repository>
	</repositories>
</profile>
```

# 把第三方 jar 包导入本地仓库
```shell
mvn install:install-file -DgroupId="com.example" -DartifactId="common_util" -Dversion="1.1.3-SNAPSHOT" -Dfile="common_util-1.1.3-SNAPSHOT.jar" -Dpackaging="jar"
```

# 设置maven项目使用Java8

方法1:配置settings.xml
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
方法2:配置pom.xml文件
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
