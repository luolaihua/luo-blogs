# GCC命令总结

# 一. 常用编译命令选项

假设源程序文件名为test.c。

## 1. 无选项编译链接

用法：#gcc test.c

作用：将test.c预处理、汇编、编译并链接形成可执行文件。这里未指定输出文件，默认输出为a.out。

## 2. 选项 -o

用法：#gcc test.c -o test

作用：将test.c预处理、汇编、编译并链接形成可执行文件test。-o选项用来指定输出文件的文件名。

## 3. 选项 -E

用法：#gcc -E test.c -o test.i

作用：将test.c预处理输出test.i文件。

## 4. 选项 -S
用法：#gcc -S test.i

作用：将预处理输出文件test.i汇编成test.s文件。

## 5. 选项 -c
用法：#gcc -c test.s

作用：将汇编输出文件test.s编译输出test.o文件。

## 6. 无选项链接
用法：#gcc test.o -o test

作用：将编译输出文件test.o链接成最终可执行文件test。

## 7. 选项-O
用法：#gcc -O1 test.c -o test

作用：使用编译优化级别1编译程序。级别为1~3，级别越大优化效果越好，但编译时间越长。

## 8. 选项 -Wall
-Wall选项

编译后显示所有警告。

## 9. -W选项

与-Wall类似，会显示警告，但是只显示 编译器认为 会 出现错误 的警告

## 10. -I选项（大写的i）

include头文件非标准库中存在的也不是在当前文件夹下的，需要将地址用-I包含

例：-I /home/src/

## 11. -g选项

添加gdb调试选项

## 12. -w选项（小写字母）

-w：关闭编译时的警告

解释：编译后不显示任何warning，因为有时在编译之后编译器会显示一些例如数据转换之类的警告，而这些警告是可以忽略的



# 二. 多源文件的编译方法

如果有多个源文件，基本上有两种编译方法：
[假设有两个源文件为test.c和testfun.c]

## 1. 多个文件一起编译
用法：#gcc testfun.c test.c -o test
作用：将testfun.c和test.c分别编译后链接成test可执行文件。

## 2. 分别编译各个源文件，之后对编译后输出的目标文件链接
用法：
#gcc -c testfun.c //将testfun.c编译成testfun.o
#gcc -c test.c   //将test.c编译成test.o
#gcc -o testfun.o test.o -o test //将testfun.o和test.o链接成test

以上两种方法相比较，第一中方法编译时需要所有文件重新编译，而第二种方法可以只重新编译修改的文件，未修改的文件不用重新编译。

参考链接：

https://www.cnblogs.com/ibyte/p/5828445.html

http://www.topabu.com/linux/gcc-compile.html