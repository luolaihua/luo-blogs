### 和宏一样快的内联函数（ An Inline Function is As Fast As a Macro）

> 原文链接：https://gcc.gnu.org/onlinedocs/gcc-9.2.0/gcc/Inline.html#Inline

通过声明一个函数 内联，你可以使用 GCC 编译器更快地调用这个函数。GCC能实现这一点的一种方法是：将该函数的代码集成到其调用方的代码中。通过消除函数调用开销（建立调用、传递参数、跳转到函数代码并返回），来加速代码的执行; 

此外，如果函数有实参为常量，那么这些实参的已知值可能允许在编译时进行简化，因此并不需要包含所有内联函数的代码。内联函数会影响程序的代码量，并且这种影响是难以预测的; 根据具体情况，通过将函数内联，目标代码可能会变大或变小。你还可以在使用GCC编译时，尝试使用选项：`-finline-functions` ，将所有“足够简单”的函数集成到它们的调用方中。

GCC 实现了声明内联函数的三种不同语义：一种是` -std=gnu89 `或者是` -fgnu89-inline`，或者使用 `gnu_inline` 属性时，让所有内联声明中都存在。另一种是 `-std=c99, -std=gnu99` ，或者使用后一个C版本的选项(不包括`-fgnu89-inline`) ，第三种是在编译 C + + 时使用。

要声明一个函数为内联，可以在它的声明中使用 `inline` 关键字，如下所示:

```c
static inline int
inc (int *a)
{
  return (*a)++;
}
```

如果您正在编写一个头文件用以包含在 ISO C90程序中，需要使用 `__inline__`关键字， 而不是 `inline`。查看替代关键字。详情见 [Alternate Keywords](https://gcc.gnu.org/onlinedocs/gcc-9.2.0/gcc/Alternate-Keywords.html#Alternate-Keywords)。

这三种类型的内联在两个重要的情况下表现相似： 一是当内联关键字 `inline`被用于静态`static`函数时，就像上面的例子一样; 二是当一个函数首次声明时不使用内联关键字 `inline`，然后在定义时使用 `inline`，就像这样：

```c
extern int inc (int *a); //声明时未使用 inline 修饰 ，其中extern 关键字可以省略
inline int // 函数定义时却使用 inline
inc (int *a)
{
  return (*a)++;
}
```

在这两种常见情况下，除了程序运行速度之外，程序的行为与没有使用 `inline` 关键字的情况相同。

当一个函数既是内联`inline` 函数又是静态`static`函数时，如果所有对该函数的调用都集成到调用方中，并且函数的地址从未被使用，那么这个函数自己的汇编代码也将不会被引用。在这种情况下，除非指定选项  `-fkeep-inline-functions`，那么GCC 事实上并不会输出该函数的汇编代码。如果有一个非集成的调用，那么函数就会像在一般情况下一样，被编译成汇编代码。如果程序引用了它的地址，那么函数也必须被编译，因为它不能被内联。

> When a function is both inline and `static`, if all calls to the function are integrated into the caller, and the function’s address is never used, then the function’s own assembler code is never referenced. In this case, GCC does not actually output assembler code for the function, unless you specify the option -fkeep-inline-functions. If there is a nonintegrated call, then the function is compiled to assembler code as usual. The function must also be compiled as usual if the program refers to its address, because that cannot be inlined.

注意，函数定义中的某些用法可能使它不适合内联替换。这些用法包括: 可变参函数（variadic functions）、 alloca 的使用、计算 goto 的使用(参见标签为值)、非局部 goto 的使用、嵌套函数（nested functions）的使用、 `setjmp`的使用、  `__builtin_longjmp` 以及 `__builtin_return` or `__builtin_apply_args`的使用。当标记为 `inline` 的函数不能替换时，使用`-Winline` 会发出警告，并给出失败的原因。

根据 ISO C + + 的要求，GCC 认为在类(class)体内定义的成员函数(member functions)应该被标记为内联 `inline` ，即使它们没有显式地用内联 `inline` 关键字声明。用户可以使用 `-fno-default-inline`覆盖这个选项；详情见 [Options Controlling C++ Dialect](https://gcc.gnu.org/onlinedocs/gcc-9.2.0/gcc/C_002b_002b-Dialect-Options.html#C_002b_002b-Dialect-Options)。

在没有优化（optimizing ）的情况下，GCC 不会内联任何函数，除非你为函数指定`always _ inline`属性，像这样:

```c
/* Prototype.  */
inline void foo (const char) __attribute__((always_inline));
```

本节的其余部分是针对于 GNU C90的内联进行说明的。



When an inline function is not `static`, then the compiler must assume that there may be calls from other source files; since a global symbol can be defined only once in any program, the function must not be defined in the other source files, so the calls therein cannot be integrated. Therefore, a non-`static` inline function is always compiled on its own in the usual fashion.

当一个内联函数不是静态 `static`的，那么编译器必须假定其他源文件可能会调用这个函数；因为一个全局符号（global symbol ）在任何程序中只能被定义一次，所以函数不能在其他源文件中被定义，所以其中的调用不能被集成。因此，非静态内联函数总是以它自己惯有的方式编译。（不推荐使用非静态内联函数）

> Therefore, a non-`static` inline function is always compiled on its own in the usual fashion.

如果在函数定义中同时指定 `inline` 和 `extern`关键字，那么该定义仅用于内联。在任何情况下，函数都不是自己编译的，即使用户显式地引用它的地址也是如此。这样的地址将变成外部引用，就好像只声明了函数，而没有定义它一样。

这种 `inline` 和 `extern` 的组合几乎具有宏的效果。使用它的方法是：

将一个函数定义放在一个包含这些关键字的头文件中，并将该定义的另一个副本（不用 `inline` 和 `extern` 修饰）放在库文件中。头文件中的定义导致对函数的大多数调用被内联。如果该函数还有其他用法，那么将引用它们在库中的副本。

> This combination of `inline` and `extern` has almost the effect of a macro. The way to use it is to put a function definition in a header file with these keywords, and put another copy of the definition (lacking `inline` and `extern`) in a library file. The definition in the header file causes most calls to the function to be inlined. If any uses of the function remain, they refer to the single copy in the library.