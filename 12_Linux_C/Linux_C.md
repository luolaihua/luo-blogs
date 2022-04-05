# ILP32和LP64
![](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs/20220404182622.png)

- **ILP32**这个缩写的意思是 int （I）、 long （L）和指针（P）类型都占32位，通常32位计算机的C编译器采用这种规范，x86平台的 gcc 也是如此。
- **LP64**是指 long （L）和指针占64位，通常64位计算机
的C编译器采用这种规范。
- 指针类型的长度总是和计算机的位数一致

![](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs/20220404183037.png)

```C
int a=0;
a = (++a)+(++a)+(++a)+(++a);
// a = 11
```

答案应该是Undefined。a = (++a)+(++a)+(++a)+(++a); 的结果之所以是Undefined，
因为在这个表达式中有五个Side Effect都在改变 a 的值，这些Side Effect按什么顺序发生不一定，只
知道在整个表达式求值结束时一定都发生了。比如现在求第二个 ++a 的值，这时第一个、第三个、
第四个 ++a 的Side Effect发生了没有， a 的值被加过几次了，这些都不确定，所以第二个 ++a 的值也
不确定。这行代码用不同平台的不同编译器来编译结果是不同的，甚至在同一平台上用同一编译器
的不同版本来编译也可能不同。

# Volitile关键字

有了 volatile 限定符，是可以防止编译器优化对设备寄存器的访问，但是对于有Cache的平台，仅
仅这样还不够，还是无法防止Cache优化对设备寄存器的访问。

用优化选项编译生成的指令明显效率更高，但使用不当会出错，为了避免编译器自作聪明，把不该
优化的也优化了，程序员应该明确告诉编译器哪些内存单元的访问是不能优化的，在C语言中可以
用 volatile 限定符修饰变量，就是告诉编译器，即使在编译时指定了优化选项，每次读这个变量仍
然要老老实实从内存读取，每次写这个变量也仍然要老老实实写回内存，不能省略任何步骤。

除了设备寄存器需要用 volatile 限定之外，当一个全局变量被同一进程中的多个控制流程访问时也
要用 volatile 限定，比如信号处理函数和多线程。

# 多文件编译链接

隐式声明的函数返回值类型都是 int ，由于我们调用这个函数时没有传任何参数，所以编译器认为这个隐式声明的参数类型是 void ，这样函数的参数和返回值类型都确定下来了，编译器根据这些信息为函数调用生成相应的指令。

```C
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

```C
#include<stdio.h>
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

![](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs/20220405172151.png)
由于编译器在处理函数调用代码时没有找到函数原型，只好根据函数调用代码做隐式声明，把这三个函数声明为：

```C
int push(char);
int pop(void);
int is_empty(void);
```

```C
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
这样编译器就不会报警告了。在这里 extern 关键字表示这个标识符具有External Linkage。External
Linkage的定义在上一章讲过，但现在应该更容易理解了， push 这个标识符具有External Linkage指
的是：如果把 main.c 和 stack.c 链接在一起，如果 push 在 main.c 和 stack.c 中都有声明（在 stack.c 中
的声明同时也是定义），那么这些声明指的是同一个函数，链接之后是同一个 GLOBAL 符号，代表同
一个地址。函数声明中的 extern 也可以省略不写，不写 extern 的函数声明也表示这个函数具
有External Linkage。