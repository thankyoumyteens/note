# 交叉编译

```sh
# 编译成linux可执行程序
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build
# 编译成Windows可执行程序
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build
# 编译成MacOS可执行程序
CGO_ENABLED=0 GOOS=darwin GOARCH=arm64 go build
```

- CGO_ENABLED: 用于控制 Go 语言编译过程中是否启用 cgo(C 代码生成工具)。cgo 允许 Go 代码中嵌入 C 代码, 从而实现 Go 和 C 代码之间的交互
- GOOS: 目标平台
  - darwin: mac
  - linux: linux
  - windows: windows
- GOARCH ：目标平台的体系架构
  - 386: 32 位 Intel CPU
  - amd64: 64 位 Intel/AMD CPU
  - arm: ARM
  - arm64 或 aarch64: 64 位 ARM
  - riscv64: 64 位 RISC-V
  - wasm: WebAssembly
