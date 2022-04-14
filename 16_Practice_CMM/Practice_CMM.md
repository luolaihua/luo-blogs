# Practice Script Language 

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

### PRACTICE 脚本架构

## 函数 Function  

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

```bash
;example   注释以分号开始 ;

//example  或者注释以两个斜杆开始： //

start:                // 标签
Step                // 命令
GOTO start     // 命令和标签

B::                   //命令,更改默认设备
B::Data.dump  //在命令之前有设备选择器
```

### 标签Labels

标签总是从第一列开始，后面总是冒号。标签区分大小写。

#### 注释Comments

注释以分号开头；或者两个正斜杠//。Var.*命令的内联注释必须以两个正斜杠开头//:

`Var.set func7(1.5,2.5) //execute a function in the target`  

#### Line Continuation Character

要在下一行继续字符串，使用反斜杠\表示练习脚本（*.cmm）中的行继续。反斜杠后不允许有空格。如果在注释行的末尾使用行连续字符，则下一行也将被解释为注释行。

> DIALOG.OK "Please switch ON the TRACE32 debugger first"+\
>
> " and then switch ON the target board."

### Script Flow

![image-20210813161831979](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20210813161831979.png)

### Conditional Script Flow

![image-20210813161904877](C:/Users/10658/Desktop/WORK/ARMv8_Note/ARMv8_note.assets/image-20210813161904877.png)

![image-20210813162440767](C:/Users/10658/Desktop/WORK/ARMv8_Note/ARMv8_note.assets/image-20210813162440767.png)

### PRACTICE Macros

PRACTICE macros are character sequences with a maximum size of 4KB. The character sequence is interpreted in the context where it is used. For a command, a PRACTICE macro can be interpreted e.g. as a number, boolean expression, parameter, or simply as a string. PRACTICE macros can be expanded to complete commands, too.

PRACTICE 宏是最大大小为4KB的字符序列。字符序列在使用它的上下文中进行解释。对于命令，PRACTICE 宏可以解释为数字、布尔表达式、参数或简单的字符串。PRACTICE 宏也可以扩展以完成命令。

Macro names in PRACTICE always start with an ampersand sign (‘&’), followed by a sequence of letters (az, A-Z), numbers (0-9), and the underscore sign (’_’). The first character after the & sign must not be a number. Macro names are case sensitive, so &a is different from &A.

实际上，宏名称总是以一个符号（“&”）开头，后跟一系列字母（az、a-Z）、数字（0-9）和下划线符号（“&”）。&符号后的第一个字符不能是数字。宏名称区分大小写，因此&a不同于&A。

Macro expansion does NOT take place inside the TRACE32 command line!

宏扩展不会在TRACE32命令行内进行！

PRACTICE macros can be declared as **GLOBAL** or **LOCAL** or **PRIVATE** macros.

![image-20210813163744888](C:/Users/10658/Desktop/WORK/ARMv8_Note/ARMv8_note.assets/image-20210813163744888.png)

#### GLOBAL Macros

PRACTICE macros declared with GLOBAL are accessible at every script level and have an unlimited lifetime.

使用全局声明的PRACTICE 宏在每个脚本级别都可以访问，并且具有无限的生存期。

如果将一个值分配给一个在PRACTICE 堆栈上尚不存在的宏，或者该宏是一个不可访问的私有宏，则该宏将被隐式创建为本地宏

## Parameter Passing

Parameters can be passed to a subroutine with a parameter list. The parameters are assigned to local PRACTICE macros, using the **ENTRY** command within the subroutine.
Subroutines can also be called up interactively by parameters. Arguments can be passed by the commands **DO, ENDDO, RUN, GOSUB, RETURN**. They can also be the result of calling a command extension or invoking the driver program on the host with arguments.

表达式中运算符前后的空格被解释为连续参数的分隔符。

![image-20210813165110660](C:/Users/10658/Desktop/WORK/ARMv8_Note/ARMv8_note.assets/image-20210813165110660.png)

# 