# Java Agent 导致的 protobuf 版本不兼容报错

某天，正在运行的项目突然报错了。

报错如下：

```
Caused by: java.lang.UnsupportedOperationException: This is supposed to be overridden by subclasses.
        at com.google.protobuf.GeneratedMessage.getUnknownFields(GeneratedMessage.java:262) ~[?:1.11.1]
        at com.qcloud.cmq.client.protocol.Cmq$cmq_tcp_auth.getSerializedSize(Cmq.java:34300) ~[cmq-standalone-client-1.0.0.jar!/:?]
        at com.google.protobuf.CodedOutputStream.computeMessageSizeNoTag(CodedOutputStream.java:877) ~[?:1.11.1]
        at com.google.protobuf.CodedOutputStream.computeMessageSize(CodedOutputStream.java:661) ~[?:1.11.1]
        at com.qcloud.cmq.client.protocol.Cmq$CMQProto.getSerializedSize(Cmq.java:2029) ~[cmq-standalone-client-1.0.0.jar!/:?]
        at com.google.protobuf.AbstractMessageLite.toByteArray(AbstractMessageLite.java:69) ~[?:1.11.1]
        at io.netty.handler.codec.protobuf.ProtobufEncoder.encode(ProtobufEncoder.java:67) ~[netty-codec-4.1.34.Final.jar!/:4.1.34.Final]
        at io.netty.handler.codec.protobuf.ProtobufEncoder.encode(ProtobufEncoder.java:61) ~[netty-codec-4.1.34.Final.jar!/:4.1.34.Final]
        at io.netty.handler.codec.MessageToMessageEncoder.write(MessageToMessageEncoder.java:89) ~[netty-codec-4.1.34.Final.jar!/:4.1.34.Final]
```

1. 首先去网上查了一下，似乎是 protobuf 的版本太高，而 cmq_client 依赖的是低版本的 protobuf
2. 确认一下项目中 protobuf 的版本是 2.4.1，不是高版本
3. 根据报错, 去项目的依赖 protobuf jar 包中看看 getUnknownFields 方法的具体内容：
   ```java
   public final UnknownFieldSet getUnknownFields() {
       // 这里看起来没什么问题
       return this.unknownFields;
   }
   ```
4. 那就把高版本 protobuf 的 jar 包拉下来看看 getUnknownFields 方法：
   ```java
   public UnknownFieldSet getUnknownFields() {
       // 看起来报错就是高版本的这行代码抛出的
       throw new UnsupportedOperationException("This is supposed to be overridden by subclasses.");
   }
   ```
5. 用 ASM 写个小接口读取问题类的方法体：
   ```java
   @GetMapping("/test1")
   public Response test1() {
       StringBuilder s = new StringBuilder();
       try {
           InputStream inputStream = this.getClass().getClassLoader()
                   .getResourceAsStream("com/google/protobuf/GeneratedMessage.class");
           ClassReader classReader = new ClassReader(inputStream);
           // 把 getUnknownFields 的方法体读取到 s 中
           ClassInfoVisitor classInfoVisitor = new ClassInfoVisitor(s);
           int options = ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES;
           classReader.accept(classInfoVisitor, options);
       } catch (IOException e) {
           e.printStackTrace();
       }
       return Response.success(s.toString());
   }
   ```
6. 重新部署项目，调接口后检查输出，发现实际加载的 com.google.protobuf.GeneratedMessage 是高版本的类：
   ```
   类名: com/google/protobuf/GeneratedMessage
   实现的接口: java/io/Serializable
   方法名: getUnknownFields
   方法描述符: ()Lcom/google/protobuf/UnknownFieldSet;
   方法签名: null
   方法开始:
   LDC This is supposed to be overridden by subclasses.
   opcode:183 调用方法 -> java/lang/UnsupportedOperationException.<init> (Ljava/lang/String;)V
   opcode:191 ATHROW
   方法结束
   ```
7. 在服务器上解压 fat jar，发现里面的 protobuf 包版本正确，是 2.4.1
8. 既然如此，再加一段代码，打印出问题 jar 包是从哪里加载的：
   ```java
   @GetMapping("/test111")
   public WrapperResponse test111() {
       StringBuilder s = new StringBuilder();
       try {
           InputStream inputStream = this.getClass().getClassLoader()
                   .getResourceAsStream("com/google/protobuf/GeneratedMessage.class");
           ClassReader classReader = new ClassReader(inputStream);
           ClassInfoVisitor classInfoVisitor = new ClassInfoVisitor(s);
           int options = ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES;
           classReader.accept(classInfoVisitor, options);
       } catch (IOException e) {
           e.printStackTrace();
       }
       // 获取jar包来源
       s.append("\n\n\n\n\n");
       // 方法1
       try {
           ProtectionDomain pd = GeneratedMessage.class.getProtectionDomain();
           if (pd == null) {
               s.append("GeneratedMessage -> protectionDomain is null").append("\n");
           }
           if (pd != null && pd.getCodeSource() != null) {
               s.append("GeneratedMessage -> ").append(pd.getCodeSource().getLocation()).append("\n");
           } else {
               s.append("GeneratedMessage -> codeSource is null").append("\n");
           }
       } catch (Exception e) {
           s.append("GeneratedMessage -> exception: ").append(e.getMessage()).append("\n");
           e.printStackTrace();
       }
       // 方法2
       try {
           URL resource = GeneratedMessage.class.getResource('/' + GeneratedMessage.class.getName().replace('.', '/') + ".class");
           s.append("GeneratedMessage resource -> ").append(resource).append("\n");
       } catch (Exception e) {
           s.append("GeneratedMessage resource -> exception: ").append(e.getMessage()).append("\n");
           e.printStackTrace();
       }
       return WrapperResponse.success(s.toString());
   }
   ```
9. 再部署一遍，关键输出如下：
   ```
   GeneratedMessage -> codeSource is null
   GeneratedMessage resource -> jar:file:/build/agent-monitor.9.1.1.jar!/com/google/protobuf/GeneratedMessage.class
   ```
10. 破案了，protobuf 类不是从项目的依赖中加载的，而是从 agent-monitor.9.1.1.jar 这个包里加载的
11. 最后问了一下同事，发现是一个近期的 JVM 日志监控需求加上去的 agent
