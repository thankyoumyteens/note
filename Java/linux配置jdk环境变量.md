# linux配置jdk环境变量

```sh
mv jdk-8u171-linux-x64.tar.gz /usr/local/java/jdk-8u171-linux-x64.tar.gz
tar -zxvf jdk-8u171-linux-x64.tar.gz
vi /etc/profile
```
在文件末尾加入:
```
export JAVA_HOME=/usr/local/java/jdk1.8.0_171
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar 
```
使profile生效
```
source /etc/profile
java -version
```
