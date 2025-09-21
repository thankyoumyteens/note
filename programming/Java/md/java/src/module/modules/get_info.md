# 获取模块信息

```java
import java.lang.module.ModuleDescriptor;
import java.util.Set;

public class Main {

    public static void main(String[] args) {
        // 获取当前类所在的模块
        Module module = Main.class.getModule();

        // 获取在module-info.java中定义的模块名
        String moduleName = module.getName();
        System.out.println(moduleName);

        // 获取模块中定义的所有包名
        Set<String> packages = module.getPackages();
        for (String pkg : packages) {
            System.out.println(pkg);
        }

        // 获取模块的描述符
        ModuleDescriptor moduleDescriptor = module.getDescriptor();
        System.out.println(moduleDescriptor);

        // 获取模块的依赖模块
        Set<ModuleDescriptor.Requires> requires = moduleDescriptor.requires();
        for (ModuleDescriptor.Requires require : requires) {
            System.out.println(require);
        }

        // 获取模块导出的包
        Set<ModuleDescriptor.Exports> exports = moduleDescriptor.exports();
        for (ModuleDescriptor.Exports export : exports) {
            System.out.println(export);
        }

        // 获取模块开放的包
        Set<ModuleDescriptor.Opens> opens = moduleDescriptor.opens();
        for (ModuleDescriptor.Opens open : opens) {
            System.out.println(open);
        }

        // 获取模块使用的服务
        Set<String> uses = moduleDescriptor.uses();
        for (String use : uses) {
            System.out.println(use);
        }
    }
}
```
