# 加载

加载的是从 Class 文件字节流中提取类型信息。

- ClassFileParser：类解析器, 用来解析 class 文件。它利用 ClassFileStream 读取 class 文件的输入流, 作为 ClassFileParser 的输入
- Verifier：验证器, 用来验证 class 文件中字节码。它将为每个类创建一个 ClassVerifier 实例来验证
- ClassLoader：类加载器
- SystemDictionary：系统字典, 用来记录已加载的所有类
- SymboleTable：符号表。用做快速查找字符串, 例如将与 JDK 基本类的名字相映射的字符串、表示函数签名类型的字符串以及 VM 内部各种用途的字符串等
