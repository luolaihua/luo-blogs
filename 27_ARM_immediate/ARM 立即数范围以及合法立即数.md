# ARM 立即数范围以及合法立即数

# 一，问题描述

笔者在写汇编代码时曾遇到过立即数不合法的问题：

`Immediate 0xXXX cannot be represented by 0-255 and a rotation`

比如笔者代码中含有如下命令：

```assembly
MOV R1, #888888 ; #888888 is 0xD9038
```

使用RVDS（RealView Development Suite）编译器进行编译，则会报出如下错误：

![image-20220615113924770](C:/Users/10658/AppData/Roaming/Typora/typora-user-images/image-20220615113924770.png)

通过阅读ARM相关技术手册，笔者有如下发现：

- 不同类型的指令，其支持的立即数长度不一样，比如有的是 `imm12`，有的是 `imm8`和 `imm5`，其中12和5分别代表立即数的比特位数，比如立即数长度为8bits时，其能表示的范围为：`0b0 ~ 0b1111 1111`，即为 `0~255`。
- 可以将立即数进行拆分，比如 `imm12 = rotate4 + imm8`，拆分成旋转位移和立即数因子，通过将立即数因子`imm8`逻辑右移`rotate4`位，即可组成范围大于12bits组成的立即数（`0b1111 1111 1111=4095`）。

# 二，立即数范围

在ARM中，无论是A64还是A32，一条汇编指令的编码长度固定为32bits，在Thumb中为16bits，这就意味着不能将带有操作码（opcode）的汇编指令编译成任意的32bits的值。

在文档编号为`DDI01001`的[ARMv5 Architecture reference Manual](https://developer.arm.com/documentation/ddi0100/i/)的文档中有如下表格：

![image-20220619214738994](C:/Users/10658/AppData/Roaming/Typora/typora-user-images/image-20220619214738994.png)

从表格中可以看出，在ARM指令集中，一条汇编指令编码成32bits后，将不同的位数划分成不同的功能区间，比如条件码（condition codes）和操作码，还有比特位要留给指令本身和寄存器使用，通常情况下只有12-bits的长度可以用来表示立即数（immediate）。

12bits可以表示的无符号数范围为：`0~4095`，有符号数的范围为：`-2048 ~ +2047`，如果不在这12 bits的立即数上增加点创作性，而直接硬解码用来表示立即数是远远不够的。

# 三，立即数求取

# 四，合法立即数

![image-20220615115724047](C:/Users/10658/AppData/Roaming/Typora/typora-user-images/image-20220615115724047.png)

![image-20220615115650572](C:/Users/10658/AppData/Roaming/Typora/typora-user-images/image-20220615115650572.png)