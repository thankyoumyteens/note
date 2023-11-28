# instantclient版本问题

查看Oracle版本
```sql
SELECT * FROM "V$VERSION"  
```

下载instant-client: [http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html](http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html)

instant-client要和数据库版本一致, 下载Basic Package, 如: instantclient-basic-windows.x64-11.2.0.4.0.zip

打开navicat->工具->选项->环境->OCI环境, 路径选择刚才下载的instantclient中的oci.dll, 重启navicat

# 系统缺少必须的VC运行库

安装vc修复工具: [https://blog.csdn.net/vbcom/article/details/7245186](https://blog.csdn.net/vbcom/article/details/7245186)
