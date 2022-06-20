# ARM 立即数范围以及立即数的编码规则

# 一，问题描述

笔者在写汇编代码时曾遇到过**立即数不合法**的问题：

`Immediate 0xXXX cannot be represented by 0-255 and a rotation`

比如笔者代码中含有如下命令：

```assembly
MOV R1, #888888 ; #888888 is 0xD9038
```

使用RVDS（RealView Development Suite）编译器进行编译，则会报出如下错误：

![image-20220615113924770](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220615113924770.png)

通过阅读ARM相关技术手册，笔者有如下发现：

- 不同类型的指令，其支持的立即数长度不一样，比如有的是 `imm12`，有的是 `imm8`和 `imm5`，其中12和5分别代表立即数的比特位数，比如立即数长度为8bits时，其能表示的范围为：`0b0 ~ 0b1111 1111`，即为 `0~255`。
- 可以将立即数进行拆分，比如 `imm12 = rotate4 + imm8`，拆分成循环位移和立即数常数，通过将立即数常数`imm8`循环右移`rotate4`位，即可组成范围大于12bits组成的立即数（`0b1111 1111 1111=4095`）。

# 二，立即数范围

在ARM中，无论是Arch64还是Arch32，一条汇编指令的编码长度固定为32bits，在Thumb中为16bits，这就意味着不能将带有操作码（opcode）的汇编指令编译成任意的32bits的值。

在文档编号为`DDI01001`的[ARMv5 Architecture reference Manual](https://developer.arm.com/documentation/ddi0100/i/)的文档中有如下表格：

![image-20220619214738994](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220619214738994.png)

从表格中可以看出，在ARM指令集中，一条汇编指令编码成32bits后，将不同的位数划分成不同的功能区间，比如条件码（condition codes）和操作码，还有比特位要留给指令本身和寄存器使用，通常情况下只有12-bits的长度可以用来表示立即数（immediate）。

12bits可以表示的无符号数范围为：`0~4095`，有符号数的范围为：`-2048 ~ +2047`，如果不在这12 bits的立即数上增加点创作性，而直接硬解码用来表示立即数是远远不够的。所以在ARM中将这12 bits分为 8-bit 常数（0~255）和 4-bit旋转位移值（0~15），8 bits 常数可以按照循环位移值的2倍（0~30）向右进行循环位移，位移的步进值是以2为单位，可以是：`0、2 、4 、6 、…  、30`。

比如 `0x23000000`占32bits，远远超过了12 bits，如果直接硬解码是表示不了的，但是其可以由 `0x23 ROR 8`得到，ROR是以32bits的位宽为基础，向右循环位移，从右边旋转出来的比特位被插入到左边空出的位中。因此按此规则， `0x23000000`的12-bit立即数表示应为：`0b0100 0010 0011`。关于其解释，见下文。

# 三，立即数编码

本章拿数据处理指令的编码举例，如下图所示为[DI0406C_arm_architecture_reference_manual](https://developer.arm.com/documentation/ddi0406/c/)参考手册中关于数据处理指令编码的表格：

![image-20220620203024660](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220620203024660.png)

更进一步，本章详细地用 ARM cortex-A系列的`MOV`指令为例：

![image-20220620203452213](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220620203452213.png)

其中的条件码 `cond`在无条件下为 `1110`，详情参考下图：

![image-20220620204022871](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220620204022871.png)

本章拿立即数 `0x23000000`举例，如下的汇编指令：

```assembly
MOV r4, #0x23000000
```

按照上述的编码规则将会被编码成：`0xE3A04423`：

![image-20220620204759336](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220620204759336.png)

换算成二进制：

![image-20220620205229926](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220620205229926.png)

即 `0x23000000`的12-bit立即数表示为：`0b0100 0010 0011`。其中高4位为`0100 = 4`，可求得循环右移的位数为 `4*2=8`，低八位 `0010 0011`即为 `0x23`。将 `0x23`循环右移8位，也正是立即数 `0x23000000`。

更多的编码示例可参考下图，图片来自[ARM指令集中立即数寻址的范围](https://www.cnblogs.com/imapla/archive/2013/01/25/2877234.html)

![image-20220620205716828](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220620205716828.png)

在ARMv7中管这种循环右移得到的立即数叫做 `modified immediate constants`,在参考手册[DI0406C_arm_architecture_reference_manual](https://developer.arm.com/documentation/ddi0406/c/)中有其更详细的描述：

![image-20220620210141302](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220620210141302.png)

![image-20220620210705030](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/image-20220620210705030.png)

其中 `abcdefgh`8个数，分别代表不同的比特位，还有一点需要特别注意，`rotation`的数值乘以2，才表示真正的循环右移次数。

![在这里插入图片描述](ARM%20%E7%AB%8B%E5%8D%B3%E6%95%B0%E8%8C%83%E5%9B%B4%E4%BB%A5%E5%8F%8A%E5%90%88%E6%B3%95%E7%AB%8B%E5%8D%B3%E6%95%B0.assets/70.jpeg)

综上所述，我们可以得出以下结论：

- 如果一个立即数小于 `0xFF（255）`那么直接用 `immed_8` 的8个比特位表示，此时不用移位，11～8 位的 `Rotate_imm` 等于 0。
- 如果 `immed_8` 的数值大于 `0xFF（255）`，那么就看这个数是否能有 `immed_8` 中的某个数移位 `2*Rotate_imm` 位形成的。如果能，那么就是合法立即数；否则非法。

关于立即数合不合法，可先参考这篇文章 [ARM 立即寻址之立即数的形成 —— 如何判断有效立即数](https://blog.csdn.net/sinat_41104353/article/details/83097466)。

