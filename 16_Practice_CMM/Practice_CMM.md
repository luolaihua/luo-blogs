# Practice Script Language 

[TOC]

原文链接：[PRACTICE Script Language User's Guide (PDF)](https://www.lauterbach.com/pdf/practice_user.pdf)

## 为什么使用PRACTICE 脚本(.cmm)

在TRACE32 中使用PRACTICE 脚本(*.cmm)将帮助你： 

1. 在调试器启动时立即执行命令
2. 根据您的项目需求自定义TRACE32PowerView用户界面
3. 使用目标板的配置来设置调试器
4. 标准化重复的和复杂的操作
5. 初始化目标(例如，要加载应用程序的内存）
6. 加载应用程序或符号
7. 添加您自己的功能， 并扩展可用的功能
8. 通过自动化加速调试
9. 与其他用户共享调试器方法， 并使他们能够更有效地工作
10. 使调试操作具有可重复性， 并可用于验证目的和回归测试  

# 相关参考文档

- [PRACTICE Reference Card (PDF)](https://www.lauterbach.com/reference_card_web.pdf)
- [PRACTICE Script Language User's Guide (PDF)](https://www.lauterbach.com/pdf/practice_user.pdf)
- [PRACTICE Script Language Reference Guide (PDF)](https://www.lauterbach.com/pdf/practice_ref.pdf)
- [PRACTICE Training Script Language (PDF)](https://www.lauterbach.com/pdf/training_practice.pdf)
- [About PRACTICE Script Language](https://www.lauterbach.com/practice.html)
- [PRACTICE Functions of the TRACE32 debug unit (PDF)](https://www.lauterbach.com/pdf/general_func.pdf)
- [PRACTICE Functions of the IDE framework (PDF)](https://www.lauterbach.com/pdf/ide_func.pdf)

# PRACTICE 脚本架构

### 函数 Function  

PRACTICE是一种面向线路（line-oriented）的测试语言，可用于解决数字测量工程的所有常见问题。PRACTICE-II是这种测试语言的增强版本，最初于1984年为在线仿真器开发。

这种测试语言允许交互式脚本开发，可以快速删除错误并立即执行脚本。PRACTICE 测试脚本的执行可以随时停止和重新启动。 

PRACTICE 包含一个非常强大的概念，用于处理脚本变量和命令参数。 此宏概念允许在命令中的任何位置替换参数。由于 PRACTICE 变量只能作为 PRACTICE 宏出现，因此排除了目标程序名称之间的冲突。

### 变量和PRACTICE 宏（PRACTICE Macros）之间的区别PRACTICE Macros

PRACTICE 宏基于类似于 C 预处理器宏的简单文本替换机制。 但是，与 C 预处理器宏相比，PRACTICE 宏只需分配一个新值，即可在其生命周期内更改其内容。

每次 PRACTICE 解释器遇到宏时，它都会被替换为相应的字符序列。只有在执行所有文本替换后，才会解释生成的行（就像 C 编译器仅适用于完全预处理的文本一样）。

PRACTICE 宏使用命令 **PRIVATE** 或 **LOCAL** 或 **GLOBAL** 声明。

PRACTICE宏的可见性明显不同于其他脚本语言（除非使用PRIVATE命令声明）：当它们处于活动状态时，可以从随后执行的所有代码中访问它们：

- 子程序(GOSUB … RETURN) 
- 子脚本 (DO … ENDDO) 
- 子块 (IF …, RePeaT, WHILE, etc.)

> PRACTICE不知道具有相应类型的变量的概念，例如C中的uint32或uint8。

### PRACTICE 脚本元素

PRACTICE 脚本由标签、命令和注释（ **labels**, **commands**, and **comments**）组成：

```assembly
;example   注释以分号开始 ;

//example  或者注释以两个斜杆开始： //

start:             	    // 标签
Step            	    // 命令
GOTO start   		    // 命令和标签

B::                	   //命令,更改默认设备
B::Data.dump  			//在命令之前有设备选择器
```

#### 标签Labels

**标签总是从第一列开始**，后面总是冒号。标签区分大小写。

#### 注释Comments

注释以分号开头；或者两个正斜杠//。Var.*命令的内联注释必须以两个正斜杠开头//:

`Var.set func7(1.5,2.5) //execute a function in the target`  

#### 行延续字符

要在下一行继续字符串，使用反斜杠\表示PRACTICE 脚本（*.cmm）中的行继续。反斜杠后不允许有空格。如果在注释行的末尾使用行连续字符，则下一行也将被解释为注释行。

> DIALOG.OK "Please switch ON the TRACE32 debugger first"+\
>
> " and then switch ON the target board."

### 脚本流

有几个命令允许控制脚本流。脚本可以分为几个模块。模块中的子例程由 GOSUB 命令调用，另一个模块由 DO 命令调用。

| STOP     | 暂时停止                   |
| -------- | -------------------------- |
| END      | 终止脚本并清除堆栈         |
| CONTinue | 继续执行脚本               |
| DO       | 调用脚本模块               |
| ENDDO    | 终止脚本模块               |
| RUN      | 清除PRACTICE堆栈和调用模块 |
| GOSUB    | 调用子例程                 |
| RETURN   | 从子例程返回               |
| GOTO     | 模块内的分支               |
| JUMPTO   | 分支到其他模块             |

### 条件脚本流

条件脚本执行由几个命令执行：

| IF       | 条件块执行                       |
| -------- | -------------------------------- |
| ELSE     | 仅在 IF 条件为 false 时编译的块  |
| WHILE    | 条件脚本循环                     |
| RePeaT   | 重复的脚本循环                   |
| ON       | 事件控制的PRACTICE 脚本执行      |
| GLOBALON | 全局事件控制的 PRACTICE 脚本执行 |
| WAIT     | 等待事件或延迟时间               |

如下示例：

```assembly
IF OS.FILE(data.tst)
PRINT "File exists"
ELSE
PRINT "File doesn't exist"
WHILE Register(pc)==0x1000
Step               ; step until pc = 1000H
RePeaT 100. Step   ; step 100 times
RePeaT 0. Step     ; step endless
ON ERROR GOTO errorexit
```

有关逻辑操作的详细信息，请参阅“PowerView 用户指南”（ide_user.pdf）中的“运算符”一章。

### 脚本嵌套

PRACTICE 脚本可以分层嵌套。第二个脚本可以作为初始脚本的子例程调用。此子例程本身可能会调用第三个脚本作为子例程。这允许结构化的模块化脚本开发。

```assembly
; 包含两个脚本调用的脚本
PRINT "Start"
DO modul1				; Execute script module 1
DO modul2				; Execute script module 2
ENDDO					; the file extension (*.cmm) can be omitted
```

### 块结构

可以将多个 PRACTICE 命令组合成一个块。块是命令的集合，这些命令始终同时执行。块通常需要 IF、WHILE 或 RePeaT 语句。但是，它们可以在任何地方实现，以便标记连接块。块用圆括号标记。

你可以跳出一个块，但不能跳出一个块。

```assembly
; Block nesting
start:
IF &abc
(
	PRINT "Function 1"
	DO func1
)
ELSE
(
	PRINT "Function 2"
	DO func2
	IF &xyz GOTO start ;jump out of the block to the label ‘start’
)
ENDDO
```

### PRACTICE 宏

PRACTICE 宏是最大大小为4KB的字符序列。字符序列在使用它的上下文中进行解释。对于命令，PRACTICE 宏可以解释为数字、布尔表达式、参数或简单的字符串。PRACTICE 宏也可以扩展以完成命令。

实际上，宏名称总是以一个符号（“&”）开头，后跟一系列字母（az、a-Z）、数字（0-9）和下划线符号（“&”）。&符号后的第一个字符不能是数字。宏名称区分大小写，因此&a不同于&A。

宏展开不会在TRACE32命令行内进行！例如 `PRINT &macroname` 或者`Data.List &my_startaddress`。

**宏扩展仅适用于 PRACTICE 脚本** （*.cmm）：

> 正常宏:  &<macroname>=<expression>
> 宏嵌套:  &&<macroname>=<expression> 

```assembly
&int=1
&int=&int+1                        ; increment current value of &int
&text="This is a test"
&command="Data.dump Register(PC)"
&float=1.4e13
&range="0x1000--0x1fff"
&address=func5
&addressrange=P:0x1234..0x5555
&boolean=SYStem.Up()
PRINT &int
PRINT "&int"                        ; after replacement: 0x2
PRINT "&(int)nd"                    ; after replacement: "2nd"
ENDDO

```

PRACTICE 宏可以声明为全局或本地或私有宏。

| LOCAL   | 声明本地宏 |
| ------- | ---------- |
| GLOBAL  | 声明全局宏 |
| PRIVATE | 声明私有宏 |

#### GLOBAL  宏

使用全局声明的PRACTICE 宏在每个脚本级别都可以访问，并且具有无限的生存期。

#### LOCAL  宏

使用 LOCAL 声明的 PRACTICE 宏在其生命周期内在所有后续执行的代码中都可见（除非被以后的宏声明隐藏）。特别是它们在以下位置可见：

子程序可见 Subroutines (`GOSUB ...RETURN`)
子脚本可见 Sub-scripts (`DO...ENDDO`)
子块可见 Sub-blocks (`IF..., RePeaT, WHILE`, etc.)  

#### PRIVATE 宏

使用 PRIVATE 声明的 PRACTICE 宏存在于声明块中，并在块结束时被擦除。它们仅在以下情况下可见：

声明块和所有子块可见(e.g. `IF..., RePeaT..., WHILE...`, etc.)

子程序不可见 Subroutines (`GOSUB...RETURN`)

子脚本不可见 Sub-scripts (`DO...ENDDO`)

> 如果将一个值分配给一个在PRACTICE 堆栈上尚不存在的宏，或者该宏是一个不可访问的私有宏，则该宏将被隐式创建为本地宏。

### 打开或关闭PRACTICE 宏扩展

您可以在以下嵌入式脚本块中打开或关闭 PRACTICE 宏扩展：

- DIALOG.view 嵌入在 PRACTICE 脚本文件 （*.cmm） 中的块，如下面的示例所示。 *
- 菜单。嵌入在实践脚本文件中的重新编程块 （*.cmm） *
- 嵌入在对话框文件 （*.dlg） 中的实践脚本块*
- 嵌入在菜单文件 （*.men） 中的实践脚本块

## 参数传递

可以将参数传递给具有参数列表的子例程。这些参数使用子例程中的 ENTRY 命令分配给本地 PRACTICE 宏。 子例程也可以通过参数以交互方式调用。

参数可以通过命令 DO、ENDDO、RUN、GOSUB、RETURN 传递。它们也可能是调用命令扩展或使用参数调用主机上的驱动程序的结果。 

表达式中运算符之前或之后的空格被解释为连续参数的分隔符。

表达式中运算符前后的**空格**被解释为连续参数的**分隔符**。

> ENTRY 					Parameter passing  

```assembly
SYStem.Up
GOSUB myTEST 0x0--0xfff
ENDDO
;by calling the subroutine myTEST, a memory test of the address range
;0x0--0xfff can be executed
myTEST:
ENTRY &range
Data.Test &range
RETURN
```

## 输入输出

多个输入和输出命令允许与用户交互。输入通常通过 AREA 窗口完成。所有打印操作都显示在 TRACE32 消息行上。默认情况下，将显示“区域”窗口 A000。输入和输出可以重新路由到另一个 AREA 窗口。

| PRINT | 打印到屏幕                     |
| ----- | ------------------------------ |
| BEEP  | 激活声音发生器，发出“哔”的声音 |
| ENTER | 基于窗口的输入                 |
| INKEY | 字符输入                       |

```assembly
PRINT "The PC address is " Register(pc) ; 打印消息
BEEP 									; end acoustic signal
INKEY 									; 等待键盘响应
INKEY &char								; 等待键盘响应
IF &char=='A'
GOSUB func_a
IF &char=='B'
GOSUB func_b
…
AREA.Create IO-Area						;新建一个名为IO-Area的窗口
AREA.Select IO-Area						;选择这个IO-Area的窗口
AREA.view IO-Area						;打开这个IO-Area的窗口
PRINT "Set the PC value"				;打印消息
ENTER &pc								;获取值
Register.Set pc &pc						;设置寄存器PC的值
WINClear TOP							;关闭窗口
AREA.RESet								;重设AREA系统
ENDDO
```

屏幕更新可能由 SCREEN 命令控制:

| SCREEN.display | 立即更新屏幕                                           |
| -------------- | ------------------------------------------------------ |
| SCREEN.ALways  | 每个命令行后更新屏幕                                   |
| SCREEN.ON      | 更新打印命令的屏幕                                     |
| SCREEN.OFF     | 只要脚本正在运行，就不要更新屏幕                       |
| SCREEN.WAIT    | 暂停 PRACTICE 脚本执行，直到处理完要在窗口中显示的数据 |

### 文件操作

| OPEN   | Open file           |
| ------ | ------------------- |
| CLOSE  | Close file          |
| READ   | Read data from file |
| WRITE  | Write data to file  |
| APPEND | Append data to file |

示例 1：创建了一个名为 test.dat 的新文件，并将寄存器信息写入新创建的文件中。 然后，结果将显示在“类型”窗口中:

```assembly
OPEN #1 test.dat /Create
WRITE #1 "PC: " Register(pc)
WRITE #1 "SP: " Register(sp)
CLOSE #1
TYPE test.dat
ENDDO
```

![image-20220415140226060](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220415140226060.png)

示例 2：打开 test.dat 文件进行读取。从此文件中读取两行并存储在两个 PRACTICE 宏中，然后将这些宏打印到 TRACE32 消息行。

```assembly
OPEN #1 test.dat /Read
READ #1 %LINE &pc ;line 1 of file
READ #1 %LINE &sp ;line 2 of file
CLOSE #1
PRINT "&pc " "&sp"
ENDDO
```

![image-20220415140446627](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220415140446627.png)

## 自动启动脚本

安装 TRACE32 软件后，脚本 autostart.cmm 将复制到 TRACE32 系统目录中。autostart.cmm 始终在 TRACE32 启动后自动执行。它提供了Lauterbach 定义的各种便利功能。建议不要更改 autostart.cmm，因为 Lauterbach 的每个软件更新都会将文件 autostart.cmm 还原为其默认内容。

autostart.cmm 调用以下脚本（如果存在）：

- ~~/system-settings.cmm，其中 ~~ 表示 TRACE32 系统目录。 建议在此处添加额外的 TRACE32 设置，这些设置应可供 TRACE32 安装的所有用户使用。典型的额外设置是菜单/工具栏扩展或用户定义的对话框。
- UAD/user-settings.cmm，其中 UAD 表示特定于用户的应用程序数据目录。TRACE32 函数版本。环境 （UAD） 返回此目录的路径。 用户可以将所有首选的额外 TRACE32 设置添加到 user-settings.cmm 脚本中。 典型的额外设置是 SETUP 命令组和个人菜单/工具栏扩展的所有设置。
-  ./work-settings.cmm，其中前导“.”表示从 TRACE32 启动的工作目录。

> 注意：如果您不使用命令行选项 -s <startup_script> 并且也没有文件 autostart.cmm，则 TRACE32 将回退到旧模式，并从工作目录或 TRACE32 系统目录（如果工作目录中不存在 t32.cmm）执行脚本 t32.cmm

如果您有一个设置调试环境的脚本，并且此脚本应在 autostart.cmm 完成后自动执行，则可以将此脚本指定为 TRACE32 可执行文件的参数。

`c:\t32\t32arm.exe -s g:\and\arm\start_up.cmm  `

可以将参数直接传递给启动脚本:

`c:\t32\t32arm.exe -s g:\and\arm\start_up.cmm param1 param2 param3  `

命令行选项 `--t32-safestart` 禁止执行 autostart.cmm 和任何其他启动脚本。

## 记录PRACTICE 脚本的调用层次结构

PRACTICE 脚本 （*.cmm） 的调用层次结构可以自动或手动记录。在任一情况下，日志机制都基于 LOG.DO   命令。

在 TRACE32 启动期间，PRACTICE 脚本调用始终自动记录。日志文件内容将输出到 TRACE32 的临时目录中的自动启动日志文件。在每次启动 TRACE32 时，都会覆盖以前的自动启动日志文件，并生成一个新日志文件。可通过 TRACE32 中的“文件File  ”菜单访问当前的自动启动日志。

 此外，您可以在 TRACE32 启动后随时手动记录 PRACTICE 脚本调用。启动日志时，可以选择文件夹和文件名。若要显示日志文件，请使用 TRACE32 命令行上的 TYPE 或 EDIT 命令。

若要启用日志记录，请使用下列选项之一：

- autostart.cmm：在 TRACE32 启动时，会自动调用 autostart.cmm 和 LOG。autostart.cmm 中的 LOG.DO  命令生成自动启动日志文件。
-  `--t32-log` 自动启动：此命令行选项启动 LOG.DO  。在内部执行以生成自动启动日志文件。 
  - 仅当 （a） 没有 autostart.cmm 时才需要此选项，或者 （b） 如果脚本块与  LOG.DO一起使用。 LOG.DO命令已从 autostart.cmm 中删除。 
  - 有关命令行选项的说明和 `--t32-logautostart` 的示例，请参阅 TRACE32 安装指南第 61 页（installation.pdf  ）中的“用于启动 TRACE32 的命令行参数”。 提示： 要在启动时显式禁用所有 PRACTICE 脚本调用，请使用 `--t32-safestart`。 

- TRACE32 命令行：使用LOG.DO <file>   命令以生成用户自己的日志

要访问 TRACE32 中的自动启动日志文件，请执行以下操作：

1. 通过 T32Start 启动 TRACE32。 autostart.cmm 会自动生成自动启动日志文件。

2. 选择“文件”菜单>“启动”>查看自动启动日志中的自动脚本“ 。 文件将在“TYPE”窗口中打开。屏幕截图显示了自动启动日志文件的示例：

   ![image-20220415143439667](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220415143439667.png)

   A：自动启动日志的文件名约定如下所述。 

   B :日志文件头告诉您自动启动日志是如何生成的。

## 调试PRACTICE 脚本

TRACE32 支持 PRACTICE 脚本的广泛调试功能。PEDIT 命令允许您创建和编辑 PRACTICE 脚本。两个基本窗口显示脚本、内部堆栈和 PRACTICE 宏:

| PEDIT       | Edit PRACTICE scripts                            |
| ----------- | ------------------------------------------------ |
| PLIST       | List PRACTICE script                             |
| PMACRO.list | List PRACTICE script nesting and PRACTICE macros |

在 PLIST 窗口中，您可以设置无限数量的程序断点来调试 PRACTICE 脚本。双击整行设置断点;再次双击同一行将删除断点。也就是说，您可以通过双击一行来切换断点。 或者，右键单击一行，然后从弹出菜单中选择“切换断点”。

![image-20220415143835499](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220415143835499.png)

启用的断点用红色小条标记，禁用的断点在 PLIST 窗口中用灰色小条标记。

| PBREAK.Set     | Set breakpoints in PRACTICE |
| -------------- | --------------------------- |
| PBREAK.Delete  | scripts Delete breakpoints  |
| PBREAK.List    | Display breakpoint list     |
| PBREAK.ENable  | Enable breakpoint           |
| PBREAK.DISable | Disable breakpoint          |

PMACRO.list 窗口显示脚本嵌套、本地和全局 PRACTICE 宏以及 ON 和 GLOBALON 定义：

![image-20220415144111402](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220415144111402.png)

双击 PRACTICE 宏（例如 &val1）会将其插入到 TRACE32 命令行中，您可以在其中修改 PRACTICE 宏的参数。 可以使用 PSTEP 命令逐步执行脚本。

TRACE32 主工具栏中的“停止”按钮可停止任何正在运行的 PRACTICE 脚本。

> PSTEP <script> Start script to be debugged in single step mode  

```assembly
PBREAK.Set 4. test.cmm
DO test.cmm
PSTEP
PSTEP
; set breakpoint
; run till line 4
; single step
```

