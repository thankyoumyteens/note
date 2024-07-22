# 加载代理库

在对虚拟机配置选项进行解析的阶段(`Arguments::parse` 函数)，Arguments 模块根据虚拟机选项 `-agentlib` 或 `-agentpath`，将需要加载的本地代理库逐一加入到代理库列表(`JvmtiAgentList::_list`)中。

在加载代理库阶段，虚拟机将按照代理库列表中的库名，根据操作系统的库搜索规则，利用 OS 模块查找库并加载到虚拟机进程地址空间中。例如，若按照命令 `java -agentlib：hprof` 来启动应用程序的话，将加载 JDK 中代理库 hprof，它的库文件名在 linux 中为 `libhprof.so`。

加载库操作需要在 Java 线程创建前完成，这样才能保证在 Java 线程需要调用时能够正确地找到本地库函数。

除了 JDK 中代理库和自定义代理库，虚拟机还将加载本地库，如 libc 或 Id 库。为应用程序定位本地库可以通过两种方式：

1. 将库复制到应用程序的共享库路径下
2. 按照特定操作系统平台指定规则加载，如 Solaris/Linux 平台上根据环境变量 LD_LIBRARY_PATH，而在 Windows 平台上根据环境变量 PATH 来定位本地库

在系统初始化过程中，当代理库被加载进虚拟机进程后，虚拟机将在库中查找函数符号 JVM_OnLoad 或 Agent_Onload 并调用该函数，实现代理库与虚拟机的连接。

```cpp
// --- src/hotspot/share/prims/jvmtiAgentList.cpp --- //

// Invokes Agent_OnLoad for -agentlib:.. -agentpath:  and converted -Xrun agents.
// Called very early -- before JavaThreads exist
void JvmtiAgentList::load_agents() {
  // Convert -Xrun to -agentlib: if there is no JVM_OnLoad
  convert_xrun_agents();
  JvmtiPhaseTransition transition;
  // 遍历_list变量
  // _list在Arguments::parse(args)中赋值
  Iterator it = agents();
  ::load_agents(it);
}

static void load_agents(JvmtiAgentList::Iterator& it) {
  while (it.has_next()) {
    it.next()->load();
  }
}

// --- src/hotspot/share/prims/jvmtiAgent.cpp --- //

bool JvmtiAgent::load(outputStream* st /* nullptr */) {
  if (is_xrun()) {
    return invoke_JVM_OnLoad(this);
  }
  return is_dynamic() ? invoke_Agent_OnAttach(this, st) : invoke_Agent_OnLoad(this);
}
```
