# 只读项目，不允许改文件

先把下面这段直接丢给 Claude Code / Codex / Cursor。

```
现在执行“阶段 0：项目级上下文校准”的第 1 轮。

本轮目标：只读取项目，理解项目现状，不生成正式文档，不修改任何文件。

重要说明：

* `.spec-workflow/` 属于本地工作流目录。
* 本轮可以识别它是否存在，但不要假设它已经是仓库正式内容。
* 不要修改 `.spec-workflow/`。
* 不要把 `.spec-workflow/` 中的内容当作已经被项目正式采纳的规则，除非文件内容本身明确说明。
* 是否将 `.spec-workflow/` 纳入版本控制，后续由我确认。

请读取并分析以下内容：

1. 项目根目录结构
2. README / readme 文件
3. pom.xml / Maven Wrapper / 构建相关文件
4. src/main 下的主要代码结构
5. src/test 下的主要测试结构
6. API 文档相关文件，例如 openapi.yml
7. 已存在的 docs 目录
8. 已存在的 AGENTS.md / CLAUDE.md / WORKFLOW.md，如果存在

本轮只输出分析结果，包括：

1. 项目目标初步判断
2. 技术栈初步判断
3. 目录结构初步判断
4. 测试方式初步判断
5. API / 文档现状初步判断
6. 明确已确认的信息
7. 不确定或需要人工确认的问题

严格限制：

* 不要修改任何文件。
* 不要新增任何文件。
* 不要运行重构。
* 不要新增依赖。
* 不要进入第 2 轮。
* 不要生成阶段 0 文档草稿。
* 如果信息无法确认，必须标记为“未确认”，不要脑补。
* 输出第 1 轮分析结果后停止，等待我确认。
```

这一轮的重点是看 AI 有没有真正读项目。

你要重点检查它的输出里有没有这种证据：

- pom.xml 中声明了哪些依赖
- Controller 在哪个 package
- Repository 是 JPA 还是别的方式
- 数据库脚本在哪里
- 测试类在哪里
- API 前缀是什么

如果它只说“这是一个 Spring Boot REST 项目，采用分层架构”，但没有证据路径，就不合格。

## AI 输出示例

