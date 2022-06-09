

# Makefile使用过程中遇到的问题详解

# 问题1：如何指定makefile文件进行编译

默认情况下，`make`命令会在当前目录下按照以下顺序，搜索这三个文件：

1. GNUmakefile  
2. makefile  
3. Makefile  

比如，如果三个文件同时存在，则make会优先使用GNUmakefile，名为GNUmakefile的文件不存在，则会去找makefile ，最后才是Makefile。我们也可以自己定义makefile的文件名，比如myMake，但是在使用的时候就不能仅仅输入一条 `make`指令了，要指定其他文件作为makefile文件，可以使用如下三个选项：

```shell
make -f myMake
make --file=myMake
make --makefile=myMake
```

需要注意的是，make的执行目录为输入 `make`命令时的工作目录，与makefile的存储位置无关，指定其他位置的makefile文件只是将该文件加载进来，工作目录并没有改变。



# 问题2：Makefile中 = 和 := 的区别