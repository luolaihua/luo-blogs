# Linux下使用gnome-terminal命令一键开启工作环境

# 前言

笔者的主力开发环境为Linux，工作中总会在不同路径下打开多个终端窗口（terminal），以及开启一些工具软件，每当一关机或者重启，又得重新一个一个开启工具软件，并且又要在特定的工作目录下打开之前被关闭的终端窗口。于是想着编写一个脚本，每次开机后运行，即可自动在指定工作目录下打开终端，以及开启一些软件。本文主要用到的指令为`gnome-terminal`。

# gnome-terminal使用指南

在Ubuntu中可以使用`man gnome-terminal`命令查看[gnome-terminal的简单使用指南](https://www.systutorials.com/docs/linux/man/1-gnome-terminal/)：

```bash
NAME
       gnome-terminal — 一个终端仿真应用.

概要
       gnome-terminal  [-e,  --command=STRING]   [-x, --execute ]  [--window-with-profile=PROFILENAME]  [--tab-with-profile=PROFILENAME]  [--window-with-profile-internal-id=PROFILEID]  [--tab-with-profile-internal-id=PROFILEID]  [--role=ROLE]  [--show-menubar]  [--hide-menubar]  [--geometry=GEOMETRY]  [--working-directory=DIRNAME]  [-?, --help]

选项
       -e, --command=STRING
                 在终端内执行此选项的参数。

       -x, --execute
                 在终端内执行命令行的其余部分。

       --window-with-profile=PROFILENAME
                 打开一个新窗口，其中包含具有给定配置文件的选项卡。 可以提供多个这些选项。

       --tab-with-profile=PROFILENAME
                 在具有给定配置文件的窗口中打开一个选项卡。可以提供多个这些选项，以打开多个选项卡 。

       --window-with-profile-internal-id=PROFILEID
                 打开一个新窗口，其中包含具有给定配置文件 ID 的选项卡。在内部用于保存会话。

       --tab-with-profile-internal-id=PROFILEID
                 在窗口中打开具有给定配置文件 ID 的选项卡。 在内部用于保存会话。

       --role=ROLE
                 为最后一次指定的窗口设置role;仅适用于一个窗口;可以为从命令行创建的每个窗口指定一次。
                 
       --show-menubar
                 打开最后指定的窗口的菜单栏;仅适用于一个窗口;可以为从命令行创建的每个窗口指定一次。

       --hide-menubar
                 关闭最后指定的窗口的菜单栏;仅适用于一个窗口;可以为从命令行创建的每个窗口指定一次。

       --geometry=GEOMETRY
                 指定窗口位置，每个要打开的窗口可以指定一次。

       --working-directory=DIRNAME
                 将终端的工作目录设置为 DIRNAME。

       -?, --help
                 显示帮助消息。

```

在Ubuntu的使用手册下，有关于gnome-terminal更详细的介绍，以下[指南针对Ubuntu22.04 LTS的gnome-terminal](http://manpages.ubuntu.com/manpages/jammy/en/man1/gnome-terminal.1.html)，Ubuntu20使用的gnome为gnome3，比如笔者的Ubuntu环境：

![image-20220514194254980](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220514194254980.png)

对其他版本的Gnome不一定支持。指南如下：

```bash
 gnome-terminal的参数选项：
 	   --help, -h
           显示所有选项的简要概述。

       --help-all
           详细显示所有选项。

       --help-gtk
           显示所有 GTK 选项。

       --help-terminal
           显示要在新终端选项卡或窗口之间进行选择的所有选项。

       --help-terminal-options
           显示用于更改终端属性的所有选项，无论它们位于单独的选项卡还是窗口中。

       --help-window-options
           显示用于更改包含终端的窗口属性的所有选项。

       --load-config=FILE
           通过从配置文件加载应用程序，将应用程序还原到以前保存的状态，配置文件无格式要求。
       --preferences
           显示首选项窗口。

       --print-environment, -p
           打印终端环境变量以与创建新的终端进行交互。

       --quiet, -q
           禁止诊断并创建新的终端

       --verbose, -v
           增加诊断周期并创建新的终端。

       --tab
           使用默认配置文件在最后打开的窗口中打开包含终端的新选项卡。相当于快捷键【CTRL+SHIFT+T】

       --window
           打开一个新窗口，包含一个选项卡，其中包含具有默认配置文件的终端。

       --command, -e=COMMAND
           以与 shell 相同的方式将此选项的参数拆分为程序和参数，并在终端内执行生成的命令行。
           这个选项已经过时了，可以使用 -- 来代替, 并在其后面写上程序和参数，比如：
           打开一个python3窗口，可以使用命令： 
           gnome-terminal -e "python3 -q"
           更推荐使用：
           gnome-terminal -- python3 -q
			需要注意的是，COMMAND并不是通过shell运行的，它会被拆分成一个个词，并像程序一样执行，如果			需要使用shell语法，可以使用如下形式：
           gnome-terminal -- sh -c '...'.

       --execute PROGRAM [ARGS], -x PROGRAM [ARGS]
           此时停止解析选项，并将所有后续选项解释为程序和参数，以便在终端内执行。
			这个选项已经过时了，可以使用 -- 来代替, 并在其后面写上程序和参数，比如：
           打开一个python3窗口，可以使用命令： 
           gnome-terminal -x python3 -q
           更推荐使用：
           gnome-terminal -- python3 -q

       --fd=FD
           转发文件描述符。

       --profile=PROFILE-NAME
           使用给定的配置文件而不是默认配置文件。

       --title, -t=TITLE
           设置初始终端标题。

       --wait
           等到终端的子项退出。

       --working-directory=DIRNAME
           设置终端的工作目录。

       --zoom=ZOOM
           设置终端的缩放系数。1.0 是正常大小。

       --active
           将最后指定的选项卡设置为其窗口中的活动选项卡。

       --full-screen
           全屏显示窗口。

       --geometry=GEOMETRY
           将窗口大小设置为 COLSxROWS+X+Y。例如，80x24 或 80x24+200+200。 

       --hide-menubar
           关闭窗口的菜单栏。

       --show-menubar
           打开窗口的菜单栏。

       --maximize
           最大化窗口。

       --role=ROLE
           设置 X 窗口的role。

       --class=CLASS
           窗口管理器使用的程序类。

       --display=DISPLAY
           X 窗口显示

       --g-fatal-warnings
           Make all warnings fatal.

       --gdk-debug=FLAGS
           要设置的 GDK 调试标志。

       --gdk-no-debug=FLAGS
           GDK debugging flags to unset.

       --gtk-debug=FLAGS
           GTK debugging flags to set.

       --gtk-no-debug=FLAGS
           GTK debugging flags to unset.

       --gtk-module=MODULES
           Load additional GTK modules.

       --name=NAME
           Program name as used by the window manager.

```

# gnome-terminal使用示例

在上个章节中介绍了gnome-terminal的使用指南，在本章节中将对这个命令做简单的使用举例，关于更详细的使用，还需读者自己摸索。

## 从配置文件中恢复终端

值得一提的是，gnome目前主要有gnome2和gnome3两个版本，两个版本直接还是有点差异的，比如关于窗口的配置文件选项，在gnome2中：

![gnome2](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220514204246201.png)

在gnome3中：

![image-20220514204357000](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220514204357000.png)

在gnome3中取消了终端配置文件保存的选项：`--save-config=FILE`，但却保留了加载终端配置文件的选项`--save-config=FILE`，这一操作直接让用户感到迷惑：配置文件从哪里来？怎么写这个配置文件？

![image-20220514204707011](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220514204707011.png)

幸好笔者手上有gnome2的环境，在gnome2下，将当前终端窗口的状态保存：`gnome-terminal --save-config=t.cfg`，这个配置文件格式无关紧要，也可以是个txt文件。以下是笔者从gnome2的环境下拷贝过来的终端配置文件，读者可以直接在gnome3环境下使用：

```bash
#GNOME Terminal 3.3.68

[GNOME Terminal Configuration]
Version=1
CompatVersion=1
FacttoryEnabled=true

#窗口配置，Windows0和Window1是要打开的窗口名字
Windows=Windows0;Window1;

#Windows0窗口配值
[Windows0]
Menubarvisible=true
Maximized=true
#当前终端位于Terminal1的选项卡
ActiveTerminal=Terminal1
Geometry=237x52+O+26
#当前终端窗口下有三个终端选项卡，分别为Terminal1，Terminal2，Terminal3;
#选项卡名字和数量可以自己设置
Terminals=Terminal1;Terminal2;Terminal3;

#Windows0下的Terminal1窗口配值
[Terminal1]
#打开Terminal1后要运行的命令，此处为运行一个test.sh的脚本
Command='/bin/sh' '-c' './test.sh'' && exec $SHELL -l'
#打开Terminal1后的工作目录
WorkingDirectory=/home/Documents
#缩放和窗口大小
zoom=1
width=237
Height=52

[Terminal2]
Command='/bin/sh' '-c' 'pwd'' && exec $SHELL -l'
WorkingDirectory=/home
zoom=1
width=237
Height=52

[Terminal3]
Command='/bin/sh' '-c' 'ls -la'' && exec $SHELL -l'
WorkingDirectory=/home
zoom=1
width=237
Height=52

[Windows1]
Menubarvisible=true
Maximized=true
ActiveTerminal=Terminal4
Geometry=237x52+O+26
Terminals=Terminal4;Terminal5;

[Terminal4]
WorkingDirectory=/home
zoom=1
width=237
Height=52
[Terminal5]
WorkingDirectory=/home
zoom=1
width=237
Height=52
```

在窗口配置文件中，可以设置一次性打开多少个终端窗口，每个终端窗口下终端选项卡的数量，以及打开终端需要运行的命令和工作目录。需要注意的是，命令的设置需要使用 `Command='/bin/sh' '-c' 'your command'' && exec $SHELL -l'`的形式，`your command`为用户自己设置的命令，如果不想设置某个属性，直接将其注释或删除即可。

## 使用shell脚本恢复终端

知道了`gnome-terminal`的使用方法，读者也可以自己编一个shell脚本，直接配置终端窗口。

比如我每次开机我想打开三个工作目录并运行一下命令（比如打开工作软件等），读者可写一个这样的脚本：

```shell
#!/bin/bash

dir1="/aaa/bbb/ccc/ddd/"
dir2="/ccc/ggg/ccc/ddd/"

gnome-terminal --window --working-directory=${dir1} --title='dir1' --command="bash -c pwd;bash" \
--tab \
--working-directory=${dir2} --title='dir2' --command="bash -c ls;bash" \
--tab \
#打开vscode
--working-directory=/home --title='run_eclipse' --command="bash -c code;bash"\

```

该脚本只使用了一个gnome-terminal命令，开启了一个终端窗口，终端窗口内有三个终端选项卡，每个选项卡都设置了运行不同的命令以及工作目录。

读者可以根据此脚本配置自己的一键恢复工作环境的脚本。



参考链接：

https://www.systutorials.com/docs/linux/man/1-gnome-terminal/

http://manpages.ubuntu.com/manpages/jammy/en/man1/gnome-terminal.1.html

http://www.linux-commands-examples.com/gnome-terminal