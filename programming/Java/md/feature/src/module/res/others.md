# 跨模块加载资源

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Optional;

public class Main {

    public static void main(String[] args) {
        // 获取其它模块
        Optional<Module> module2 = ModuleLayer.boot().findModule("module2");
        // 读取其它模块的资源
        module2.ifPresent((module -> {
            // 可以随时加载来自其他模块的顶级资源
            try (InputStream topLevel = module.getResourceAsStream("topLevel.txt")) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(topLevel));
                String line = reader.readLine();
                System.out.println(line);
            } catch (IOException e) {
                System.out.println(e.getMessage());
            }
            // 在默认情况下，来自其他模块的包中的资源是被封装的，所以此时返回null
            try (InputStream inPackage = module.getResourceAsStream("com/example/inPackage.txt")) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(inPackage));
                String line = reader.readLine();
                System.out.println(line);
            } catch (IOException e) {
                System.out.println(e.getMessage());
            }
            // 因为META-INF不是一个有效的包名，所以可以访问该目录中的资源
            try (InputStream inPackage = module.getResourceAsStream("META-INF/test.txt")) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(inPackage));
                String line = reader.readLine();
                System.out.println(line);
            } catch (IOException e) {
                System.out.println(e.getMessage());
            }
        }));
    }
}
```

资源封装仅适用于包中的资源(.class 文件不会被封装, 这些文件可以被另一个模块加载)。所有其他资源可以被其他模块自由使用, 但并不建议这么做。依赖来自另一个模块的资源并不是完全的模块化，最好只从同一个模块中加载资源。如果确实需要来自其他模块的资源，可以通过导出类中的方法甚至作为服务来公开资源的内容。

通过使用开放式模块(open module)或开放式包(open package)，可以向其他模块公开包中封装的资源。加载位于开放式模块或包中的资源就好像没有对资源进行封装一样。
