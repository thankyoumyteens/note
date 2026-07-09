# 创建文档

## 项目和 AI 会话在同一个路径下

```
Phase 0: Project-level context calibration.

Important Phase 0 permission rule:

* During Phase 0, the project’s source code, tests, resources, build files, and existing project files are read-only unless explicitly listed as allowed output files.
* Phase 0 may read and analyze the project.
* Phase 0 may create or update only the context files listed below.
* Do not modify business code, test code, resources, build configuration, wrapper scripts, or existing README files during Phase 0.
* After Phase 0 is completed, later phases may modify the project only when explicitly authorized.

Before doing the task:

1. Run pwd to confirm the current working directory.
2. Keep allowed documentation writes separate from forbidden project modifications.

Must create or update these files:

* .spec-workflow/steering/product.md
* .spec-workflow/steering/tech.md
* .spec-workflow/steering/structure.md
* AGENTS.md
* CLAUDE.md
* docs/lessons/README.md
* docs/decisions/README.md

Requirements:

1. First read project facts from the current working directory, including:
    * README.md
    * pom.xml
    * src/main/java
    * src/main/resources
    * src/test/java
    * OpenAPI / Swagger configuration
    * database initialization scripts
    * test configuration
2. For the three steering files, prefer MCP-exposed steering create/update tools. If the current session does not expose those tools, create or update the steering markdown files according to steering_guide:
    * product
    * tech
    * structure
3. AGENTS.md, CLAUDE.md, docs/lessons/README.md, and docs/decisions/README.md may be created or updated directly.
4. AGENTS.md must state:
    * read steering documents first
    * do only one task at a time
    * do not expand requirements
    * do not add dependencies unless explicitly allowed
    * do not modify unauthorized files
    * do not run git add
    * do not run git commit
    * after completion, report modified files, test result, and git diff --stat
    Do not write Phase 0-only rules into AGENTS.md.
5. Forbidden modifications during Phase 0:
    * src/main/java
    * src/test/java
    * src/main/resources
    * pom.xml
    * README.md
    * mvnw
    * mvnw.cmd
    * any business code
    * any test code
    * any build configuration
    * any project file not explicitly listed as an allowed output file
6. Documentation content must be based only on observed project facts.
    * If information is uncertain, write Unconfirmed.
    * Do not invent facts.
    * Do not design future features in advance.
7. File content requirements:
    product.md must include:
    * project goal
    * business domain
    * core entities
    * current functional boundaries
    * explicit non-goals
    tech.md must include:
    * Java / Spring Boot / Maven versions
    * database
    * test framework
    * API documentation approach
    * run method
    * technologies that must not be introduced casually
    structure.md must include:
    * directory structure
    * main packages
    * Controller / Service / Repository / Model / DTO organization
    * test directory structure
    * where future code should be added
    CLAUDE.md must include:
    * AGENTS.md is the source of truth
    * Claude should follow AGENTS.md first
    docs/lessons/README.md must include:
    * this directory records AI mistakes, tool pitfalls, and process lessons
    * do not invent existing lessons
    docs/decisions/README.md must include:
    * this directory records long-term architecture decisions and technical tradeoffs
    * do not invent existing decisions
8. Verification:
    * Run git diff --stat.
    * Verify that only the allowed context files were created or modified.
    * Do not run tests unless needed, because this task is documentation-only.
9. Final output must contain only:
    * current working directory
    * list of created/modified files
    * whether only allowed files were modified
    * git diff --stat
    * unconfirmed issues

Do not output a long explanation.

Stop after the final report.
```

## 项目和 AI 会话不在同一个路径下

```
Phase 0: Project-level context calibration.

Before starting, set the target project root:

TARGET_PROJECT_ROOT=/Users/aaa/IdeaProjects/project-a

The AI workspace and the target project are in different directories.

Path rules:

Target project root:
TARGET_PROJECT_ROOT
Context output root:
the current working directory of this AI session

Important Phase 0 permission rule:

* During Phase 0, TARGET_PROJECT_ROOT is read-only.
* Phase 0 may only read and analyze the target project.
* Phase 0 must create or update context files only under the current working directory.
* Do not create or modify any files inside TARGET_PROJECT_ROOT during Phase 0.
* After Phase 0 is completed, later phases may modify the target project only when explicitly authorized.

Before doing the task:

1. Run pwd to confirm the current working directory.
2. Resolve and confirm TARGET_PROJECT_ROOT.
3. Keep the two roots separate throughout the task.

Must create or update these files under the current working directory:

* .spec-workflow/steering/product.md
* .spec-workflow/steering/tech.md
* .spec-workflow/steering/structure.md
* AGENTS.md
* CLAUDE.md
* docs/lessons/README.md
* docs/decisions/README.md

Requirements:

1. First read project facts from TARGET_PROJECT_ROOT, including:
    * README.md
    * pom.xml
    * src/main/java
    * src/main/resources
    * src/test/java
    * OpenAPI / Swagger configuration
    * database initialization scripts
    * test configuration
2. For the three steering files, prefer MCP-exposed steering create/update tools. If the current session does not expose those tools, create or update the steering markdown files according to steering_guide:
    * product
    * tech
    * structure
3. AGENTS.md, CLAUDE.md, docs/lessons/README.md, and docs/decisions/README.md may be created or updated directly.
4. AGENTS.md must explicitly state:
    * the resolved absolute path of TARGET_PROJECT_ROOT
    * the current working directory is the AI workspace/context output root
    * read steering documents first
    * do only one task at a time
    * do not expand requirements
    * do not add dependencies unless explicitly allowed
    * do not modify unauthorized files
    * do not run git add
    * do not run git commit
    * after completion, report modified files, test result, and git diff --stat
    Do not write Phase 0-only rules into AGENTS.md.
5. Forbidden modifications during Phase 0:
    * anything under TARGET_PROJECT_ROOT
    * src/main/java
    * src/test/java
    * src/main/resources
    * pom.xml
    * README.md
    * mvnw
    * mvnw.cmd
    * any business code
    * any test code
    * any build configuration
6. Documentation content must be based only on observed project facts.
    * If information is uncertain, write Unconfirmed.
    * Do not invent facts.
    * Do not design future features in advance.
7. File content requirements:
    product.md must include:
    * project goal
    * business domain
    * core entities
    * current functional boundaries
    * explicit non-goals
    tech.md must include:
    * Java / Spring Boot / Maven versions
    * database
    * test framework
    * API documentation approach
    * run method
    * technologies that must not be introduced casually
    structure.md must include:
    * directory structure
    * main packages
    * Controller / Service / Repository / Model / DTO organization
    * test directory structure
    * where future code should be added
    CLAUDE.md must include:
    * AGENTS.md is the source of truth
    * Claude should follow AGENTS.md first
    docs/lessons/README.md must include:
    * this directory records AI mistakes, tool pitfalls, and process lessons
    * do not invent existing lessons
    docs/decisions/README.md must include:
    * this directory records long-term architecture decisions and technical tradeoffs
    * do not invent existing decisions
8. Verification:
    * Run git diff --stat in the current working directory.
    * Verify that TARGET_PROJECT_ROOT was not modified during Phase 0.
    * Do not run tests unless needed, because this task is documentation-only.
9. Final output must contain only:
    * resolved TARGET_PROJECT_ROOT
    * list of created/modified files
    * whether only allowed files were modified
    * whether TARGET_PROJECT_ROOT remained unmodified during Phase 0
    * git diff --stat
    * unconfirmed issues

Do not output a long explanation.

Stop after the final report.
```
