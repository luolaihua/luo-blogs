# 使用Gitee用作图片床写博客（Picgo+typora+Gitee）

[TOC]

# 问题描述

笔者习惯于使用markdown文件来写技术文章，使用的md工具为Typora，其中比较麻烦的一点是：md文件中的图片仅保存在本地，当md文件需要共享时，还需要把图片文件夹分享出去。所以需要一个图片床（图片服务器）将md中的图片在线保存。不仅如此，使用图片床的md文件还可以直接导入CSDN等博客网站中，图片不会丢失。

# 解决办法

大佬们普遍使用Picgo工具用于上传图片并获取链接：

![image-20220106184808952](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061848042.png)

![image-20220106184702894](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061847023.png)

PicGo的下载地址和说明文档：

> - Picgo最新版下载地址：https://github.com/Molunerfinn/PicGo/releases/latest
> - Picgo说明文档：https://picgo.github.io/PicGo-Doc/zh/guide/#%E7%89%B9%E8%89%B2%E5%8A%9F%E8%83%BD

目前最新版为2.3.0，windows用户选择exe文件下载即可：

![image-20220106185131726](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061851813.png)

Picgo支持多种图片床，其中常用且免费的是**github**和**gitee**，但是在国内github连接不稳定，所以还是推荐使用国产的gitee比较好：

![image-20220106185515708](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061855772.png)

# 配置教程

## 第一步：安装PicGo并在Typora中配置

PicGo2.3.0已经不需要设置图片床插件，可以直接使用图片床。将PicGo安装好后，在typora中配置即可：

打开Typora后，点击菜单栏->文件->偏好设置->图像设置:

![image-20220106190004943](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061900013.png)

在设置中配置好PicGo的安装路径即可。

## 第二步，在Gitee中创建图片仓库

gitee地址：https://gitee.com

### 1，新建仓库

![image-20220106190625449](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061906532.png)

### 2，生成私人令牌

在gitee的设置中找到**私人令牌**，并点击生成新令牌：

![image-20220106190929516](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061909586.png)

注意：**私人令牌只会显示一次，注意保存**。

![image-20220106191009816](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061910863.png)

# 在PicGo中配置Gitee图床

找到Gitee图床设置：

![image-20220106191157393](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061912516.png)

> - owner：所有者，写上你的码云账号名，如果你不知道你的账号名，进入你刚才的仓库，浏览器url里面有。
> - repo：仓库名称，只要写上仓库名称就行，比如我自己的仓库blogImage。
> - path：写上路径，一般是img，这几个项都不用加“ / “符号。
> - token：刚才你获取的个人令牌，两个插件是通用的，如果你用了另一个再来用这个，它会自动读取另一个插件的部分配置，不用重新申请。
> - message：不用填。

全部配置完成后，即可进行图片上传测试。

## 注意

截止至2022-3-20，在新版本的PicGo中，其图床设置中以及没有默认的Gitee图床：

![image-20220320154000682](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/image-20220320154000682.png)

所以需要在插件设置中搜索gitee的插件，并安装（需要提前安装node.js）：

![image-20220320154137580](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/image-20220320154137580.png)

# 运行测试

在PicGo的上传区中上传图片：

![image-20220106191426846](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061914920.png)

然后在gitee仓库中查看是否有图片上传成功：

![image-20220106191544068](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061915147.png)

如果图片可以上传成功，就可以使用typora新建一个md文件进行测试：

![image-20220106191742462](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061917567.png)

可以看到md文件中的图片地址，说明配置成功。

最后可以将md文件直接导入到CSDN博客中：

![image-20220106191937831](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/img/202201061919884.png)



参考文章：

https://zhuanlan.zhihu.com/p/355919389

https://blog.csdn.net/shdxhsq/article/details/119246183

https://zhuanlan.zhihu.com/p/178938338

https://blog.csdn.net/shdxhsq/article/details/119246183

https://zhuanlan.zhihu.com/p/178938338

