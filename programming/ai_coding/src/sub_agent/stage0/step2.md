# 验收文档

你后续审完文件后，用这个小修提示词：

```
Make minor revisions to the Stage 0 documentation.

Only modify the files and content I specify.

Required changes:

[List the changes you want to make here]

Requirements:

* Do not re-analyze the entire project unless the requested changes require additional evidence
* Do not modify unspecified files
* Do not modify business code
* Do not modify test code
* Do not modify pom.xml
* Continue to update steering files through spec-workflow-mcp
* When finished, output only:

  * List of modified files
  * git diff --stat
  * Whether only the specified files were modified

Stop when finished.
```
