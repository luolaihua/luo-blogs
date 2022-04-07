# C/C++预处理过程的详细梳理（宏定义+条件预处理+其它预处理）

- [C/C++预处理过程的详细梳理（宏定义+条件预处理+其它预处理）](#cc预处理过程的详细梳理宏定义条件预处理其它预处理)
- [1 预处理的步骤](#1-预处理的步骤)
  - [1.1 把源代码中出现的字符映射到源字符集](#11-把源代码中出现的字符映射到源字符集)
  - [1.2 将多个**物理行**替换成一个**逻辑行**](#12-将多个物理行替换成一个逻辑行)
  - [1.3 将注释替换为空格](#13-将注释替换为空格)
  - [1.4 将**逻辑行**划分成预处理记号（Token）和空白字符](#14-将逻辑行划分成预处理记号token和空白字符)
  - [1.5 宏展开，处理#include预处理指示](#15-宏展开处理include预处理指示)
  - [1.6 将转义序列替换](#16-将转义序列替换)
  - [1.7 连接相邻字符串](#17-连接相邻字符串)
  - [1.8 丢弃空白字符，如空格和Tab等](#18-丢弃空白字符如空格和tab等)
- [2 宏定义](#2-宏定义)
  - [2.1 变量宏定义和函数宏定义：#define](#21-变量宏定义和函数宏定义define)
- [文件包含：#include](#文件包含include)
- [#undef指令](#undef指令)
- [条件编译](#条件编译)
- [预定义宏](#预定义宏)
- [泛型选择](#泛型选择)
- [内联函数（C99）](#内联函数c99)



C预处理器在程序执行之前查看程序，根据程序中的预处理指令，预处理器把符号缩写替换成其表示的内容。基本上它的工作就是**文本替换**。

# 1 预处理的步骤

## 1.1 把源代码中出现的字符映射到源字符集

字符常量要用单引号括起来，例如 '}' ，注意单引号只能括一个字符而不能像双引号那样括一串字符，字符常量也可以是一个转义序列，例如 '\n' ，这时虽然单引号括了两个字符，但实际上只表示一个字符。和字符串字面值中使用转义序列有一点区别，如果在字符常量中要表示双引号"和问号?，既可以使用转义序列 \" 和 \? ，也可以直接用字符"和?，而要表示'和\则必须使用转义序列。C语言规定了一些三连符（Trigraph），在某些特殊的终端上缺少某些字符，需要用Trigraph输入，例如用 ??= 表示#字符。预处理首先就是将这些三连符替换成相应的单字符。

## 1.2 将多个**物理行**替换成一个**逻辑行**
把用 \ 字符续行的多行代码接成一行。定位每个反斜杠后面跟着的换行符实例，并删除它们，这种续行的写法要求 \ 后面紧跟换行，中间不能有其它空白字符。例如：
```c
//两个物理行
printf("That is wond\
		erful!\n");
//转换成一个逻辑行：
printf("That is wonderful!\n");

#define STR "hello, "\
                "world" //world前面的是tab

//会变成如下形式
#define STR "hello, "       "world"
```

## 1.3 将注释替换为空格

编译器将用一个空格字符替换每一条注释，不管是单行注释还是多行注释都替换成一个空格。

```c
int/*这看起来并不是空格*/fox;
//会变成：
int fox;
```

## 1.4 将**逻辑行**划分成预处理记号（Token）和空白字符

预处理Token包括标识符、整数常量、浮点数常量、字符常量、字符串、运算符和其它符号。继续上面的例子，两个源代码行被接成一个逻辑代码行，然后这个逻辑代码行被划分成Token和空白字符（+号为方便描述所加）： 
> #+ define + 空格 + STR + 空格 + "hello+ " + Tab + Tab + "world"

## 1.5 宏展开，处理#include预处理指示

如果遇到 #include预处理指示，则把相应的源文件包含进来，并对源文件做以上1-4步预处理。如果遇到宏定义则做宏展开。

## 1.6 将转义序列替换

找出字符常量或字符串中的转义序列，用相应的字节来替换它，比如把 \n 替换成字节0x0a。

## 1.7 连接相邻字符串

比如有如下代码：
```c
printf(
        STR);
```
经过第四步逻辑行处理后，可得到以下Token：
> printf + ( + 换行 + Tab + STR + ) + ; + 换行

再经过第五步宏展开，可得：
> printf + ( + 换行 + Tab + "hello, " + Tab + Tab + "world" + ) + ; + 换行

然后把相邻的字符串连接起来，其中"hello, " 和 "world"两个字符串可以连接在一起，最后结果为：
> printf + ( + 换行 + Tab + "hello, " + "world" + ) + ; + 换行

## 1.8 丢弃空白字符，如空格和Tab等

经过以上处理之后，把空白字符丢掉，把Token交给C编译器做语法解析，这时就不再是预处
理Token，而称为C Token了。这里丢掉的空白字符包括
> 空格、换行、水平Tab、垂直Tab、分页符。

继续上面的例子，最后交给C编译器做语法解析的Token是：

>printf + ( + "hello,world" + ) + ; 

**注意，把一个预处理指示写成多行要用 \ 续行，因为根据定义，一条预处理指示只
能由一个逻辑代码行组成，而把C代码写成多行则不需要用 \ 续行，因为换行在C代码中只不过是一种空白字符，在做语法解析时所有空白字符都已经丢掉了。**

现在我们可以给出预处理指示的严格定义：

> 一条预处理指示由一个逻辑代码行组成，以 # 开头，后面跟若干个预处理Token，在预处理指示中允许使用的空白字符只有空格和Tab。

# 2 宏定义

## 2.1 变量宏定义和函数宏定义：#define
使用#define来定义**明示常量**，也叫**符号常量**。预处理器指令从#开始运行，到后面的第一个换行符为止，也就是说指令的长度仅限于一行（逻辑行）。
示例程序1：

```c
// main1.c
#include<stdio.h>
#define TWO 2
#define OW "This is a\
    test.have a try" //反斜杠把该定义延续到下一行
#define FOUR TWO*TWO //预处理不做计算，只是简单替换 
#define PX printf("X is %d.\n",x)
#define FMT "X is %d.\n"
 
//在#define中使用参数--类函数宏，圆括号中可以有一个或多个参数。
#define SQUARE(X) X*X
#define PR(X) printf("The result is %d.\n",X);
 
//预处理粘合剂：##运算符 ,下面会介绍
#define XNAME(n) x ## n
#define PRINT_XN(n) printf("x" #n " = %d\n", x ## n); 

int main(void)
{
	int x = TWO;
	
	PX;
	x = FOUR;
	printf(FMT,x);
	printf("%s\n",OW);
	printf("TWO:OW\n");
	
	x = SQUARE(x);
	PR(x);
	
	//宏定义只是简单替换，
	//这里变成：printf("The result is %d.\n", x + 2 * x + 2);  16+2*16+2==50	
	PR(SQUARE(x + 2));
	
	//这里变成：printf("The result is %d.\n", x++ * x++);  16*17==272	
	PR(SQUARE(x++));
	
	//##运算符
	int XNAME(1) = 14; //变成 int x1 = 14；
	int XNAME(2) = 20; //变成 int x2 = 20;
	int x3 = 30;
	PRINT_XN(1);       //变成 printf("x1 = %d\n", x1); 
	PRINT_XN(2);       //变成 printf("x2 = %d\n", x2); 
	PRINT_XN(3);       //变成 printf("x3 = %d\n", x3); 
	return 0;	
} 
/*
结果： 
	X is 2.
	X is 4.
	This is a       test.have a try
	TWO:OW
	The result is 16.
	The result is 50. 
	The result is 272.
	x1 = 14
	x2 = 20
	x3 = 30
*/
```
在命令行中可以使用如下两个命令,对main1.c程序进行预处理:
> gcc -E main1.c
> 
> cpp main1.c

得到的结果如下:
```c
int main(void)
{
 int x = 2;

 printf("X is %d.\n",x);
 x = 2*2;
 printf("X is %d.\n",x);
 printf("%s\n","This is a    test.have a try");
 printf("TWO:OW\n");

 x = x*x;
 printf("The result is %d.\n",x);;



 printf("The result is %d.\n",x + 2*x + 2);;


 printf("The result is %d.\n",x++*x++);;


 int x1 = 14;
 int x2 = 20;
 int x3 = 30;
 printf("x" "1" " = %d\n", x1);;
 printf("x" "2" " = %d\n", x2);;
 printf("x" "3" " = %d\n", x3);;
 return 0;
}
```
下图为经过预处理之后的代码与原始的程序的代码对比图:
![](https://s3.bmp.ovh/imgs/2022/04/07/771b1e8a3f3ed692.png)

关于函数宏定义的注意事项可以参考博客:
https://blog.csdn.net/luolaihua2018/article/details/123935238

总结来说,函数式宏定义和真正的函数有以下不同点:

1. 宏定义的参数没有类型, 


















#  文件包含：#include
当预处理器发现#include时，会查看后面的文件名，并把文件的内容包含到当前文件中，即替换源文件中的#include指令。
#  #undef指令
#undef指令用于取消已定义的#define指令
假如有如下定义：
```c
#define LIMIT 100
```
然后又有如下指令：
```c
#undef LIMIT
```
将移除上面的定义，可以将LIMIT重新定义一个新值，即使原来没有定义LIMIT，取消LIMIT定义仍然有效，如果想使用一个名称，又不确定之前是否用过，为了安全起见，可以使用#undef指令取消改名字的定义。

#  条件编译
可以使用这些指令告诉编译器根据编译时的条件执行或忽略代码块。

```c
#include<stdio.h>
#define TEST 
#ifdef TEST        //如果已经用#define定义了MAVIS，则执行下面指令 
	#include "string.h"
	#define NUM 999
#else              //否则 
	#include "math.h"
	#define NUM 666
#endif             //条件结束，必须以#endif结尾 

int main(void)
{
	#ifdef TEST
		printf("this is a test: %d\n",NUM);
	#endif
	
	#ifndef SIZE   //#ifndef 和#ifdef指令的用法类似，不过它的意思相反，如果未定义SIZE，则执行下面代码段 
		#define SIZE 2
		puts("size is not defined!");
		printf("size = %d\n", SIZE);
	#endif 
	
	// #if指令很像C语言中的if
	#if SIZE == 1
		puts("size == 1");
	#elif SIZE == 2
		puts("size == 2");
	#else
		puts("size == 0");	
	#endif 
	
	/*较新的编译器提供另一种方法测试名称是否定义
		即，用#if defined (SIZE) 来代替 #ifdef VAX 
	*/
	#if defined (SIZE)
		puts("size!!!");
	#endif 
	return 0;
	/*
	结果： 
		this is a test: 999
		size is not defined!
		size = 2
		size == 2
		size!!!
	*/
}
```
#  预定义宏

```c
#include<stdio.h>
void why_me();

int main(void)
{
	printf("The file is %s.\n", __FILE__);//当前源代码文件名的字符串字面量 
	printf("The date is %s.\n", __DATE__);//预处理的日期 
	printf("The time is %s.\n", __TIME__);//翻译代码的时间 
	//printf("The version is %ld.\n", __STDC_VERSION__);
	printf("This is line %d.\n", __LINE__);// 当前源代码所在的行号 
	printf("This function is %s,\n", __func__);//预定义标识符，不是预定义宏，当前所在函数的函数名称 
	
	why_me();
	
	return 0;	
} 

void why_me(){
	printf("This function is %s\n", __func__);
	printf("This is line %d\n", __LINE__);
}
/*
结果： 
	The file is C:\Users\LUO\Desktop\C\code-train\predef.c.
	The date is Sep 24 2020.
	The time is 20:14:14.
	This is line 10.
	This function is main,
	This function is why_me
	This is line 20
*/
```
#  泛型选择
在程序设计中，**泛型编程**指那些没有特定类型，但一旦指定一种类型，既可以转换成指定类型的代码。C++在模板中可以创建泛型算法，然后编译器根据指定的类型自动使用实例化代码。C11新增了一种表达式，叫作**泛型选择表达式**，可根据表达式的类型选择一个值。
```c
-Generic(x, int: 0,float: 1, double: 2, default: 3)
```
_Generic是C11的关键字，第一个项是一个表达式，后面每个项都由一个类型、一个冒号和一个值组成。

```c
#include<stdio.h>

#define MYTYPE(X) _Generic((X),int:"data is int",float:"data is float",double:"data is double",default:"other")

int main(void)
{
	int d = 4;
	
	printf("%s\n", MYTYPE(d)); //d是int类型, MYTYPE(4)得”int” 
	printf("%s\n", MYTYPE(d*2.0)); //d*2.0是double类型，, MYTYPE(8.0)得”double”  
	printf("%s\n", MYTYPE(3L)); //3L是long类型, MYTYPE(3L)得”other”
	printf("%s\n", MYTYPE(&d)); //&d是int *类型, MYTYPE(&d)得”other”
	
	return 0;
}
/*
结果： 
	data is int
	data is double
	other
	other
	
*/
```

#  内联函数（C99）
通常函数的调用都有一定的开销，因为函数的调用包括建立调用、传递参数、跳转到函数代码并返回。内联函数就是**以空间换时间**，使函数的调用更加快捷。
标准规定：**具有内部链接的函数可以成为内联函数**，还规定了**内联函数的定义与调用该函数的代码必须在同一个文件中。**因此最简单的办法是使用**inline**和**static**修饰。通常，内联函数应定义在首次使用它的文件中，所以内联函数也相当于函数原型。
```c
#include<stdio.h>
inline static void test()
{
	puts("test!");
}
int main()
{
	...
	test();
	...
}
```
- 由于并未给内联函数预留单独的代码块，所以无法获得内联函数的地址，另外，内联函数无法在调试器中显示。
- 由于内联函数具有内部链接，所以在多个文件中定义同一个内联函数不会产生什么影响。
- 如果多个文件都需要使用同一个内联函数，可以将它定义在h头文件中。


