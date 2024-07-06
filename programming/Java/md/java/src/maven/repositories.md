# 设置私服

修改 maven 的配置文件 settings.xml

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