```
第 1 轮分析已完成。仅读取文件，未修改文件，未运行测试或构建。

  1. 项目目标初步判断

  这是 Spring PetClinic 的 REST 后端版本，只提供 REST API，没有 UI。README 明确
  写明 “only provides a REST API. There is no UI”，并说明 Angular 前端在另一个仓
  库消费该 API。证据：readme.md。

  项目业务目标是管理兽医诊所中的 owners、pets、vets、visits、pet types、
  specialties、users。证据：readme.md API overview、src/main/resources/
  openapi.yml tags/paths、src/main/java/org/springframework/samples/petclinic/
  model/*。

  项目采用 API First 方式，OpenAPI 规格文件用于生成 DTO 和 API interface，
  Controller 实现这些生成接口。证据：readme.md “API First Approach”、pom.xml
  openapi-generator-maven-plugin、Controller 如 OwnerRestControllerV1 implements
  OwnersApi。

  2. 技术栈初步判断

  已确认：

  - Spring Boot：pom.xml parent 为 org.springframework.boot:spring-boot-starter-
    parent:4.0.6。

  - Maven：存在 pom.xml、mvnw、mvnw.cmd、.mvn/wrapper/maven-wrapper.properties；
    Wrapper 使用 Maven 3.9.9。

  - Web：spring-boot-starter-webmvc，入口类 PetClinicApplication 使用
    @SpringBootApplication。

  - 数据访问：JPA、JDBC、Spring Data JPA 三种 repository profile。证据：
    application.properties profile 说明，repository/jdbc、repository/jpa、
    repository/springdatajpa。

  - 数据库：H2、HSQLDB、MySQL、PostgreSQL。证据：pom.xml runtime dependencies、
    application-*.properties、src/main/resources/db/*。

  - API 文档：springdoc-openapi + OpenAPI Generator。证据：pom.xml springdoc-
    openapi-starter-webmvc-ui、openapi-generator-maven-plugin、SwaggerConfig。

  - DTO/接口生成：OpenAPI Generator 生成
    org.springframework.samples.petclinic.rest.dto 和
    org.springframework.samples.petclinic.rest.api 到 target/generated-sources。
    证据：pom.xml、readme.md。

  - Entity/DTO 映射：MapStruct。证据：pom.xml mapstruct、src/main/java/.../
    mapper/*Mapper.java。

  - 安全：Spring Security，可通过 petclinic.security.enable 开关启用 Basic
    Auth。证据：BasicAuthenticationConfig、DisableSecurityConfig、
    application.properties。

  - 测试：JUnit/Spring Boot Test/Mockito/MockMvc/Postman Newman/JMeter。证据：
    pom.xml test dependencies、src/test/java、src/test/postman/README.md、src/
    test/jmeter/README.md。

  3. 目录结构初步判断

  根目录关键结构：

  - src/main/java/org/springframework/samples/petclinic：主代码。
  - src/main/resources：应用配置、OpenAPI、数据库初始化脚本、messages、logback。
  - src/test/java：Java 测试。
  - src/test/resources：测试配置。
  - src/test/postman：Postman/Newman 非回归测试。
  - src/test/jmeter：JMeter 性能测试。
  - .github/workflows：CI、Docker、Newman workflow。
  - .spec-workflow/：存在，但本轮只确认存在；未读取其内容，也不将其视为正式项目
    规则。

  - docs/：未发现，find docs 返回不存在。
  - AGENTS.md / CLAUDE.md / WORKFLOW.md：根目录及 maxdepth 2 搜索未发现。

  主代码分层：

  - rest/controller/v1、rest/controller/v2：REST Controller。
  - service：ClinicService、UserService 及实现。
  - repository：抽象 repository 接口。
  - repository/jdbc、repository/jpa、repository/springdatajpa：不同 profile 的实
    现。

  - model：JPA 实体。
  - mapper：MapStruct mapper。
  - security：安全配置。
  - config：Swagger/OpenAPI 配置。
  - rest/advice、rest/validation：异常处理与校验。

  4. 测试方式初步判断

  Java 测试：

  - CI 使用 ./mvnw -B verify。证据：.github/workflows/maven-build-pull-
    request.yml。

  - 主干 CI 使用 ./mvnw -B verify ... sonar。证据：.github/workflows/maven-
    build-master.yml。

  - Controller 测试使用 @SpringBootTest、
    @ContextConfiguration(ApplicationTestConfig.class)、
    MockMvcBuilders.standaloneSetup(...)、@MockitoBean。证据：src/test/java/org/
    springframework/samples/petclinic/rest/controller/*Tests.java。

  - Service 测试覆盖不同 profile：hsqldb/jdbc、h2/jdbc、jpa/hsqldb、spring-data-
    jpa/hsqldb。证据：ClinicService*Tests、UserService*Tests。

  - 测试配置默认 spring.profiles.active=hsqldb,spring-data-jpa，并设置
    petclinic.security.enable=true。证据：src/test/resources/
    application.properties。

  - JaCoCo 在 Maven 构建中配置覆盖率检查：line 0.85、branch 0.66，排除生成的
    rest/dto 和 rest/api。证据：pom.xml jacoco-maven-plugin。

  非 Java 测试：

  - Postman/Newman 测试需要先运行应用，然后执行 postman-tests.sh，通过 npx
    newman 运行集合。证据：src/test/postman/README.md、postman-tests.sh。

  - JMeter 性能测试需要本地 API 运行，使用 jmeter -n -t src/test/jmeter/
    petclinic-jmeter-crud-benchmark.jmx ...。证据：src/test/jmeter/README.md。

  5. API / 文档现状初步判断

  已存在 src/main/resources/openapi.yml，声明 openapi: 3.0.1，包含 paths：/
  owners、/v2/owners、/pets、/v2/pets、/vets、/visits、/pettypes、/
  specialties、/users、/oops。证据：openapi.yml。

  README 写 Swagger UI 地址为
  http://localhost:9966/petclinic/swagger-ui.html，API docs 为
  /petclinic/v3/api-docs。证据：readme.md。

  OpenAPI Generator 配置：

  - inputSpec：src/main/resources/openapi.yml
  - generator：spring
  - library：spring-boot
  - interfaceOnly=true
  - useTags=true
  - apiPackage：org.springframework.samples.petclinic.rest.api
  - modelPackage：org.springframework.samples.petclinic.rest.dto

  证据：pom.xml。

  注意：README 写 “API documentation (OAS 3.1)”，但 openapi.yml 实际声明
  openapi: 3.0.1。这是已发现的不一致，需确认。

  6. 明确已确认的信息

  - 默认运行端口是 9966，context path 是 /petclinic/。证据：src/main/resources/
    application.properties。

  - 默认 profile 是 h2,spring-data-jpa。证据：src/main/resources/
    application.properties。

  - 默认安全关闭：petclinic.security.enable=false。证据：src/main/resources/
    application.properties。

  - 测试资源默认 profile 是 hsqldb,spring-data-jpa，安全开启。证据：src/test/
    resources/application.properties。

  - 核心数据库表包括 vets、specialties、vet_specialties、types、owners、pets、
    visits、users、roles。证据：src/main/resources/db/h2/schema.sql。

  - H2 初始数据包含默认 admin 用户及 ROLE_OWNER_ADMIN、ROLE_VET_ADMIN、
    ROLE_ADMIN。证据：src/main/resources/db/h2/data.sql。

  - Controller 以 /api 为基础路径，v1/v2 并存。证据：OwnerRestControllerV1、
    PetRestControllerV1、OwnerRestControllerV2、PetRestControllerV2。

  - 主要业务入口是 ClinicService 和 UserService。证据：src/main/java/.../
    service/ClinicService.java、UserService.java。

  - Repository 抽象与实现分离，具体实现由 Spring profile 选择。证据：repository/
    *.java、repository/jdbc/* @Profile("jdbc")、repository/jpa/*
    @Profile("jpa")、repository/springdatajpa/* @Profile("spring-data-jpa")。

  7. 不确定或需要人工确认的问题

  - .spec-workflow/ 是否纳入版本控制、是否作为正式开发规则：未确认。
  - README 标注 OAS 3.1，但 openapi.yml 是 3.0.1，实际应以哪个为准：未确认。
  - 是否要求后续开发始终 API First，即先改 openapi.yml 再生成 DTO/API：README 和
    POM 支持该模式，但团队执行规则未确认。

  - Java 版本约束的来源：CI 明确使用 JDK 17；pom.xml enforcer 使用
    ${java.version}，但当前 POM 源码未直接定义该属性，具体有效值未确认。

  - docs/ 目录当前不存在，是否后续需要创建正式文档目录：未确认。
  - AGENTS.md / CLAUDE.md / WORKFLOW.md 当前未发现，是否后续需要新增或引入：未确
    认。

  本轮停止，等待你确认是否进入下一轮。
```

