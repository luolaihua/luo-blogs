# ARMv7和ARMv8中关于内存访问的汇编指令总结对比

# 前言

ARM处理器是精简指令集计算机 (Reduced Instruction Set Computer，RISC)  处理器，复杂指令集计算机（Complex Instruction Set Computer，CISC）处理器，比如X86，具有丰富的指令集，能够用单个指令执行复杂的操作。这种处理器通常具有大量的内部逻辑，用于将机器指令解码为内部操作序列（微码，microcode  ）。相比之下，RISC架构具有较少数量的更通用的指令，这些指令可使用更少的晶体管执行，从而节省生产成本并且更节能。与其他RISC架构一样，ARM的内核具有大量通用寄存器，许多指令在单个周期（cycle）内执行。它具有简单的寻址模式，其中所有加载/存储的地址都可以从寄存器内容和指令字段中确定。

ARM 指令集通常被认为是简单、合乎逻辑和高效的。但是，它不能直接在内存上执行数据处理操作：比如，要递增某个内存位置中的值，必须先将该值加载到 ARM 寄存器，在寄存器中递增，并且需要第三条指令才能将更新的值再写回内存当中。

与 x86（但与 [68K](https://baike.baidu.com/item/68K/10168192) 不同）一样，ARM 指令通常采用两个或三个操作数格式，在大多数情况下，第一个操作数指定结果的目标（多加载/多存储例外）。相比之下，68K 将目标作为最后一个操作数。对于 ARM 指令，通常对哪些寄存器可用作操作数没有限制。下面给出了不同汇编语言之间差异的风格：

```
#使寄存器的值自增100的指令
x86: add eax, #100
68K: ADD #100, D0
ARM: add r0, r0, 100
#将r1中保存的地址上的值加载到r0,r1可看作是寄存器指针
x86: mov eax, DWORD PTR [ebx]
68K: MOVE.L (A0), D0
ARM: ldr r0, [r1]
```

ARMv7和ARMv8都是 **加载/存储** 架构，这意味着它们不能直接对内存中的数据进行处理， 只有加载和存储指令才能访问内存。所以需要通过通用寄存器（GPR），先将内存中的数据加载到寄存器中，处理完成后，再存储回内存中。此外，ARMv8具有A64模式和A32模式，也就是64bits模式和32bits模式，32bits模式的指令集和ARMv7的指令集几乎一致。所以在学习ARMv7指令集的同时，也是相当于在学习ARMv8的A32模式的指令集。

笔者最近在做ARMv8下的内存拷贝实验，需要在A64模式和A32模式下进行，所以对ARMv7和ARMv8下的内存访问汇编指令进行总结和对比。

在文章开始前有必要对ARMv7和ARMv8寄存器的位宽进行简单说明。一般情况下，ARMv8中用X表示A64下的64bits寄存器，W则是32bits寄存器。此外还有 B、H、S、D 以及 Q 寄存器，它们的位宽如下图所示。在ARMv7中通用寄存器则是用R表示，它与ARMv8下的W是一致的。

![image-20220504144618085](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220504144618085.png)



# ARMv7下的内存访问指令

ARM 内核仅在寄存器上执行算术逻辑单元 （ALU） 操作。唯一支持的内存操作是加载（LOAD，LDR，将数据从内存读取到寄存器）或存储（STORE，STR，将数据从寄存器写入内存）。

用户可以通过在指令中附加 B 表示 Byte（8位）、H 表示Halfword ，半字（16位）、或 D表示doubleword ，双字（64 位），来指定加载或存储传输的大小，例如 LDRB。仅对于加载LDR，还可以使用额外的 S 来指示有符号字节或半字（SB 表示有符号字节，SH 表示有符号半字）。附加的类型可以是:

- B – unsigned Byte. (Zero extend to 32 bits on loads.)
- SB – signed Byte. (Sign extend to 32 bits.)
- H – unsigned Halfword. (Zero extend to 32 bits on loads.)
- SH – signed Halfword. (Sign extend to 32 bits.)  

这种方法可能很有用，因为如果将 8 位或 16 位加载到 32 位寄存器中，则必须决定如何处理寄存器中的符号位。无符号数字是零扩展的（即寄存器最重要的16或24位设置为零），但对于有符号数字，必须将符号位（字节的位[7]或半字的位[15]）复制到寄存器的前16位（或24位）。

## 寻址模式

LDR和STR有多种寻址模式，如下示例：

- (1) LDR R0, [R1]                      ;加载的地址保存在R1当中
- (2) LDR R0, [R1, R2]                ;加载的地址为R1 + R2
- (3) LDR R0, [R1, R2, LSL #2]   ;加载的地址R1 + (R2*4)，逻辑左移1位相当于乘以2
- (4) LDR R0, [R1, #32]!             ;先更新 R1为R1 + 32，然后再从地址R1（R1:=R1 + 32）上加载
- (5) LDR R0, [R1], #32              ;先从R1处加载，然后更新 R1为R1 + 32

方式（1）为寄存器寻址（Register addressing）方式，从R1中保存的数据为地址，将该地址上的数据加载到R0。

方式（2）和（3）为前下标寻址（Pre-indexed addressing），在内存访问之前添加基址寄存器的偏移量，基本的形式为：`LDR Rd, [Rn, Op2]  `，偏移量可以是正数或负数，也可以是立即数或另一个应用了可选移位的寄存器。

方式（4）为前下标寻址+写回（Pre-indexed with write-back），它指令的最后使用了一个感叹号`!`，可以理解为优先进行R1:=R1 + 32操作，即先更新 R1为R1 + 32，然后再将R1所指向的数据加载到R0当中。

方式（5）为后下标+写回（Post-index with write-back），偏移量在方括号之外，表示先进行数据加载，即先从R1处加载，然后更新 R1为R1 + 32。

## 多加载/存储

多加载和存储（LDM/STM)使连续的字（word，4字节）可以从存储器中读取或写入。这些对于堆栈操作和内存复制非常有用。只有word可以以这种方式操作，并且必须使用与word对齐的地址。如下指令：

```
LDMIA R10!, { R0-R3, R12 }  
```

操作数是一个基址寄存器（带有可选的 ！表示基址寄存器的回写，即更新基址寄存器），大括号之间有一个寄存器列表。寄存器列表以逗号分隔，连字符`-`用于指示范围。寄存器的加载或存储顺序与此列表中指定的顺序无关。相反，该操作以固定方式进行，**编号最低的寄存器始终映射到最低的地址**。

如上示例指令，大括号内有R0，R1，R2，R3和R12五个目标寄存器，基址寄存器为R10，则该指令会进行如下操作：

```
[R10] -> R0
[R10+4] -> R1
[R10+8] -> R2
[R10+12] -> R3
[R10+16] -> R12
```

由于加了`!`，操作完成后还需要对R10进行更新，将R10更新为R10+20。

该指令还必须指定如何从基址寄存器 Rd 中继续操作。有四种情况：

- IA/IB（之后/之前递增，Increment After/Before  ）
- DA/DB（之后/之前递减，Decrement After/Before  ）

这些也可以使用后缀（FD，FA，ED和EA），这些后缀是从栈stack的角度工作的，ARM7支持四种堆栈模式：满递减(FD)、满递增(FA)、空递减(ED)、空递增(EA)，并指定栈指针是指向栈的完整（Full)顶部还是空(Empty)的顶部，以及栈在内存中是上升(Ascend)还是下降(Descend)。

- FD：堆栈地址从上往下递减，且指针指向最后一个入栈元素。
- FA：堆栈地址从下往上递增，且指针指向最后一个入栈元素。
- ED：堆栈地址从上往下递减，且指针指向下一个可用空位。
- EA：堆栈地址从下网上递增，且指针指向下一个可用空位。

按照惯例，**只有（FD） 选项是用于基于 ARM 处理器系统中的栈**。这意味着栈指针指向栈内存中最后填充的位置，并且将随着压入到栈的每个新数据项而递减。

```assembly
STMFD sp!, {r0-r5} ; 将r0至r5压入FD栈，并且更新指针
LDMFD sp!, {r0-r5} ; 将r0至r5弹出FD栈，并且更新指针
```

下图展示了将R1和R2压入一个FD栈中，在执行 STMFD （PUSH） 指令之前，栈指针SP指向栈中最后一个占用的word。指令完成后，栈指针SP递减 8（两个word），两个寄存器的内容已写入内存，由于内存地址是向上递增，并且按照**编号最低的寄存器将写入最低的内存地址**的规则，所以R2在R1的上方。

![压栈操作](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220504160835646.png)

# ARMv8下的内存访问指令

与所有以前的 ARM 处理器一样，ARMv8 架构是加载/存储架构。程序必须指定地址、要传输的数据的大小以及源或目标寄存器。ARMv8还有其他加载和存储指令，提供了更多选项，例如非临时加载/存储（non-temporal Load/Store  ）、加载/存储独占项（Load/Store exclusives），和获取/释放（Acquire/Release）。

## 加载和存储指令格式

ARMv8中的加载和存储指令和ARMv7中的相同：

```
LDR Rt, <addr>  
STR Rn, <addr>  
```

当加载整数寄存器时，可选择数据大小进行加载，例如，要加载小于指定寄存器值的大小，可将以下后缀之一追加到 LDR 指令中：

- LDRB (8-bit, zero extended).
- LDRSB (8-bit, sign extended).
- LDRH (16-bit, zero extended).
- LDRSH (16-bit, sign extended).
- LDRSW (32-bit, sign extended).  

还有未缩放的偏移形式，例如LDUR<type>，程序员通常不需要显式使用 LDUR形式，因为大多数汇编程序可以根据使用的偏移量选择适当的版本。

用户不需要指定对 X 寄存器的零扩展加载，因为写入 W 寄存器实际上为零会扩展到整个寄存器宽度。

下图为指令`LDRSB W4, <addr>`  的示意图，在ARMv8中寄存器为64位，W寄存器为A32模式下的描述，所以只用上了前32位。SB为有符号8位扩展，在addr地址上的数据为0x8A，将其加载到W4中，并进行有符号扩展，最后得到的结果为：![image-20220504192128300](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220504192128300.png)

下图为指令`LDRSB X4, <addr>`  的示意图，在ARMv8中寄存器为64位，X寄存器为A64模式下的描述，所以为64位。SB为有符号8位扩展，在addr地址上的数据为0x8A，将其加载到X4中，并进行有符号扩展，最后得到的结果为：

![image-20220504192515719](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220504192515719.png)

下图为指令`LDRB W4, <addr>`  的示意图，SB为零扩展，在addr地址上的数据为0x8A，将其加载到W4中，并进行零扩展，最后得到的结果为：

![image-20220504192614599](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220504192614599.png)

此外，如果要存储的数据大小可能小于寄存器，可以通过向 STR 添加 B 或 H 后缀来指定此项。

## 浮点和 NEON 标量加载和存储

加载和存储指令还可以访问浮点/NEON 寄存器。大小仅由正在加载或存储的寄存器确定，寄存器可以是任何 B、H、S、D 或 Q 寄存器。并且浮点和标量 NEON 的加载和存储，使用与整数寄存器加载和存储相同的寻址模式。

![Memory bits written by Load instructions](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220504193024266.png)

![Memory bits read by Store instructions](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220504192850607.png)

需要注意的是，符号扩展（sign-extension）并不支持加载到 FP/SIMD 寄存器中。此类加载的地址仍使用通用寄存器指定。比如：

```assembly
LDR D0, [X0, X1]  
```

D寄存器也为64位（doubleword ，8字节），上述指令会将地址X0+X1上的数据加载到D0寄存器当中。

## 指定加载或存储指令的地址

A64 可用的寻址模式与 A32 和 T32 中的寻址模式类似。有一些额外的限制以及一些新功能，但对于熟悉A32或T32的人来说，A64可用的寻址模式并不陌生。 在 A64 中，地址操作数的基本寄存器必须始终是 X 寄存器。但是，有几条指令支持零扩展或符号扩展，因此可以提供 32 位偏移量作为 W 寄存器。

### 偏移模式

偏移寻址模式将立即数或可选的修改的寄存器值添加到 64 位基址寄存器以生成地址。

```assembly
LDR X0, [X1]                ;Load from the address in X1
LDR X0, [X1, #8]            ;Load from address X1 + 8
LDR X0, [X1, X2]            ;Load from address X1 + X2
LDR X0, [X1, X2, LSL, #3]   ;Load from address X1 + (X2 << 3)
LDR X0, [X1, W2, SXTW]      ;Load from address X1 + sign_extend(W2)
LDR X0, [X1, W2, SXTW, #3]  ;Load from address X1 + (sign_extend(W2) << 3)  
```

通常，在指定移位或扩展选项时，移位量可以是访问大小的 0（默认值）或 log2（以字节为单位）（以便 Rn << <shift> 将 Rn 乘以访问大小）。

以下是一段C程序的示例：

```c
// A C example showing accesses that a compiler is likely to generate.
void example_dup(int32_t a[], int32_t length) 
{
	int32_t first = a[0]; // LDR W3, [X0]
	for (int32_t i = 1; i < length; i++) 
    {
		a[i] = first; // STR W3, [X0, W2, SXTW, #2]
	}
}
```

### 索引模式

索引模式类似于偏移模式，但它们会更新基址寄存器。语法与 A32 和 T32 中的语法相同，但操作集的限制性更强。通常，只能为索引模式提供立即数偏移量。同ARMv7一样，有两种变体：前索引模式（在访问内存之前应用偏移量）和后索引模式（在访问内存后应用偏移量）：

```assembly
LDR X0, [X1, #8]!         ;Pre-index: Update X1 first (to X1 + #8), then load from the new address
LDR X0, [X1], #8          ;Post-index: Load from the unmodified address in X1 first, then update X1 (to X1 + #8)
STP X0, X1, [SP, #-16]!   ;Push X0 and X1 to the stack.
LDP X0, X1, [SP], #16     ;Pop X0 and X1 off the stack  
```

C语言示例：

```c
// A C example showing accesses that a compiler is likely to generate.
void example_strcpy(char * dst, const char * src)
{
	char c;
do {
	c = *(src++); // LDRB W2, [X1], #1
	*(dst++) = c; // STRB W2, [X0], #1
	} while (c != '\0');
}
```

## 访问多个内存位置

**A64 不包括 A32 和 T32 代码可用的多加载 （LDM） 或多存储（STM） 指令**。

在 A64 代码中，有成对加载（Load Pair ，LDP） 和存储对（Store Pair，STP）。与 A32中的LDRD 和 STRD 指令不同，LDP/STP可以读取或写入任何两个整数寄存器。数据被读取或写入到相邻的内存位置或从相邻的内存位置写入。为这些指令提供的寻址模式选项比其他内存访问指令更具限制性。

LDP 和 STP 指令只能使用具有缩放的 7 位有符号立即数的基址寄存器，并具有可选的预增量或后增量。与 32 位 LDRD 和 STRD 不同，LDP 和 STP 可以进行未对齐的访问。

- 指令`LDP W3, W7, [X0]`，它将[X0]上的数据加载到W3，将[X0+4]加载到W7，如图：

  ![LDP W3, W7 [X0]  ](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220504200848918.png)

- 指令`LDP X8, X2, [X0, #0x10]!` ，将[X0, #0x10]上的数据加载到X8，将[X0 + 0x10 + 8]上的数据加载到X2，如图：

  ![LDP X8, X2, [X0 + #0x10]!](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220504200913340.png)

- 指令`LDPSW X3, X4, [X0]`，将[X0]加载到X3，将[X0+4]加载到X4，并且进行有符号扩展，扩展到64bits

- 指令`LDP D8, D2, [X11], #0x10` ，将[X11]加载到D8，将[X11+8]加载到D2，最后将X11更新为X11+0x10

- 指令`STP X9, X8, [X4]`， 将64bits的数据从X9 存储到地址[X4],并且将X8中的64bits数据存储到[X4+8]