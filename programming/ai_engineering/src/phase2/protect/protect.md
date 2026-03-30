# Context 注入与安全防护

Prompt Injection（提示词注入）的本质，和防范 SQL 注入（SQL Injection） 或 跨站脚本攻击（XSS） 的底层逻辑是完全一模一样的：系统把用户输入的数据（Data），错误地当成了可执行的指令（Code）。
