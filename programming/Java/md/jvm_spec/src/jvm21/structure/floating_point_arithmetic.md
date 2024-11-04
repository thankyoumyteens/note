# 浮点数运算

The Java Virtual Machine incorporates a subset of the floating-point arithmetic
specified in the IEEE 754 Standard.

In Java SE 15 and later, the Java Virtual Machine uses the 2019 version of the IEEE 754
Standard. Prior to Java SE 15, the Java Virtual Machine used the 1985 version of the IEEE
754 Standard, where the binary32 format was known as the single format and the binary64
format was known as the double format.

Many of the Java Virtual Machine instructions for arithmetic and
type conversion work with floating-point numbers. These instructions
typically correspond to IEEE 754 operations (Table 2.8-A), except for certain
instructions described below.

Table 2.8-A. Correspondence with IEEE 754 operations

| Instruction                        | IEEE 754 operation                                                                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| _`dcmp<op>`_, _`fcmp<op>`_         | compareQuietLess, compareQuietLessEqual, compareQuietGreater,compareQuietGreaterEqual, compareQuietEqual, compareQuietNotEqual |
| _`dadd`_, _`fadd`_                 | addition                                                                                                                       |
| _`dsub`_, _`fsub`_                 | subtraction                                                                                                                    |
| _`dmul`_, _`fmul`_                 | multiplication                                                                                                                 |
| _`ddiv`_, _`fdiv`_                 | division                                                                                                                       |
| _`dneg`_, _`fneg`_                 | negate                                                                                                                         |
| _`i2d`_, _`i2f`_, _`l2d`_, _`l2f`_ | convertFromInt                                                                                                                 |
| _`d2i`_, _`d2l`_, _`f2i`_, _`f2l`_ | convertToIntegerTowardZero                                                                                                     |
| _`d2f`_, _`f2d`_                   | convertFormat                                                                                                                  |

The key differences between the floating-point arithmetic supported by the Java
Virtual Machine and the IEEE 754 Standard are:
