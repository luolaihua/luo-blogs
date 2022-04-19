# ARM中的PMU(Performance Monitor Unit，性能监控单元)是什么

在ARMv8-A中，性能监控扩展是一种已经实现的**可选**的功能，但是ARM官方强烈建议在ARMv8-A的实现中，包含性能监控扩展的第三版，即PMUv3。注意，在ARMv8中并不支持PMUv3之前的版本。

性能监控单元一般由一下几部分组成：

- 一个64位的循环计数器（cycle counter)
- 多个事件计数器（event counter），每个计数器计数的事件是可编程的。ARMv8提供最多31个事件计数器的空间，实际的计数器的数量是IMPLEMENTATION DEFINED，并且它的说明包含一个识别机制。也就是说在不同的架构下，计数器的数量是不一样的，随着需求而变，比如在Cortex-A53中，只有5个事件计数器。（ARM 建议至少实现两个计数器，并且虚拟机管理程序至少为访客操作系统提供这么多计数器）
- 使能（enable）和重置（reset）计数器的控制；标记溢出（overflow）的控制；在溢出时使用中断的控制。

性能监控软件可以独立于事件计数器启用循环计数器。

被监控的事件（events）可以分成两类：

- 可能在许多微体系结构中保持一致的体系结构和微体系结构事件。
- 特定于实现的事件。

PMU架构使用事件号码（event number）来表示一个事件：

- 定义常见事件的事件编号，以便在许多体系结构和微体系结构中使用。作为最低要求，包含 PMUv3 的实现必须实现常见事件的子集。

常见事件（common events）有：

![](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220419213244911.png)

![image-20220419213348825](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs_pc0/image-20220419213348825.png)
并且为IMPLEMENTATION DEFINED  的事件保留较大的事件编号空间。

当实现包括性能监视器扩展时，ARMv8 将定义以下可能到性能监视器寄存器的接口：

- 系统寄存器接口。此接口是必需的。
- 外部调试接口，可选地支持内存映射访问。此接口是可选的。

一个操作系统可以使用系统寄存器访问计数器。这支持许多用途：

- 动态编译技术
- 能源管理

此外，如果需要，操作系统可以使应用程序软件能够访问计数器。这使应用程序能够通过细粒度（fine-grain   ）控制监视其自身的性能，而无需操作系统支持。例如，应用程序可能实现每个功能的性能监视。

在许多情况下，集成到实现中的性能监视功能对于应用程序和应用程序开发都很有价值。当操作系统不使用性能监视器本身时，ARM 建议操作系统使应用程序软件能够访问性能监视器。

从程序员的角度来看，PMU是一个方便的性能监控和调整工具。我们可以从这些PMU事件计数器中获得处理器状态，如循环，指令执行，分支切换，缓存未命中/命中，内存读/写等信息。

自 3.6 起，Linux 内核中增加了性能计数器支持。内核有一个名为 perf 的实用程序，用于查看 CPU PMU 事件统计信息。Perf 支持原始事件 ID 或命名事件。由于 CPU 的体系结构不同，内核中只有少数事件是通用定义的。与特定 CPU 体系结构相关的所有其他事件只能使用原始事件 ID 进行访问。





[How to Use Performance Monitor Unit(PMU) of 64-bit ARMv8-A in Linux](https://zhiyisun.github.io/2016/03/02/How-to-Use-Performance-Monitor-Unit-(PMU)-of-64-bit-ARMv8-A-in-Linux.html)

