# ILP32和LP64
![](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs/20220404182622.png)

- **ILP32**这个缩写的意思是 int （I）、 long （L）和指针（P）类型都占32位，通常32位计算机的C编译器采用这种规范，x86平台的 gcc 也是如此。
- **LP64**是指 long （L）和指针占64位，通常64位计算机
的C编译器采用这种规范。
- 指针类型的长度总是和计算机的位数一致

![](https://gitee.com/luo-san-pao/luo-blog-images/raw/master/imgs/20220404183037.png)

```C
int a=0;
a = (++a)+(++a)+(++a)+(++a);
// a = 11
```

答案应该是Undefined。a = (++a)+(++a)+(++a)+(++a); 的结果之所以是Undefined，
因为在这个表达式中有五个Side Effect都在改变 a 的值，这些Side Effect按什么顺序发生不一定，只
知道在整个表达式求值结束时一定都发生了。比如现在求第二个 ++a 的值，这时第一个、第三个、
第四个 ++a 的Side Effect发生了没有， a 的值被加过几次了，这些都不确定，所以第二个 ++a 的值也
不确定。这行代码用不同平台的不同编译器来编译结果是不同的，甚至在同一平台上用同一编译器
的不同版本来编译也可能不同。