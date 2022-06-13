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

# 处理器访问类型Access Classes for Core Resources  

以下是一些处理器资源常用的缓存访问类型：

| IC   | Instruction Cache指令缓存                              |
| ---- | ------------------------------------------------------ |
| DC   | Data Cache数据缓存                                     |
| L2   | Level 2 Cache 二级缓存                                 |
| NC   | No Cache (access with caching inhibited)限制缓存的访问 |

比如下面这些指令

```
Data.dump DC:0x6770 ; 显示地址0x6770处的16进制数据转存，DC表面数据从Data cache上获得的
Data.dump NC:0x6770 ;NC表示不经过缓存，数据是从物理内存physical memory上读取的
```

# 访问类型属性Access Class Attributes  

| E    | 运行时访问，优先采用非侵入性访问，如果不支持，就是侵入性访问。 |
| ---- | ------------------------------------------------------------ |
| A    | 物理地址的访问，绕过MMU（MMU可以将虚拟地址和物理地址进行转换） |
| S    | Supervisor 内存，特权访问                                    |
| U    | 用户内存，非特权访问                                         |
| Z    | 安全访问（比如ARM的TrustZone）                               |
| N    | 非安全访问                                                   |

比如以下命令：

> Data.dump A:0x29876  
>
> 解释：dump物理地址为0x29876上的数据

> Data.dump AD:0x29876  
>
> 解释：D表示Data，代表数据内存，所以同上命令

> Data.dump ADC:0x29876  
>
> 解释：A同上，DC表示Data Cache，表示dump物理地址为0x29876上的数据，数据的来源为Data Cache

# 访问类型扩展

如果用户忽略指定访问类型，Trace32将根据经验进行填充，填充的规则基于：

- 当前CPU的上下文context（架构特有的）
- 使用的窗口类型（比如Data.dump是显示数据内存，List.Mix窗口是显示代码内存）
- 所加载应用的符号信息（比如代码和数据的结合）
- 使用不同的指令集的段segments
- 特殊的调试设置（比如SYStem.Option.*)

比如通过CPU访问，假设CPU处于非安全的supervisor模式，执行32bits代码。

![image-20220613224236044](Trace32%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B-%E8%AE%BF%E9%97%AE%E7%B1%BB%E5%9E%8B%EF%BC%88Access%20Class%EF%BC%89.assets/image-20220613224236044.png)

Trace32会自动将`A`扩展成 `ANSD`，将`Z`扩展成`ZSD`
