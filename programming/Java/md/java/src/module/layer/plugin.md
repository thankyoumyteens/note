# 实现插件

```
.
├── api                                                 // 插件接口模块
│   └── src
│       └── main
│           └── java
│               ├── com
│               │   └── example
│               │       └── api
│               │           └── Plugin.java             // 插件接口
│               └── module-info.java
├── core                                                // 主模块
│   └── src
│       └── main
│           └── java
│               ├── com
│               │   └── example
│               │       └── core
│               │           └── Main.java               // 程序入口
│               └── module-info.java
└── plugins                                             // 插件模块
    └── greeting-plugin
        ├── greeting-plugin.iml
        └── src
            └── main
                └── java
                    ├── com
                    │   └── example
                    │       └── greeting
                    │           └── GreetingPlugin.java // 插件实现
                    └── module-info.java
```

## 插件接口模块

### 模块描述符

```java
module com.example.api {
    // 导出插件接口包，供插件模块实现
    exports com.example.api;
}
```

### Plugin.java

```java
package com.example.api;

// 所有插件必须实现的接口
public interface Plugin {
    String getName();       // 插件名称

    void execute();         // 插件执行逻辑
}
```

## 插件模块

### 模块描述符

```java
module plugin.greeting {
    requires com.example.api;
    // 插件模块提供服务
    provides com.example.api.Plugin with com.example.greeting.GreetingPlugin;
}
```

### GreetingPlugin.java

```java
package com.example.greeting;

public class GreetingPlugin implements com.example.api.Plugin {
    @Override
    public String getName() {
        return "greeting";
    }

    @Override
    public void execute() {
        System.out.println("from greeting plugin");
    }
}
```

## 主模块

### 模块描述符

```java
module com.example.core {
    requires com.example.api;
    // 使用插件服务
    uses com.example.api.Plugin;
}
```

### Main.java

```java
package com.example.core;

import com.example.api.Plugin;

import java.lang.module.Configuration;
import java.lang.module.ModuleDescriptor;
import java.lang.module.ModuleFinder;
import java.lang.module.ModuleReference;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public class Main {

    /**
     * 插件模块信息类
     * 包含模块名和模块路径
     */
    public static class ModuleInfo {
        public final String name; // 模块名
        public final Path path; // 模块的绝对路径

        public ModuleInfo(String name, Path path) {
            this.name = name;
            this.path = path;
        }
    }

    /**
     * 查找插件模块
     *
     * @param pluginDir 插件目录
     * @return 模块名和模块路径的集合
     */
    public static Set<ModuleInfo> findPlugins(Path pluginDir) {
        // 找出pluginDir下的所有模块
        ModuleFinder pluginFinder = ModuleFinder.of(pluginDir);
        Set<ModuleReference> all = pluginFinder.findAll();

        Set<ModuleInfo> pluginSet = new HashSet<>();
        for (ModuleReference moduleReference : all) {
            // 获取模块描述符
            ModuleDescriptor descriptor = moduleReference.descriptor();
            // 获取模块名
            String moduleName = descriptor.name();

            // 在这个例子中, 规定插件模块名必须以"plugin"开头
            if (moduleName.startsWith("plugin")) {
                // 发现插件模块，添加到插件集合
                moduleReference.location().ifPresent(uri -> {
                    ModuleInfo moduleInfo = new ModuleInfo(moduleName, Paths.get(uri.getPath()));
                    pluginSet.add(moduleInfo);
                });
            }
        }
        // 返回插件模块信息集合
        return pluginSet;
    }

    /**
     * 创建插件层
     * 每个插件模块创建一个插件层, 并添加到插件层集合中
     *
     * @param pluginSet   插件模块信息集合
     * @param parentLayer 父层
     * @return 插件层集合
     * @throws MalformedURLException 如果模块路径转换为URL失败
     */
    public static Set<ModuleLayer> createPluginLayers(Set<ModuleInfo> pluginSet, ModuleLayer parentLayer) throws MalformedURLException {
        // 为每个插件模块创建一个插件层
        Set<ModuleLayer> pluginLayers = new HashSet<>();
        for (ModuleInfo moduleInfo : pluginSet) {
            // 创建插件模块的查找器
            ModuleFinder pluginFinder = ModuleFinder.of(moduleInfo.path);
            // 解析插件模块依赖
            Configuration parentConfig = parentLayer.configuration();
            Configuration pluginConfig = parentConfig.resolve(
                    pluginFinder,
                    ModuleFinder.of(), // 依赖从父层获取
                    Set.of(moduleInfo.name) // 插件模块名集合
            );

            // 为插件层创建类加载器
            ClassLoader parentClassLoader = ClassLoader.getSystemClassLoader();
            URL[] pluginUrls = {moduleInfo.path.toUri().toURL()};
            URLClassLoader pluginClassLoader = new URLClassLoader(
                    pluginUrls,
                    parentClassLoader
            );

            // 创建插件层
            ModuleLayer pluginLayer = parentLayer.defineModulesWithOneLoader(
                    pluginConfig,
                    pluginClassLoader
            );
            // 添加插件层到集合
            pluginLayers.add(pluginLayer);
        }
        // 返回插件层集合
        return pluginLayers;
    }

    /**
     * 加载插件
     * 从每个插件层中加载实现Plugin接口的服务类对象
     *
     * @param pluginLayers 插件层集合
     * @return 插件实例列表
     */
    public static List<Plugin> loadPlugins(Set<ModuleLayer> pluginLayers) {
        // 通过ServiceLoader发现实现类
        List<Plugin> plugins = new ArrayList<>();
        // 通过ServiceLoader扫描插件层中实现Plugin接口的服务
        for (ModuleLayer pluginLayer : pluginLayers) {
            ServiceLoader<Plugin> serviceLoader = ServiceLoader.load(
                    pluginLayer,       // 插件层
                    Plugin.class       // 插件接口
            );
            for (Plugin plugin : serviceLoader) {
                plugins.add(plugin);
            }
        }
        return plugins;
    }

    public static void main(String[] args) throws Exception {
        // 插件目录（存放所有插件模块）
        Path pluginDir = Paths.get("/tmp/plugins");
        System.out.println("插件目录：" + pluginDir.toAbsolutePath());

        // 查找插件模块
        Set<ModuleInfo> pluginSet = findPlugins(pluginDir);
        // 获取父层
        ModuleLayer parentLayer = ModuleLayer.boot();
        // 创建插件层
        Set<ModuleLayer> pluginLayers = createPluginLayers(pluginSet, parentLayer);
        // 加载插件
        List<Plugin> plugins = loadPlugins(pluginLayers);

        // 执行插件
        System.out.println("发现 " + plugins.size() + " 个插件：");
        for (Plugin plugin : plugins) {
            System.out.println("执行插件：" + plugin.getName());
            plugin.execute();
        }
    }
}
```
