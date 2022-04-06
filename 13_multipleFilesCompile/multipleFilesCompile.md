
- [多文件编译链接与.h头文件包含规则](#多文件编译链接与h头文件包含规则)
  - [extern 和 static 关键字](#extern-和-static-关键字)
  - [使用头文件封装](#使用头文件封装)
    - [一，尖括号和双引号](#一尖括号和双引号)
    - [二，头文件路径查找](#二头文件路径查找)
    - [三，头文件重复包含](#三头文件重复包含)
    - [四，为什么要包含头文件而不是 .c 文件](#四为什么要包含头文件而不是-c-文件)

# 多文件编译链接与.h头文件包含规则

如下示例程序，stack.c中定义了一个栈，以及栈的一些简单功能函数：push()，pop()以及is_empty()等。main.c为程序主函数，主要测试了栈的这些功能。

```c
// stack.c
char stack[512];
int top = -1;
void push(char c)
{
    stack[++top] = c;
}

char pop(void)
{
    return stack[top--];
}

int is_empty(void)
{
    return top == -1;
}
```

```c
// main.c
#include<stdio.h>
int main(void)
{
    push('a');
    push('b');
    push('c');
    while(!is_empty())
        putchar(pop());
    putchar('\n');
    return 0;
}
```
在命令行中使用gcc进行编译：
```
$ gcc main.c stack.c -o main
```
也分可以多步编译：
```
$ gcc -c main.c
$ gcc -c stack.c
$ gcc main.o stack.o -o main
```
但是编译成功后会报如下警告，如果未报，可添加 -Wall 参数：
![](https://img-blog.csdnimg.cn/img_convert/1af359e1814685b32da1f3a165b5f031.png)
<pre><b>main.c:</b> In function ‘<b>main</b>’:
<b>main.c:14:5:</b> <font color="#75507B"><b>warning: </b></font>implicit declaration of function ‘<b>push</b>’ [<font color="#75507B"><b>-Wimplicit-function-declaration</b></font>]
   14 |     <font color="#75507B"><b>push</b></font>(&apos;a&apos;);
      |     <font color="#75507B"><b>^~~~</b></font>
<b>main.c:17:12:</b> <font color="#75507B"><b>warning: </b></font>implicit declaration of function ‘<b>is_empty</b>’ [<font color="#75507B"><b>-Wimplicit-function-declaration</b></font>]
   17 |     while(!<font color="#75507B"><b>is_empty</b></font>())
      |            <font color="#75507B"><b>^~~~~~~~</b></font>
<b>main.c:18:17:</b> <font color="#75507B"><b>warning: </b></font>implicit declaration of function ‘<b>pop</b>’; did you mean ‘<b>popen</b>’? [<font color="#75507B"><b>-Wimplicit-function-declaration</b></font>]
   18 |         putchar(<font color="#75507B"><b>pop</b></font>());
      |                 <font color="#75507B"><b>^~~</b></font>
      |                 <font color="#4E9A06">popen</font>
</pre>

警告中提到 push()，pop()以及is_empty()都是隐式声明的函数，这是因为这些函数在调用之前未经声明或者定义（或者其声明定义在其他源文件中），编译器在处理这些函数调用代码时没有找到函数原型，只好根据函数调用代码做隐式声明，进行逆推。

此外，隐式声明的函数返回值类型都默认为 **int** ，再根据调用当前函数时传入的参数类型来确定函数的参数类型 ，这样函数的参数和返回值类型都确定下来了，编译器根据这些信息为函数调用生成相应的指令。因此，编译器会把这三个函数声明为：
```c
int push(char);
int pop(void);
int is_empty(void);
```
## extern 和 static 关键字
可以使用extern关键字，在函数调用之前进行声明，这样编译器就不会报警告了。

在这里 extern 关键字表示这个标识符具有外部链接External Linkage。push 这个标识符具有External Linkage指的是：如果把 main.c 和 stack.c 链接在一起，如果 push 在 main.c 和 stack.c 中都有声明（在 stack.c 中的声明同时也是定义），那么这些声明指的是同一个函数，链接之后是同一个 GLOBAL 符号，代表同一个地址。函数声明中的 extern 也可以省略不写，不写 extern 的函数声明也表示这个函数具有External Linkage。

```c
#include<stdio.h>

//extern关键字告诉编译器，函数的定义在其他源文件中
extern void push(char);
extern char pop(void);
extern int is_empty(void);

int a, b = 1;

int main(void)
{
    push('a');
    push('b');
    push('c');
    while(!is_empty())
        putchar(pop());
    putchar('\n');
    return 0;
}
```

如果用 static 关键字修饰一个函数声明，则表示该标识符具有内部链接属性Internal Linkage，例如有以下两个程序文件：
```c
/* foo.c */
static void foo(void) {}
```
```c
/* main.c */
void foo(void);
int main(void) { foo(); return 0; }
```
编译链接在一起会出错：
```
$ gcc foo.c main.c
/tmp/ccRC2Yjn.o: In function `main':
main.c:(.text+0x12): undefined reference to `foo'
collect2: ld returned 1 exit status
```

通俗地来讲，static关键字具有文件作用域，上述程序中，在foo.c中使用static修饰了foo()函数，使得foo()函数只在foo.c文件中可见，对main.c文件不可见，所以在编译过程中找不到foo()函数的定义。

从编译链接的角度来分析：
>虽然在 foo.c 中定义了函数 foo ，但这个函数只具有内部链接属性Internal Linkage，只有在 foo.c 中多次声明才表示同一个函数，而在 main.c 中声明就不表示它了。如果把 foo.c 编译成目标文件，函数名 foo 在其中是一个 LOCAL 的符号，不参与链接过程，所以在链接时， main.c 中用到一个External Linkage的 foo 函数，链接器却找不到它的定义在哪儿，无法确定它的地址，也就无法做符号解析，只好报错。

凡是被多次声明的变量或函数，必须有且只有一个声明是定义，如果有多个定义，或者一个定义都没有，链接器就无法完成链接。

## 使用头文件封装

在上文中提到：在函数调用之前，需要有函数的定义或者声明，否则编译器就会根据函数的调用，自己推导出隐式声明的函数声明，其中函数的返回值默认为 int ，函数参数类型根据调用的实际输入参数确定。但是随着程序的源文件逐渐增多，如果每一个功能文件中都需要调用stack.c里面的函数，则需要在各个文件中重复写函数的声明。重复性的工作应该尽量避免，我们可以写一个stack.h的头文件，将函数的声明放入，需要用到stack.c里面的函数的源文件，只需包含该头文件即可：

```c
#ifndef _STACK_H
#define _STACK_H
void push(char);
char pop(void);
int is_empty(void);
#endif
```
这样在 main.c 中只需包含这个头文件就可以了，而不需要写三个函数声明：
```c
/* main.c */
#include <stdio.h>
#include "stack.h"
int main(void)
{
    push('a');
    push('b');
    push('c');
    while(!is_empty())
    putchar(pop());
    putchar('\n');
    return 0;
}

```

关于头文件，有以下问题需要注意：
### 一，尖括号和双引号

包含头文件，有尖括号和双引号之分，这也是一道基础性的C语言面试问题，读者可以做如下实验，包含头文件时全使用尖括号或者双引号，看看是否可以通用：

```c
//报错
#include<stack.h>
#include<stdio.h>
//正常运行
#include"stack.h"
#include"stdio.h"
```
通过实验可知，二者是不可通用的，尖括号有使用限制，不可以给自己定义的头文件使用尖括号包含,否则会出现如下错误：
<pre><b>main.c:7:9:</b> <font color="#CC0000"><b>fatal error: </b></font>stack.h: 没有那个文件或目录
    7 | #include<font color="#CC0000"><b>&lt;stack.h&gt;</b></font>
      |         <font color="#CC0000"><b>^~~~~~~~~</b></font>
compilation terminated.
</pre>
如果全使用双引号，则可以编译成功。

尖括号和双引号的区别如下：
- 对于用角括号包含的头文件， gcc 首先查找 -I 选项指定的目录，然后查找系统的头文件目录（通常是 /usr/include ，在我的系统上还包括 /usr/lib/gcc/x86_64-linux-gnu/9/include ）；
- 而对于用引号包含的头文件， gcc 首先查找包含头文件的 .c 文件所在的目录，然后查找 -I 选项指定的目录，然后查找系统的头文件目录。


### 二，头文件路径查找
当前的目录结构如下：
<pre><font color="#4E9A06"><b>luo@luo-X550JX</b></font>:<font color="#3465A4"><b>~/STUDY/Linux_C/ASM</b></font>$ tree
<font color="#3465A4"><b>.</b></font>
├── main3.c
├── main.c
├── stack.c
└── stack.h

0 directories, 4 files
</pre>
stack.h头文件和stack.c文件与main.c文件在同一个文件夹中。则可以用

 > gcc -c main.c 
 
 编译， gcc 会自动在 main.c 所在的目录中找到 stack.h 。假如把 stack.h 移到一个子目录:

 <pre><font color="#4E9A06"><b>luo@luo-X550JX</b></font>:<font color="#3465A4"><b>~/STUDY/Linux_C/ASM</b></font>$ tree
<font color="#3465A4"><b>.</b></font>
├── main3.c
├── main.c
└── <font color="#3465A4"><b>stack</b></font>
    ├── stack.c
    └── stack.h

1 directory, 4 files
</pre>

再次使用gcc -c main.c 编译则会找不到stack.h：

<pre><font color="#4E9A06"><b>luo@luo-X550JX</b></font>:<font color="#3465A4"><b>~/STUDY/Linux_C/ASM</b></font>$ gcc main.c -c
<b>main.c:7:9:</b> <font color="#CC0000"><b>fatal error: </b></font>stack.h: 没有那个文件或目录
    7 | #include<font color="#CC0000"><b>&quot;stack.h&quot;</b></font>
      |         <font color="#CC0000"><b>^~~~~~~~~</b></font>
compilation terminated.
</pre>

有两种解决办法：

一是使用gcc 的 -I参数指定路径，用 -I 选项告诉 gcc 头文件要到子目录 stack 里找。具体的写法如下：
```
# 写法1， 使用 -I[dir]格式，直接在I后面接路径名称
$ gcc main.c -c -Istack

# 写法2， 使用 -I [dir]格式，路径和-I分开写
$ gcc main.c -c -I ./stack/

# 编译链接
$ gcc main.c ./stack/stack.c -o main -I ./stack/

```
二是在 #include 预处理指示中可以使用相对路径，例如把上面的代码改成 #include "stack/stack.h" ，那么编译时就不需要加 -Istack 选项了，因为 gcc 会自动在 main.c 所在的目录中查找，而头文件相对于 main.c 所在目录的相对路径正是 stack/stack.h。

### 三，头文件重复包含
回到我们一开始写的头文件stack.h中，在 stack.h 中我们看到两个新的预处理指示 #ifndef STACK_H 和 #endif ，#ifndef是if not define的简写，意思是说，如果 STACK_H 这个宏没有定义过，那么就定义一个STACK_H宏，并且开始其他操作，如定义函数或变量，直到#endif这一行为止。如果在包含这个头文件时 STACK_H 这个宏已经定义过了，则直接跳过这段代码。
```c
#ifndef _STACK_H
#define _STACK_H
void push(char);
char pop(void);
int is_empty(void);
#endif
```
这是为了解决头文件重复包含，而导致的代码冗余，命名冲突，重复定义等一系列问题。假如 main.c 包含了两次 stack.h ：
```c
#include "stack.h"
#include "stack.h"
int main(void)
{
...
```
则第一次包含 stack.h 时并没有定义 STACK_H 这个宏，因此头文件的内容包含在预处理的输出结果中：
```c
#define STACK_H
extern void push(char);
extern char pop(void);
extern int is_empty(void);
#include "stack.h"
int main(void)
{
...
```

其中已经定义了这个宏，因此第二次再包含就相当于包含了一个空文件，这就避免了头文件的内容被重复包含。这种保护头文件的写法称为Header Guard，以后我们每写一个头文件都要加上Header Guard，宏定义名就用头文件名的大写形式，这是规范的做法。

在大规模的项目当中，头文件中包含头文件的问题很常见，这样重复包含的问题就很难被发现，虽然程序中的变量和函数可以被重复声明，这种情况下，程序还可以正常运行，但是重复包含头文件将会带来以下危害：

1. 一是使预处理的速度变慢，要处理很多本来不需要处理的头文件。
2. 二是头文件包含陷入死循环，如果有 foo.h 包含 bar.h ， bar.h 又包含 foo.h 的情况，预处理器就陷入死循环了（其实编译器都会规定一个包含层数的上限）。
3. 三是头文件里有些代码不允许重复出现，虽然变量和函数允许多次声明（只要不是多次定义
就行），但头文件里有些代码是不允许多次出现的，比如 typedef 类型定义和结构体Tag定义
等，在一个程序文件中只允许出现一次。

### 四，为什么要包含头文件而不是 .c 文件
先看示例程序和编译结果，本次实验有三个源文件，stack.c中定义了栈相关功能函数，foo.c和main.c中直接使用include包含了stack.c文件，来调用其中的函数：

```c
//stack.c
char stack[512];
int top = -1;
void push(char c)
{
    stack[++top] = c;
}

char pop(void)
{
    return stack[top--];
}

int is_empty(void)
{
    return top == -1;
}
```
```c
//foo.c
#include"stack/stack.c"

void foo()
{
    is_empty();
}

```
```c
//main.c
#include"stack/stack.c"
#include<stdio.h>
void foo();
int main(void)
{
    foo();
    push('a');
    push('b');
    push('c');
    while(!is_empty())
        putchar(pop());
    putchar('\n');
    return 0;
}
```
编译结果：
<pre><font color="#4E9A06"><b>luo@luo-X550JX</b></font>:<font color="#3465A4"><b>~/STUDY/Linux_C/ASM</b></font>$ gcc main.c foo.c -o main
/usr/bin/ld: /tmp/cc61cDKn.o:(.data+0x0): multiple definition of `top&apos;; /tmp/ccsld8Vm.o:(.data+0x0): first defined here
/usr/bin/ld: /tmp/cc61cDKn.o: in function `push&apos;:
foo.c:(.text+0x0): multiple definition of `push&apos;; /tmp/ccsld8Vm.o:main.c:(.text+0x0): first defined here
/usr/bin/ld: /tmp/cc61cDKn.o: in function `pop&apos;:
foo.c:(.text+0x35): multiple definition of `pop&apos;; /tmp/ccsld8Vm.o:main.c:(.text+0x35): first defined here
/usr/bin/ld: /tmp/cc61cDKn.o: in function `is_empty&apos;:
foo.c:(.text+0x5b): multiple definition of `is_empty&apos;; /tmp/ccsld8Vm.o:main.c:(.text+0x5b): first defined here
collect2: error: ld returned 1 exit status
</pre>

出现了重复定义的错误。原因在于直接include源文件stack.c，相当于把stack.c中关于变量和函数的相关定义也包含了进来，就相当于 push 、 pop 、 is_empty 这三个函数在 main.c 和 foo.c 中都有定义，那么 main.c 和 foo.c 就不能链接在一起了。如果采用包含头文件的办法，则是多次声明，一次定义，这三个函数在main.c和foo.c中声明了各声明了一次，只在 stack.c 中定义了一次，最后可以把 main.c 、 stack.c 、 foo.c 链接在一起。如下图所示：

![](https://img-blog.csdnimg.cn/img_convert/560e908d39ae7a262c7b4b24409a52d8.png)


参考文章：

> http://akaedu.github.io/book/
