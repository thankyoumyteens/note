# jinfo

jinfo(Configuration Info for Java)的作用是实时查看和调整虚拟机各项参数。

jinfo 命令格式:

```sh
jinfo [option] pid
```

## 查看 PrintGC 是否开启

```sh
$ jinfo -flag PrintGC 31836
-XX:-PrintGC
```

## 显示全部已配置的参数

```sh
jinfo -flags 31836
VM Flags:
-XX:CICompilerCount=2 -XX:ConcGCThreads=1 -XX:G1ConcRefinementThreads=1 -XX:G1EagerReclaimRemSetThreshold=8 -XX:G1HeapRegionSize=1048576 -XX:GCDrainStackTargetSize=64 -XX:InitialHeapSize=31457280 -XX:MarkStackSize=4194304 -XX:MaxHeapSize=490733568 -XX:MaxNewSize=293601280 -XX:MinHeapDeltaBytes=1048576 -XX:MinHeapSize=8388608 -XX:NonNMethodCodeHeapSize=5826188 -XX:NonProfiledCodeHeapSize=122916026 -XX:ProfiledCodeHeapSize=122916026 -XX:ReservedCodeCacheSize=251658240 -XX:+SegmentedCodeCache -XX:SoftMaxHeapSize=490733568 -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseFastUnorderedTimeStamps -XX:+UseG1GC
```

## 显示当前 JVM 的全部系统属性

```sh
jinfo -sysprops 31836
Java System Properties:
#Mon Dec 04 21:38:33 CST 2023
java.specification.version=17
sun.jnu.encoding=UTF-8
java.class.path=demo.jar
java.vm.vendor=BellSoft
sun.arch.data.model=64
catalina.useNaming=false
```
