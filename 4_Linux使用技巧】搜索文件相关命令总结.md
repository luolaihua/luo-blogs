# 【Linux使用技巧】搜索文件相关命令总结

在Windows系统下可以使用文件管理器或者系统自带的搜索功能来搜索文件，也可以使用搜索软件[Everything](https://www.voidtools.com/zh-cn/) 进行查找。但是在Linux系统中，没有相关GUI软件，只能通过一些查找命令进行查找。

# 一般查找：find

关于find指令的详细用法可以参考[Linux Find 命令精通指南](https://www.oracle.com/cn/technical-resources/articles/linux-calish-find.html) 以及 [Linux find 命令](https://www.runoob.com/linux/linux-comm-find.html) 。本文只总结其常用方法。一般使用方法：

`find PATH -name FILENAME`  

上述命令的意义为：在PATH路径下查找名为FILENAME的文件，其中PATH如果省略，则默认从当前目录开始搜索。

**PATH**：要查找的目录路径。 

-    ~ 表示$HOME目录
- ​    **.** 表示当前目录
- ​    / 表示根目录 

除了-name，常用的查找方式有：

> -perm                                #按执行权限来查找
> -user    username             #按文件属主来查找
> -group groupname            #按组来查找
> -mtime   -n +n                   #按文件更改时间来查找文件，-n指n天以内，+n指n天以前
> -atime    -n +n                   #按文件访问时间来查找文件，-n指n天以内，+n指n天以前
> -ctime    -n +n                  #按文件创建时间来查找文件，-n指n天以内，+n指n天以前
> -nogroup                          #查无有效属组的文件，即文件的属组在/etc/groups中不存在
> -nouser                            #查无有效属主的文件，即文件的属主在/etc/passwd中不存
> -type    b/d/c/p/l/f             #查是块设备、目录、字符设备、管道、符号链接、普通文件
> -size      n[c]                    #查长度为n块[或n字节]的文件
> -mount                            #查文件时不跨越文件系统mount点
> -follow                            #如果遇到符号链接文件，就跟踪链接所指的文件
> -prune                            #忽略某个目录

在当前目录下查找data.txt文件，find命令会自动迭代搜索子目录：

`find . -name data.txt`  

此外还可以使用星号*进行模糊匹配：

查找当前目录下所有的txt文档，注意使用单引号将带有星号的文件名包含，或者使用反斜杠转义符\：

`find . -name '*.txt'` 

`find . -name \*.txt` 

不然会报错[paths must precede expression](https://www.cnblogs.com/peter1994/p/7297656.html) ：

![image-20220110213003794](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201102130594.png)

报错是因为星号被展开为当前目录下所有的文件，将*号打印，可以发现：

![image-20220110213138058](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201102131996.png)

查找以test开头的文件：

![image-20220110213531753](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201102218393.png)

同样需要将星号转义：

`find . -name 'test*'`

 在当前目录及子目录中，查找大写字母开头的txt文件 ：

`find . -name '[A-Z]*.txt' -print` 

此外，如果需要忽略文件名的大小写，可以将-name改成-iname。

# 数据库查找-locate

与find不同， locate命令依赖于一个数据库文件， Linux系统默认每天会检索一下系统中的所有文件， 然后将检索到的文件记录到数据库中。 在运行locate命令的时候可直接到数据库中查找记录并打印到屏幕上， 所以使用locate命令要比find命令反馈更为迅速。 在执行这个命令之前一般需要执行updatedb命令（这不是必须的， 因为系统每天会自动检索并更新数据库信息， 但是有时候会因为文件发生了变化而系统还没有再次更新而无法找到实际上确实存在的文件。 所以有时需要主动运行该命令， 以创建最新的文件列表数据库） ， 以及时更新数据库记录。【引用自 Linux系统命令及Shell脚本实践指南—王军】

![image-20220110221511829](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201102215963.png)

```
创建一个文件
[root@localhost ~]# touch test_locate
#用find命令查找
[root@localhost ~]# find / -name test_locate
/root/test_locate #
找到了
#再用locate找一下
[root@localhost ~]# locate test_locate
[root@localhost ~]# #
没找到！ 为什么？
#执行一下updatedb， 更新数据库
[root@localhost ~]# updatedb
[root@localhost ~]# locate test_locate
/root/test_locate #
找到了！ 说明由于没有更新数据库， 所以无法使用locate命令找到刚创建的文件
#将该文件删除
[root@localhost ~]# rm test_locate
rm: remove regular empty file 'test_locate'? y #
确认删除了
#再次locate， 但仍然可以找到
[root@localhost ~]# locate test_locate
/root/test_locate
#用updatedb再次更新一下
[root@localhost ~]# updatedb
[root@localhost ~]# locate test_locate
[root@localhost ~]# #
再找， 没有这个文件了
```

这个实验表明， locate命令依赖于其用于记录文件的数据库， 该数据库需要使用updatedb来更新。
当然， 系统每天也会自动运行一次， 但是不必等系统运行， 必要的时候可主动进行手动更新。  

