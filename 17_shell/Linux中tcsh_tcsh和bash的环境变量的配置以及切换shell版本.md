# Linux中tcsh/tcsh和bash的环境变量的设置

@[toc]
## 一，前言

笔者最近在工作环境内使用`export`命令设置环境变量时，出现了：`export：Command not found.`的错误，经研究才发现Linux内支持多种Shell，比如sh、bash、csh、tcsh、ash。更改环境变量的命令在各种shell中有所不同，在笔者的工作环境中使用的shell为tcsh，并不支持`export`命令，所以才导致找不到命令的错误。通过使用 `echo $SHELL`,可查看当前环境所使用的shell类型：

![image-20220424125431133](https://img-blog.csdnimg.cn/img_convert/14f7f8b9f553fdc07817954377e5f2c6.png)

也可以通过 `cat`命令查看当前Linux系统存在的shell版本： `cat/etc/shells`

![image-20220424125630557](https://img-blog.csdnimg.cn/img_convert/6011ab7b2e3bec9dc51989d808d407bb.png)

在笔者的Ubuntu系统中，shell的版本较少：

![image-20220424125832701](https://img-blog.csdnimg.cn/img_convert/ff4b984cb82eb6165addb0814ecc7d30.png)

本着研究精神，笔者将对常用的tcsh和bash中关于环境变量的设置问题进行总结梳理。

## 二，tcsh/csh中设置环境变量：set和setenv

csh全称为 C shell，语法类似C语言，故有此名称，设计者为Bill Joy（vi编辑器也是此人开发的）。而tcsh则为csh的增强版，加入了命令补全功能，提供了更加强大的语法支持。

csh/tcsh有两种类型的变量：局部变量和环境变量

- 局域变量是在shell内部声明的

- 环境变量是全局域的变量

使用`set`来定义局部变量, 使用`setenv`可以定义环境变量，局部变量只对本shell有效, 不能传递给子shell，
但环境变量可传递给子shell， `setenv`有点类似于bash中`export`操作。它们二者的语法如下：

```bash
set varname = value; 
setenv varname2 valu2;
```

使用示例：

![image-20220424132221330](https://img-blog.csdnimg.cn/img_convert/7589ed2be985512cf81bad83005583bd.png)

此外，可以使用`printenv`命令打印出当前系统的所有环境变量：

![image-20220424133815287](https://img-blog.csdnimg.cn/img_convert/8352a42bfa9e338d81b0c571a062398e.png)

环境变量中，我们经常使用的是`PATH`环境变量，相关操作一般有如下三种：

1.  `setenv PATH "xxx/xxx/xx"`       								 #将PATH设置为"xxx/xxx/xx"
2.  `setenv PATH "${PATH}:/usr/local/sbin"`      *#追加*/usr/local/sbin到PATH中
3.  `setenv PATH "${PATH}:${HOME}/bin"` 	         *#追加*${HOME}/bin到PATH中

需要注意的是，在命令行中直接这样设置环境变量只对当前窗口有效，如果将当前窗口关闭，或者新开一个控制窗口，之前关于变量的设置将失效：

![image-20220424132627842](https://img-blog.csdnimg.cn/img_convert/9bbb2baf35deda55a6047b15129e53f1.png)

关于永久设置环境变量的操作，将在文章末尾说明。

## 三，bash中更改环境变量：export

bash shell 是 Linux 的默认 shell， 由 GNU 组织开发，保持了对 sh shell 的兼容性，是各种 Linux 发行版默认配置的 shell。由于bash的通用性和普及性，导致笔者一度认为shell 就是bash shell。

在bash中用于**设置或显示环境变量**的命令是`export`。 `export` 可新增，修改或删除环境变量，供后续执行的程序使用。和tcsh/csh中的`setenv`一样， `export` 的效力仅限于**该次登陆操作**，如果关闭该命令控制窗口，当前export的操作将失效。

1. `PATH=/etc` *#等于两边不能有空格*
2. `export PATH=$PATH:/xxx/xxx/bin` * #追加/xxx/xxx/bin*

语法：

```
export [-fnp][变量名称]=[变量设置值]
```

- -f 　代表[变量名称]中为函数名称。
- -n 　删除指定的变量。变量实际上并未删除，只是不会输出到后续指令的执行环境中。
- -p 　列出所有的shell赋予程序的环境变量

如下所示，使用`export -p`命令可以列出当前的环境变量值：

![image-20220424140251311](https://img-blog.csdnimg.cn/img_convert/4624b61bdad11e78382d3131a3e52bf2.png)

关于定义环境变量和复制操作：

```
export MYENV //定义环境变量
export MYENV=7 //定义环境变量并赋值
```

## 四，使用chsh命令更改当前使用的shell

查看当前环境所使用的shell是哪一种有很多种方法，这里列举两种：

![image-20220424140752168](https://img-blog.csdnimg.cn/img_convert/950efe1b98210774a9c90491eda7ad22.png)

一种是使用`env`命令，另一种是直接打印出`SHELL`。

如果想更改当前使用的shell，可以使用`chsh`命令：

```
名称
       chsh - change login shell

使用
       chsh [options] [LOGIN]

描述
      chsh 命令更改用户login shell程序。这将确定用户的初始登录命令的名称。普通用户只能为自己的帐户更改login shell;超级用户可以更改任何帐户的login shell。

选项
       适用于 chsh 命令的选项包括：
       -h, --help
           显示帮助消息并退出。
       -R, --root CHROOT_DIR
           在CHROOT_DIR目录中应用更改，并使用CHROOT_DIR目录中的配置文件。
       -s, --shell SHELL
           用户的新login shell的名称。将此字段设置为空会导致系统选择默认登录 shell。如果未选择 -s 选项，chsh 将以交互方式运行，提示用户使用当前登录 shell。输入新值以更改 shell，或将该行留空以使用当前值。当前外壳显示在一对 [ ] 标记之间。

注意事项
      对login shell的唯一限制是命令名称必须在 /etc/shells 中列出，除非调用者是超级用户，然后可以添加任何值。具有受限login shell的帐户不得更改其login shell。因此，不鼓励将 /bin/rsh 放在 /etc/shells 中，因为意外地更改为受限制的 shell 会阻止用户将其登录 shell 更改回其原始值。

相关文件
       /etc/passwd
           User account information.
       /etc/shells
           List of valid login shells.
       /etc/login.defs
           Shadow password suite configuration.

```



使用示例：

`chsh -s /bin/sh`

执行完退出重新登录，更改将生效。



## 五，关于永久更改环境变量的问题

上文中所述关于更改环境变量的命令操作都是一次性的，关闭当前命令窗口后将失效。用户可以通过修改一些配置文件达到永久修改环境变量的目的：

比如修改用户根目录下的`~/.bashrc`或`~/.tcshrc`文件：

```bash
#打开文件
vim ~/.bashrc
vim ~/.tcshrc

#在文件末尾加上
export PATH=$PATH:/.../...    
setenv PATH $PATH:/.../...  

#使设置生效
source ~/.bashrc
source ~/.tcshrc
```

关于具体的配置文件修改，可以参考：[Linux中profile、bashrc、~/.bash_profile、~/.bashrc、~/.bash_profile之间的区别和联系以及执行顺序](https://blog.csdn.net/gatieme/article/details/45064705)，这里就不多加赘述。

需要注意的是，需谨慎修改相关配置文件，笔者因为错误操作，曾导致修改.tcshrc文件后，所有命令全部失效，报`Command not found`的错误，想恢复.tcshrc文件中的修改，却发现连vim也打不开了，这时读者可以通过`/bin/vim`来打开vim编辑器：

```bash
/bin/vim ~/.tcshrc
```

将之前修改的环境变量删除，然后重启环境即可解决此问题。

> 参考文章：
>
> [几种常见的Shell：sh、bash、csh、tcsh、ash](http://c.biancheng.net/cpp/view/6995.html)
>
> [linux配置csh设置环境变量](https://blog.csdn.net/matchbox1234/article/details/107822693)
>
> [Linux之环境变量（永久设置）](https://www.jianshu.com/p/9e32a0f9999c)

