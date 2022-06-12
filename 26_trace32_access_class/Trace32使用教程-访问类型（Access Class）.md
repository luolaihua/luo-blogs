# Trace32使用教程-访问类型（Access Class）

访问类型（Access Class）被 Trace32的PowerView用于指定访问内存、外设的寄存器、可寻址的core资源、协处理寄存器以及Trace32的虚拟内存等。

在Trace32中，寻址包括两部分：访问类型+地址，比如：

```
Data.Dump A:0x123456
```

其中 `A`为访问类型，`0x123456`为访问的地址，二者之间用冒号 `：`连接。

访问类型可以是：

- 程序内存类型（program memory class）
- 数据内存类型（ data memory class）

# 程序内存类型**Program Memory Classes**

通常使用字母 `P(Program)`来表示程序内存类型（可省略）,比如以下命令：

> List P:0x4568
>
> List 0x4568

`P`可以省略，上述两个命令都是在程序地址为 `0x4568`的地方，打开源代码窗口。

除了 `P`类型之外，还有 `R`, `T`和 `V`等程序内存类型，这些类型是处理器架构用来指定不同指令集的编码格式：

|  R   | 针对ARM架构，表示ARM指令集编码                               |
| :--: | ------------------------------------------------------------ |
|  T   | 针对ARM架构，表示THUMB指令集编码                             |
|  V   | 针对[POWER](https://baike.baidu.com/item/power/1199555)架构，表示VLE指令集编码 |

可用的程序内存类型取决于当前所使用的处理器架构，详细内容可以参考[Processor Architecture Manual](https://www2.lauterbach.com/pdf/main.pdf)。

# 数据内存类型Data Memory Classes  

通常使用字母 `D(Data)`来表示程序内存类型（可省略）,比如以下命令：

> Data.dump D:0x6770  
>
> Data.dump 0x6770  

`D`可以省略，所以上述两个命令都是同一个操作。

此外，对于一些特殊场景，还可以使用其他的字母来表示内存类型，比如 `X`表示针对MMDSP架构，使用 X总线来访问数据内存。

在Trace32中总是以如下的窗口显示`Data.dump`的信息：

![image-20220612224343142](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220612224343142.png)

比如其中修饰内存地址的 `SD`就代表“Supervisor Data ”。

如果访问类型被忽略，Trace32将会使用默认的访问类型。比如直接对内存地址 `0x40080000`进行 `Data.dump`,则可以发现默认使用了 `ZSD`的访问类型进行修饰，关于 `ZSD`代表何种类型，将在下文中解释。

![image-20220612225150494](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220612225150494.png)



![image-20220612223454360](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220612223454360.png)

| IC   |      |
| ---- | ---- |
| DC   |      |
| L2   |      |
| NC   |      |



**IC**  Instruction Cache

**DC** 

Data Cache

**L2** 

Level 2 Cache

**NC** 

No Cache (access with caching inhibited)

```
Data.dump D:0x6770 ; display a hex dump starting at
; Data address 0x6770
Data.dump X:0x6770 ; use X-Bus to access data memory
; MMDSP architecture
Data.dump 0x6770 ; the default access class for a
; hex dump is the data memory
; class
```



