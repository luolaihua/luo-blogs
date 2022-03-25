# Makefile学习笔记

# 一，Makefile总述

## 1，Makefile的组成

Makefile主要有5部分组成：

1. **显示规则**。显示地指出要生成的目标文件，目标文件的依赖文件，以及生成该目标文件的命令。其中，**命令必须以[Tab]键开始**。
2. **隐晦规则**。make有自动推导功能，可以简略地书写Makefile
3. **变量的定义**。Makefile中的变量类似C语言中的宏。
4. **文件指示**。其中包含三部分：1，在一个Makefile中引用另一个Makefile；2，可以指定Makefile中的有效部分；3，定义一个多行的命令。
5. **注释**。Makefile中只有行注释，使用“#”号。

## 2，Makefile的文件名

make默认的文件名有三个，并且它们的识别顺序如下：

1. GNUmakefile
2. makefile
3. Makefile

此外，“GNUmakefile”是GNU识别的，最好不要用。最好使用“makefile”和“Makefile”  。根据识别顺序，如果“makefile”和“Makefile”同时存在，会优先使用 “makefile”。

此外，也可以指定其他文件名来书写Makefile。不过需要在使用make命令时，使用参数“-f”和“--file” 来指定Makefile文件，例如：

`make -f myMake`

## 3，引用其他Makefile

类似于C语言中的“#include”，Makefile中可以使用“include”关键字将别的Makefile包含进来，  



