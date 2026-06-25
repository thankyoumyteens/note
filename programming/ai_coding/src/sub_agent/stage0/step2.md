# 生成阶段 0 文档

```
现在执行“阶段 0：项目级上下文校准”的第 2 轮。

前提：第 1 轮只读分析已经完成，我已确认可以进入第 2 轮。

本轮目标：根据第 1 轮分析结果，生成阶段 0 文档草稿。

请注意：

* 本轮只生成文档草稿。
* 不要写入文件。
* 不要修改业务代码。
* 不要修改 pom.xml。
* 不要新增依赖。
* 不要重构。
* 不要进入需求开发阶段。
* 不要进入第 3 轮验收。
* 不要自我声明“文档已通过验收”。

请生成以下文档草稿：

1. `.spec-workflow/steering/product.md`

   * 项目目标
   * 业务边界
   * 用户对象
   * 当前不做什么
   * 未确认事项

2. `.spec-workflow/steering/tech.md`

   * 技术栈
   * 构建方式
   * 测试方式
   * API 文档现状
   * 明确不引入的技术
   * 未确认事项

3. `.spec-workflow/steering/structure.md`

   * 项目目录结构
   * 主要模块职责
   * Controller / Service / Repository / Model 的组织方式
   * 测试目录结构
   * 后续修改代码时应遵守的结构边界

4. `docs/lessons/README.md`

   * lessons 目录用途
   * 什么时候新增 lesson
   * lesson 文件命名规则
   * 每条 lesson 应包含哪些内容
   * AI 协作中需要记录的问题类型

要求：

* 所有结论必须基于第 1 轮读取到的项目事实。
* 没有证据的内容必须写成“未确认”。
* 不要把推测写成确定事实。
* 如果 README 和实际文件存在冲突，要明确记录冲突，而不是自行修正。
* 如果 openapi.yml 和 README 描述不一致，要明确记录不一致，而不是自行决定升级或修改。
* 如果 Java 版本未显式确认，要记录为“未显式确认”，不要写死。
* `.spec-workflow/` 仍视为本地工作流目录；本轮只生成草稿，不代表正式纳入仓库。

输出完成后停止，等待我进行第 3 轮人工验收。
```

这一轮才允许它写文件。

注意重点：**阶段 0 文档不是 feature spec**。
不要让它提前写你后面要加的功能。

## AI 输出示例

