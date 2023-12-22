# ParNew

ParNew 是 Serial 的多线程并行版本, 它使用多条线程进行 GC, GC 时也需要暂停用户线程, 除此之外其余都与 Serial 完全一致。

除了 Serial 外, 目前只有它能与 CMS 配合工作。

从 JDK 9 开始, ParNew + CMS 的组合就不再是官方推荐的服务端模式下的垃圾回收器解决方案了。
