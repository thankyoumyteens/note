# 解析 MANIFEST.MF 文件

```cpp
// --- src/java.base/share/native/libjli/parse_manifest.c --- //
/**
 * 解析 jar 包中的 MANIFEST.MF 文件
 *
 * @param jarfile jar 包文件名
 * @param info 存放解析结果
 * @return 0: 成功，-1: 无法打开 jar 文件，-2: 访问 MANIFEST.MF 文件异常(比如manifest文件不存在、或者 jar 包格式不对)
 */
int
JLI_ParseManifest(char *jarfile, manifest_info *info) {
    int fd;
    zentry entry;
    char *lp;
    char *name;
    char *value;
    int rc;

    // 打开 jar 包文件
    if ((fd = JLI_Open(jarfile, O_RDONLY)) == -1) {
        // 文件打开失败
        return (-1);
    }

    info->manifest_version = NULL;
    info->main_class = NULL;
    info->jre_version = NULL;
    info->jre_restrict_search = 0;
    info->splashscreen_image_file_name = NULL;

    // 在 jar 包中定位到 MANIFEST.MF 文件
    // manifest_name 的值固定是 META-INF/MANIFEST.MF
    if ((rc = find_file(fd, &entry, manifest_name)) != 0) {
        close(fd);
        // MANIFEST.MF 文件不存在
        return (-2);
    }

    // 读取 MANIFEST.MF 文件的内容
    // 例如: Manifest-Version: 1.0\r\nCreated-By: Maven JAR Plugin 3.3.0\r\nBuild-Jdk-Spec: 21......
    manifest = inflate_file(fd, &entry, NULL);
    if (manifest == NULL) {
        close(fd);
        return (-2);
    }

    lp = manifest;
    // 解析出键值对(name value pair)
    // 比如: Manifest-Version: 1.0 中的键是 Manifest-Version，值是 1.0
    while ((rc = parse_nv_pair(&lp, &name, &value)) > 0) {
        if (JLI_StrCaseCmp(name, "Manifest-Version") == 0) {
            info->manifest_version = value;
        } else if (JLI_StrCaseCmp(name, "Main-Class") == 0) {
            info->main_class = value;
        } else if (JLI_StrCaseCmp(name, "JRE-Version") == 0) {
            // manifest 里的这个 JRE 版本配置被命令行选项中的覆盖
            // 这里不再使用 manifest 中的 JRE-Version，而是把它清空/置 0
            info->jre_version = 0;
        } else if (JLI_StrCaseCmp(name, "Splashscreen-Image") == 0) {
            info->splashscreen_image_file_name = value;
        }
    }
    close(fd);
    if (rc == 0)
        return (0);
    else
        return (-2);
}
```