````
以下为第 2 轮文档草稿，仅供人工验收。本轮未写入文件，未修改代码。

  .spec-workflow/steering/product.md 草稿

  # Product Steering

  ## 项目目标

  本项目是 Spring PetClinic 示例应用的 REST 后端版本，只提供 REST API，不提供
  UI。

  证据：
  - `readme.md` 明确说明：该后端版本 “only provides a REST API” 且 “There is no
  UI”。
  - `src/main/java/org/springframework/samples/petclinic/
  PetClinicApplication.java` 是 Spring Boot 应用入口。
  - `src/main/resources/openapi.yml` 定义了 REST API 契约。

  项目用于管理兽医诊所相关资源，包括宠物主人、宠物、兽医、就诊记录、宠物类型、兽
  医专长和用户。

  证据：
  - `readme.md` API overview 列出 owners、pets、vets、visits、pet types、
  specialties、users。
  - `src/main/resources/openapi.yml` tags 包含 owners、pets、vets、visits、
  pettypes、specialties、users。
  - `src/main/java/org/springframework/samples/petclinic/model/` 下存在
  `Owner`、`Pet`、`Vet`、`Visit`、`PetType`、`Specialty`、`User`、`Role`。

  ## 业务边界

  当前已确认的业务边界：

  - Owner：管理宠物主人信息及其宠物。
    - 证据：`Owner` 实体、`OwnerRestControllerV1`、`openapi.yml` `/owners` 相关
    路径。
  - Pet：管理宠物信息、宠物类型、所属 Owner、就诊记录。
    - 证据：`Pet` 实体、`PetRestControllerV1`、`PetRestControllerV2`。
  - Visit：管理宠物就诊记录。
    - 证据：`Visit` 实体、`VisitRestControllerV1`、`openapi.yml` `/visits`。
  - Vet：管理兽医及其 specialties。
    - 证据：`Vet` 实体、`VetRestControllerV1`。
  - PetType：管理宠物类型。
    - 证据：`PetType` 实体、`PetTypeRestControllerV1`。
  - Specialty：管理兽医专长。
    - 证据：`Specialty` 实体、`SpecialtyRestControllerV1`。
  - User / Role：支持 Basic Authentication 相关用户和角色。
    - 证据：`User`、`Role` 实体，`BasicAuthenticationConfig`，`src/main/
    resources/db/h2/data.sql` 中 admin 用户和角色。

  ## 用户对象

  已确认的系统使用对象：

  - API 消费方：README 指出 Angular 前端项目 `spring-petclinic-angular` 会消费该
  REST API。
    - 证据：`readme.md`。
  - Owner 管理相关角色：`OWNER_ADMIN`。
    - 证据：`readme.md` security configuration、Controller 中
    `@PreAuthorize("hasRole(@roles.OWNER_ADMIN)")`。
  - Vet 管理相关角色：`VET_ADMIN`。
    - 证据：`readme.md` security configuration、Controller 中
    `@PreAuthorize("hasRole(@roles.VET_ADMIN)")`。
  - 用户管理相关角色：`ADMIN`。
    - 证据：`readme.md` security configuration、`UserRestControllerV1`。

  未确认：
  - 真实生产用户画像、权限矩阵是否完整覆盖业务需求，未在第 1 轮确认。
  - 是否存在除 Angular 前端、Postman/Newman、JMeter 之外的正式 API 消费方，未确
  认。

  ## 当前不做什么

  当前项目明确不包含 UI。

  证据：
  - `readme.md` 明确说明 “There is no UI”。

  当前第 0 阶段不做以下事项：

  - 不新增业务功能。
  - 不修改 OpenAPI 契约。
  - 不生成 DTO/API 接口。
  - 不修改 Controller、Service、Repository、Model。
  - 不新增依赖。
  - 不修改 `pom.xml`。
  - 不创建或修改 `.spec-workflow/` 文件。
  - 不创建或修改 `docs/` 文件。

  ## 未确认事项

  - `.spec-workflow/` 当前属于本地工作流目录，不视为仓库已经正式采纳的项目规则；
  是否纳入版本控制，未确认。
  - 当前仓库未发现 `docs/` 目录；是否创建 `docs/lessons/README.md`，需后续明确写
  入指令。
  - 当前未发现 `AGENTS.md`、`CLAUDE.md`、`WORKFLOW.md`；是否新增，未确认。
  - README 中 API 文档描述为 OAS 3.1，但 `src/main/resources/openapi.yml` 实际声
  明为 `openapi: 3.0.1`。当前以 `openapi.yml` 为事实来源，该不一致暂不修正。

  .spec-workflow/steering/tech.md 草稿

  # Technical Steering

  ## 技术栈

  已确认技术栈：

  - Spring Boot
    - 证据：`pom.xml` parent 为 `org.springframework.boot:spring-boot-starter-
    parent:4.0.6`。
  - Spring Web MVC
    - 证据：`pom.xml` 依赖 `spring-boot-starter-webmvc`。
  - Spring Boot Actuator
    - 证据：`pom.xml` 依赖 `spring-boot-starter-actuator`。
  - Spring Security
    - 证据：`pom.xml` 依赖 `spring-boot-starter-security`，`security/
    BasicAuthenticationConfig.java`，`security/DisableSecurityConfig.java`。
  - Spring Validation
    - 证据：`pom.xml` 依赖 `spring-boot-starter-validation`。
  - Spring Data JPA / JPA / JDBC
    - 证据：`pom.xml` 依赖 `spring-boot-starter-data-jpa`、`spring-boot-starter-
    jdbc`、`spring-data-jdbc-core`。
    - 证据：`repository/jdbc`、`repository/jpa`、`repository/springdatajpa`。
  - H2、HSQLDB、MySQL、PostgreSQL
    - 证据：`pom.xml` runtime dependencies，`application-h2.properties`、
    `application-hsqldb.properties`、`application-mysql.properties`、
    `application-postgres.properties`。
  - OpenAPI Generator
    - 证据：`pom.xml` `openapi-generator-maven-plugin`。
  - springdoc-openapi
    - 证据：`pom.xml` `springdoc-openapi-starter-webmvc-ui`，
    `SwaggerConfig.java`。
  - MapStruct
    - 证据：`pom.xml` `mapstruct` 和 `mapstruct-processor`，`mapper/
    *Mapper.java`。
  - JUnit / Spring Boot Test / Mockito / MockMvc
    - 证据：`pom.xml` test dependencies，`src/test/java`。
  - Newman / Postman
    - 证据：`src/test/postman/README.md`，`postman-tests.sh`。
  - JMeter
    - 证据：`src/test/jmeter/README.md`，`petclinic-jmeter-crud-benchmark.jmx`。
  - Docker / Docker Compose / Jib
    - 证据：`docker-compose.yml`，`pom.xml` `jib-maven-plugin`，`.github/
    workflows/docker-build.yml`。

  ## 构建方式

  项目使用 Maven 构建。

  证据：
  - 根目录存在 `pom.xml`、`mvnw`、`mvnw.cmd`。
  - `.mvn/wrapper/maven-wrapper.properties` 使用 Maven `3.9.9`。
  - CI 中 Pull Request 构建命令为 `./mvnw -B verify`，见 `.github/workflows/
  maven-build-pull-request.yml`。
  - master 分支 CI 使用 `./mvnw -B verify ... sonar`，见 `.github/workflows/
  maven-build-master.yml`。

  生成代码方式：

  - OpenAPI Generator 从 `src/main/resources/openapi.yml` 生成 API interface 和
  DTO。
  - 生成包：
    - `org.springframework.samples.petclinic.rest.api`
    - `org.springframework.samples.petclinic.rest.dto`
  - 生成目录：
    - `target/generated-sources/openapi/src/main/java`

  证据：
  - `pom.xml` `openapi-generator-maven-plugin`。
  - `readme.md` “Generated code”。

  MapStruct 生成 mapper 实现。

  证据：
  - `pom.xml` `maven-compiler-plugin` annotationProcessorPaths 包含 `mapstruct-
  processor`。
  - `mapper/*Mapper.java` 使用 `@Mapper`。

  ## 测试方式

  Java 测试：

  - Maven verify 是 CI 主要测试入口。
    - 证据：`.github/workflows/maven-build-pull-request.yml`。
  - Controller 测试使用 Spring Boot Test、Mockito、MockMvc standalone setup。
    - 证据：`src/test/java/org/springframework/samples/petclinic/rest/
    controller/*Tests.java`。
  - Service 测试覆盖不同 repository/database profile 组合。
    - 证据：`ClinicServiceHsqlJdbcTests`、`ClinicServiceH2JdbcTests`、
    `ClinicServiceJpaTests`、`ClinicServiceSpringDataJpaTests`、
    `UserService*Tests`。
  - 测试默认 profile 为 `hsqldb,spring-data-jpa`，并开启
  `petclinic.security.enable=true`。
    - 证据：`src/test/resources/application.properties`。

  覆盖率：

  - JaCoCo 配置 line coverage 最低 `0.85`，branch coverage 最低 `0.66`。
  - 生成代码 `rest/dto` 和 `rest/api` 被排除。
    - 证据：`pom.xml` `jacoco-maven-plugin`。

  Postman/Newman：

  - 需要先运行本地 API，再运行 `postman-tests.sh`。
    - 证据：`src/test/postman/README.md`。
  - CI 有 Newman smoke testing workflow。
    - 证据：`.github/workflows/newman-pipeline.yml`。

  JMeter：

  - 用于性能测试，需要本地 API 运行。
    - 证据：`src/test/jmeter/README.md`。

  ## API 文档现状

  已确认：

  - OpenAPI 文件位于 `src/main/resources/openapi.yml`。
  - `openapi.yml` 实际声明为 `openapi: 3.0.1`。
  - README 写 Swagger UI 地址为 `/petclinic/swagger-ui.html`。
  - README 写 API docs 地址为 `/petclinic/v3/api-docs`。
  - `SwaggerConfig.java` 配置 springdoc OpenAPI 信息。

  文档不一致：

  - README 中写 “API documentation (OAS 3.1)”。
  - `src/main/resources/openapi.yml` 实际声明 `openapi: 3.0.1`。
  - 当前记录为文档不一致问题，不自行修改 README，不升级 OpenAPI 版本。

  API First 约束：

  - 当前项目结构体现 API First 模式。
  - 如果后续涉及 API 契约变更，默认应先修改 `openapi.yml`，再生成 DTO/API，并同
  步实现 Controller / Service / 测试。
  - 本约束来自人工确认和第 1 轮项目事实；当前阶段不执行生成、修改或重构。

  ## 明确不引入的技术

  当前阶段明确不引入：

  - 不新增前端 UI 技术。
    - 证据：README 明确项目无 UI。
  - 不新增依赖。
  - 不替换 Maven 构建体系。
  - 不替换数据库迁移方案。
  - 不引入新的 API 文档工具。
  - 不引入新的测试框架。
  - 不修改现有 Spring profile 策略。

  说明：
  - 以上是阶段 0 当前约束，不表示未来永远禁止；若后续需要引入，需单独确认。

  ## 未确认事项

  - CI 使用 JDK 17。
    - 证据：`.github/workflows/*.yml` 使用 `java-version: '17'`。
  - `pom.xml` 中 Java 版本最终有效值未在第 1 轮通过 effective-pom 或构建显式确
  认。
  - 是否要求所有本地开发者使用 Maven Wrapper 而不是系统 Maven，未确认。
  - 是否将 `.spec-workflow/` 纳入版本控制，未确认。
  - 是否创建 `docs/` 目录，未确认。

  .spec-workflow/steering/structure.md 草稿

  # Structure Steering

  ## 项目目录结构

  当前已确认目录结构：

  ```text
  .
  ├── .github/workflows
  ├── .mvn/wrapper
  ├── .spec-workflow
  ├── src
  │   ├── main
  │   │   ├── java/org/springframework/samples/petclinic
  │   │   └── resources
  │   └── test
  │       ├── java
  │       ├── resources
  │       ├── postman
  │       └── jmeter
  ├── pom.xml
  ├── mvnw
  ├── mvnw.cmd
  ├── docker-compose.yml
  ├── postman-tests.sh
  └── readme.md

  证据：

  - 第 1 轮 find / rg --files 读取结果。
  - 根目录存在 .spec-workflow/，但当前仅视为本地工作流目录，不视为仓库正式规则。

  当前未发现：

  - docs/ 目录。
  - AGENTS.md。
  - CLAUDE.md。
  - WORKFLOW.md。

  ## 主要模块职责

  ### 应用入口

  - PetClinicApplication
      - Spring Boot 应用入口。
      - 证据：src/main/java/org/springframework/samples/petclinic/
        PetClinicApplication.java。

  ### REST 层

  - rest/controller/v1
      - v1 REST Controller。
      - 包含 Owner、Pet、User、Visit、Vet、PetType、Specialty、Root Controller。
      - 证据：src/main/java/org/springframework/samples/petclinic/rest/
        controller/v1/*。

  - rest/controller/v2
      - v2 REST Controller。
      - 当前包含 Owner 和 Pet 分页相关接口。
      - 证据：OwnerRestControllerV2、PetRestControllerV2。

  - rest/advice
      - 全局异常处理。
      - 证据：ExceptionControllerAdvice.java。

  - rest/validation
      - REST 相关校验。
      - 证据：PetAgeValidation.java、PetAgeValidator.java。

  ### Service 层

  - ClinicService
      - Controller 访问诊所核心业务的主要 facade。
      - 证据：ClinicService.java 注释 “Mostly used as a facade so all
        controllers have a single point of entry”。

  - ClinicServiceImpl
      - ClinicService 实现。

  - UserService
      - 用户保存业务入口。

  - UserServiceImpl
      - UserService 实现。

  ### Repository 层

  Repository 抽象接口位于：

  - repository/OwnerRepository.java
  - repository/PetRepository.java
  - repository/VisitRepository.java
  - repository/VetRepository.java
  - repository/PetTypeRepository.java
  - repository/SpecialtyRepository.java
  - repository/UserRepository.java

  Repository 实现按 profile 分组：

  - repository/jdbc
      - @Profile("jdbc")

  - repository/jpa
      - @Profile("jpa")

  - repository/springdatajpa
      - @Profile("spring-data-jpa")

  证据：

  - 各实现类和接口上的 @Profile。
  - application.properties 对 repository layer profile 的说明。

  ### Model 层

  JPA 实体位于 model 包。

  主要实体：

  - BaseEntity
  - NamedEntity
  - Person
  - Owner
  - Pet
  - PetType
  - Visit
  - Vet
  - Specialty
  - User
  - Role

  证据：

  - src/main/java/org/springframework/samples/petclinic/model/*。
  - 实体类上的 @Entity、@Table。

  主要关系：

  - Owner 一对多 Pet。
      - 证据：Owner 中 @OneToMany(mappedBy = "owner")。

  - Pet 多对一 Owner，多对一 PetType，一对多 Visit。
      - 证据：Pet 中 @ManyToOne owner、@ManyToOne type、@OneToMany visits。

  - Vet 多对多 Specialty。
      - 证据：Vet 中 @ManyToMany 和 @JoinTable(name = "vet_specialties")。

  - Visit 多对一 Pet。
      - 证据：Visit 中 @ManyToOne pet。

  - User 一对多 Role。
      - 证据：User 中 @OneToMany(mappedBy = "user")。

  ### Mapper 层

  MapStruct mapper 位于 mapper 包，用于 Entity 与 DTO 转换。

  证据：

  - OwnerMapper、PetMapper、VisitMapper、VetMapper、PetTypeMapper、
    SpecialtyMapper、UserMapper。

  - mapper 接口使用 @Mapper。

  ### 配置层

  - config/SwaggerConfig.java
      - springdoc OpenAPI 信息配置。

  - security/BasicAuthenticationConfig.java
      - petclinic.security.enable=true 时启用 Basic Auth。

  - security/DisableSecurityConfig.java
      - petclinic.security.enable=false 时允许请求。

  - security/Roles.java
      - 角色常量/Bean 支持。

  ## Controller / Service / Repository / Model 的组织方式

  当前组织方式：

  - Controller 实现 OpenAPI Generator 生成的 API interface。
      - 证据：如 OwnerRestControllerV1 implements OwnersApi、PetRestControllerV1
        implements PetsApi。

  - Controller 不直接访问 Repository，而是通过 ClinicService 或 UserService。
      - 证据：Controller 构造函数注入 ClinicService / UserService。

  - Service 使用 Repository 抽象接口。
      - 证据：ClinicServiceImpl、UserServiceImpl。

  - Repository 抽象与具体实现分离，通过 Spring profile 选择实现。
      - 证据：repository/*.java 和 repository/{jdbc,jpa,springdatajpa}。

  - Model 是 JPA 实体，与数据库表对应。
      - 证据：实体类 @Table 和 SQL schema 表。

  ## 测试目录结构

  Java 测试：

  - src/test/java/org/springframework/samples/petclinic/rest/controller
      - Controller 测试。

  - src/test/java/org/springframework/samples/petclinic/service/clinicService
      - ClinicService 测试。

  - src/test/java/org/springframework/samples/petclinic/service/userService
      - UserService 测试。

  - src/test/java/org/springframework/samples/petclinic/model
      - Model validation 测试。

  - src/test/java/org/springframework/validation
      - PetAgeValidatorTest。

  测试资源：

  - src/test/resources/application.properties
      - 测试 profile 和安全配置。

  Postman/Newman：

  - src/test/postman
      - Postman collection、environment、README。

  JMeter：

  - src/test/jmeter
      - JMeter 性能测试计划和 README。

  ## 后续修改代码时应遵守的结构边界

  后续开发应遵守以下结构边界：

  - API 契约变更应先修改 src/main/resources/openapi.yml，再生成 DTO/API，并同步
    实现 Controller / Service / 测试。
      - 依据：API First 项目结构和人工确认。

  - 不应手工修改生成目录中的 DTO/API 作为长期方案。
      - 依据：README 和 POM 显示 DTO/API 由 OpenAPI Generator 生成到 target/
        generated-sources。

  - Controller 应继续实现生成的 API interface。
      - 依据：现有 Controller 组织方式。

  - Controller 应通过 Service 访问业务能力，不应绕过 Service 直接访问
    Repository。
      - 依据：现有 Controller 构造函数注入模式。

  - Repository 实现应按现有 profile 边界组织到 jdbc、jpa、springdatajpa。
      - 依据：现有 repository 包结构和 @Profile。

  - 新增实体或表结构时，应同步考虑多数据库脚本。
      - 依据：当前存在 db/h2、db/hsqldb、db/mysql、db/postgres。

  - 新增或修改 API 行为时，应补充相应 Controller/Service 测试。
      - 依据：现有测试结构覆盖 Controller 和 Service。

  - 不应把 .spec-workflow/ 当前内容视为已正式采纳的项目规则。
      - 依据：人工确认。


  **`docs/lessons/README.md` 草稿**

  ```markdown
  # Lessons

  ## lessons 目录用途

  `docs/lessons/` 用于记录项目开发和 AI 协作过程中已经确认的经验、约束、问题复盘
  和避免重复犯错的规则。

  当前仓库未发现 `docs/` 目录。

  证据：
  - 第 1 轮读取项目结构时，`find docs` 返回不存在。

  是否创建 `docs/lessons/README.md`，需等待明确写入指令。

  ## 什么时候新增 lesson

  以下情况应新增 lesson：

  - 某个问题已经发生并被定位清楚，后续有重复发生风险。
  - 某个项目约束容易被误解，需要明确记录。
  - README、OpenAPI、代码、测试之间出现不一致，且短期内不修改源文件。
  - AI 协作过程中出现错误假设、过度推断、误改文件、漏读关键文件等问题。
  - 构建、测试、生成代码或 profile 使用方式存在容易踩坑的步骤。
  - 数据库脚本、多 profile、多实现路径之间存在同步要求。

  ## lesson 文件命名规则

  建议命名规则：

  ```text
  YYYY-MM-DD-short-topic.md

  示例：

  2026-06-25-openapi-version-mismatch.md
  2026-06-25-api-first-generation-boundary.md
  2026-06-25-profile-specific-repository-implementations.md

  命名要求：

  - 使用日期前缀，便于按时间排序。
  - 使用小写英文、数字和连字符。
  - 文件名应表达具体问题，不使用泛泛名称。
  - 如果同一天多个 lesson 主题不同，应拆分成多个文件。

  ## 每条 lesson 应包含哪些内容

  每条 lesson 建议包含：

  - 标题
  - 日期
  - 背景
  - 已确认事实
  - 证据来源
  - 问题或风险
  - 正确处理方式
  - 后续检查点
  - 是否仍有未确认事项

  建议模板：

  # 标题

  日期：YYYY-MM-DD

  ## 背景

  说明该 lesson 出现的上下文。

  ## 已确认事实

  列出已经通过文件、命令输出或人工确认验证的事实。

  ## 证据来源

  列出相关文件路径、类名、配置项或测试名称。

  ## 问题或风险

  说明如果忽略该 lesson 会导致什么问题。

  ## 正确处理方式

  说明后续遇到类似情况时应该怎么做。

  ## 未确认事项

  如果仍有无法确认的内容，明确写“未确认”。

  ## AI 协作中需要记录的问题类型

  AI 协作中应记录以下类型的问题：

  - 把未读取文件的内容当作事实。
  - 根据通用经验脑补项目规则。
  - 将本地工作流目录误认为仓库正式规范。
  - 在只读阶段修改文件。
  - 未经确认创建新目录或新文档。
  - 在 OpenAPI 与 README 冲突时自行修改或升级版本。
  - 在 Java 版本未通过 effective-pom 或构建确认时写死版本。
  - 跳过现有 Controller / Service / Repository / Model 边界直接改实现。
  - 忽略多 profile repository 实现。
  - 忽略多数据库 schema/data 脚本同步。
  - 修改 API 契约后未同步 Controller、Service、测试。
  - 修改生成代码而不是修改生成源头。
  - 未运行或未说明测试状态。


  以上为草稿输出，等待第 3 轮人工验收。
````