## 人工确认

回复需要人工确认的问题：

```
这是对第 1 轮“未确认或需要人工确认的问题”的人工确认结果。

注意：

* 以下内容只作为第 1 轮分析结果的补充上下文。
* 现在不要生成阶段 0 文档草稿。
* 现在不要创建或修改任何文件。
* 请只确认你已收到这些人工决定，然后停止。

人工确认结果如下：

1. `.spec-workflow/` 的性质

`.spec-workflow/` 当前属于本地工作流目录，不视为仓库已经正式采纳的项目规则。

本阶段可以知道它存在，但不要假设它已经纳入版本控制，也不要把其中内容当成项目正式规范。是否纳入版本控制，后续单独确认。

2. OpenAPI 版本不一致

当前以 `src/main/resources/openapi.yml` 中的实际声明为准，即 `openapi: 3.0.1`。

README 中的 “OAS 3.1” 记录为文档不一致问题。当前不修改 README，也不升级 OpenAPI 版本。

3. API First 执行规则

确认当前项目结构体现了 API First 模式：`openapi.yml` 用于生成 DTO 和 API interface，Controller 实现生成接口。

后续如果涉及 API 契约变更，默认应先修改 `openapi.yml`，再生成 DTO/API，并同步实现 Controller / Service / 测试。

但这只是后续开发约束，本轮不要执行任何生成、修改或重构。

4. Java 版本约束

当前只确认 CI 使用 JDK 17。

`pom.xml` 中 Java 版本的最终有效值尚未通过 effective-pom 或构建确认，因此阶段 0 文档中应记录为：

“CI 使用 JDK 17；POM 中 Java 版本最终有效值未在第 1 轮显式确认。”

不要在文档中脑补为 Java 21、Java 25 或其他版本。

5. `docs/` 目录

当前仓库没有发现 `docs/` 目录。

后续阶段 0 文档如果需要 `docs/lessons/README.md`，应在我明确发送第 2 轮或写入指令后再处理。

现在不要创建 `docs/` 目录。

6. `AGENTS.md` / `CLAUDE.md` / `WORKFLOW.md`

当前未发现这些文件。

现在不要新增这些文件。是否需要新增，后续单独确认。

请只回复：已收到以上人工确认结果，并等待第 2 轮 Prompt。

不要生成草稿。
不要修改文件。
不要进入下一轮。
```
