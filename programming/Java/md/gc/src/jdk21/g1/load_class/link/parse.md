# 将符号引用转换成直接引用

JVM 规范规定, 指令 anewarray, checkcast, getfield, getstatic, instanceof, invokedynamic, invokeinterface , invokespecial , invokestatic, invokevirtual , Idc, ldc_w, multinewarray, multianewarray, new, putfield 和 putstatic 将符号引用指向运行时常量池。当执行到上述指令时, 需要对它的符号引用进行解析。
