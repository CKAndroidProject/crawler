> 原文链接: https://www.anquanke.com//post/id/86416 


# 【系列分享】ARM 汇编基础速成5：连续存取


                                阅读量   
                                **141030**
                            
                        |
                        
                                                            评论
                                <b>
                                    <a target="_blank">1</a>
                                </b>
                                                                                                                                    ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)
                                                                                            



##### 译文声明

本文是翻译文章，文章原作者，文章来源：azeria-labs.com
                                <br>原文地址：[https://azeria-labs.com/load-and-store-multiple-part-5/](https://azeria-labs.com/load-and-store-multiple-part-5/)

译文仅供参考，具体内容表达以及含义原文为准

****

[![](https://p1.ssl.qhimg.com/t01085ce486c2c7d104.png)](https://p1.ssl.qhimg.com/t01085ce486c2c7d104.png)

译者：[arnow117](http://bobao.360.cn/member/contribute?uid=941579989)

预估稿费：140RMB

投稿方式：发送邮件至linwei#360.cn，或登陆网页版在线投稿

<br>

传送门

[【系列分享】ARM 汇编基础速成1：ARM汇编以及汇编语言基础介绍](http://bobao.360.cn/learning/detail/4070.html)

[【系列分享】ARM 汇编基础速成2：ARM汇编中的数据类型](http://bobao.360.cn/learning/detail/4075.html)

[【系列分享】ARM 汇编基础速成3：ARM模式与THUMB模式](http://bobao.360.cn/learning/detail/4082.html)

[**【系列分享】ARM 汇编基础速成4：ARM汇编内存访问相关指令**](http://bobao.360.cn/learning/detail/4087.html)

**<br>**

**连续加载/存储**

有时连续加载(存储)会显得更加高效。因为我们可以使用LDM(load multiple)以及STM(store multiple)。这些指令基于起始地址的不同，有不同的形式。下面是我们会在这一节用到的相关代码。在下文中会详细讲解。



```
.data
array_buff:
 .word 0x00000000             /* array_buff[0] */
 .word 0x00000000             /* array_buff[1] */
 .word 0x00000000             /* array_buff[2]. 这一项存的是指向array_buff+8的指针 */
 .word 0x00000000             /* array_buff[3] */
 .word 0x00000000             /* array_buff[4] */
.text
.global main
main:
 adr r0, words+12             /* words[3]的地址 -&gt; r0 */
 ldr r1, array_buff_bridge    /* array_buff[0]的地址 -&gt; r1 */
 ldr r2, array_buff_bridge+4  /* array_buff[2]的地址 -&gt; r2 */
 ldm r0, `{`r4,r5`}`              /* words[3] -&gt; r4 = 0x03; words[4] -&gt; r5 = 0x04 */
 stm r1, `{`r4,r5`}`              /* r4 -&gt; array_buff[0] = 0x03; r5 -&gt; array_buff[1] = 0x04 */
 ldmia r0, `{`r4-r6`}`            /* words[3] -&gt; r4 = 0x03, words[4] -&gt; r5 = 0x04; words[5] -&gt; r6 = 0x05; */
 stmia r1, `{`r4-r6`}`            /* r4 -&gt; array_buff[0] = 0x03; r5 -&gt; array_buff[1] = 0x04; r6 -&gt; array_buff[2] = 0x05 */
 ldmib r0, `{`r4-r6`}`            /* words[4] -&gt; r4 = 0x04; words[5] -&gt; r5 = 0x05; words[6] -&gt; r6 = 0x06 */
 stmib r1, `{`r4-r6`}`            /* r4 -&gt; array_buff[1] = 0x04; r5 -&gt; array_buff[2] = 0x05; r6 -&gt; array_buff[3] = 0x06 */
 ldmda r0, `{`r4-r6`}`            /* words[3] -&gt; r6 = 0x03; words[2] -&gt; r5 = 0x02; words[1] -&gt; r4 = 0x01 */
 ldmdb r0, `{`r4-r6`}`            /* words[2] -&gt; r6 = 0x02; words[1] -&gt; r5 = 0x01; words[0] -&gt; r4 = 0x00 */
 stmda r2, `{`r4-r6`}`            /* r6 -&gt; array_buff[2] = 0x02; r5 -&gt; array_buff[1] = 0x01; r4 -&gt; array_buff[0] = 0x00 */
 stmdb r2, `{`r4-r5`}`            /* r5 -&gt; array_buff[1] = 0x01; r4 -&gt; array_buff[0] = 0x00; */
 bx lr
words:
 .word 0x00000000             /* words[0] */
 .word 0x00000001             /* words[1] */
 .word 0x00000002             /* words[2] */
 .word 0x00000003             /* words[3] */
 .word 0x00000004             /* words[4] */
 .word 0x00000005             /* words[5] */
 .word 0x00000006             /* words[6] */
array_buff_bridge:
 .word array_buff             /* array_buff的地址*/
 .word array_buff+8           /* array_buff[2]的地址 */
```

在开始前，再深化一个概念，就是.word标识是对内存中长度为32位的数据块作引用。这对于理解代码中的偏移量很重要。所以程序中由.data段组成的数据，内存中会申请一个长度为5的4字节数组array_buff。我们的所有内存存储操作，都是针对这段内存中的数据段做读写的。而.text端包含着我们对内存操作的代码以及只读的两个标签，一个标签是含有七个元素的数组，另一个是为了链接.text段和.data段所存在的对于array_buff的引用。下面就开始一行行的分析了！

```
adr r0, words+12             /* words[3]的地址 -&gt; r0 */
```

我们用ADR指令来获得words[3]的地址，并存到R0中。我们选了一个中间的位置是因为一会要做向前以及向后的操作。



```
gef&gt; break _start 
gef&gt; run
gef&gt; nexti
```

R0当前就存着words[3]的地址了，也就是0x80B8。也就是说，我们的数组word[0]的地址是:0x80AC(0x80B8-0XC)。



```
gef&gt; x/7w 0x00080AC
0x80ac &lt;words&gt;: 0x00000000 0x00000001 0x00000002 0x00000003
0x80bc &lt;words+16&gt;: 0x00000004 0x00000005 0x00000006
```

接下来我们把R1和R2指向array_buff[0]以及array_buff[2]。在获取了这些指针后，我们就可以操作这个数组了。



```
ldr r1, array_buff_bridge    /* array_buff[0]的地址 -&gt; r1 */
ldr r2, array_buff_bridge+4  /* array_buff[2]的地址 -&gt; r2 */
```

执行完上面这两条指令后，R1和R2的变化。



```
gef&gt; info register r1 r2
r1      0x100d0     65744
r2      0x100d8     65752
```

下一条LDM指令从R0指向的内存中加载了两个字的数据。因为R0指向words[3]的起始处，所以words[3]的值赋给R4，words[4]的值赋给R5。

```
ldm r0, `{`r4,r5`}`              /* words[3] -&gt; r4 = 0x03; words[4] -&gt; r5 = 0x04 */
```

所以我们用一条指令加载了两个数据块，并且放到了R4和R5中。



```
gef&gt; info registers r4 r5
r4      0x3      3
r5      0x4      4
```

看上去不错，再来看看STM指令。STM指令将R4与R5中的值0x3和0x4存储到R1指向的内存中。这里R1指向的是array_buff[0]，也就是说 array_buff[0] = 0x00000003以及array_buff[1] = 0x00000004。如不特定指定，LDM与STM指令操作的最小单位都是一个字(四字节)。

```
stm r1, `{`r4,r5`}`              /* r4 -&gt; array_buff[0] = 0x03; r5 -&gt; array_buff[1] = 0x04 */
```

值0x3与0x4被存储到了R1指向的地方0x100D0以及0x100D4。



```
gef&gt; x/2w 0x000100D0
0x100d0 &lt;array_buff&gt;:  0x00000003   0x00000004
```

之前说过LDM和STM有多种形式。不同形式的扩展字符和含义都不同：



```
IA(increase after)
IB(increase before)
DA(decrease after)
DB(decrease before)
```

这些扩展划分的主要依据是，作为源地址或者目的地址的指针是在访问内存前增减，还是访问内存后增减。以及，LDM与LDMIA功能相同，都是在加载操作完成后访问对地址增加的。通过这种方式，我们可以序列化的向前或者向后从一个指针指向的内存加载数据到寄存器，或者存放数据到内存。如下示意代码 。



```
ldmia r0, `{`r4-r6`}` /* words[3] -&gt; r4 = 0x03, words[4] -&gt; r5 = 0x04; words[5] -&gt; r6 = 0x05; */ 
stmia r1, `{`r4-r6`}` /* r4 -&gt; array_buff[0] = 0x03; r5 -&gt; array_buff[1] = 0x04; r6 -&gt; array_buff[2] = 0x05 */
```

在执行完这两条代码后，R4到R6寄存器所访问的内存地址以及存取的值是0x000100D0，0x000100D4，以及0x000100D8，值对应是 0x3，0x4，以及0x5。



```
gef&gt; info registers r4 r5 r6
r4     0x3     3
r5     0x4     4
r6     0x5     5
gef&gt; x/3w 0x000100D0
0x100d0 &lt;array_buff&gt;: 0x00000003  0x00000004  0x00000005
```

而LDMIB指令会首先对指向的地址先加4，然后再加载数据到寄存器中。所以第一次加载的时候也会对指针加4，所以存入寄存器的是0X4(words[4])而不是0x3(words[3])。



```
dmib r0, `{`r4-r6`}`            /* words[4] -&gt; r4 = 0x04; words[5] -&gt; r5 = 0x05; words[6] -&gt; r6 = 0x06 */
stmib r1, `{`r4-r6`}`            /* r4 -&gt; array_buff[1] = 0x04; r5 -&gt; array_buff[2] = 0x05; r6 -&gt; array_buff[3] = 0x06 */
```

执行后的调试示意:



```
gef&gt; x/3w 0x100D4
0x100d4 &lt;array_buff+4&gt;: 0x00000004  0x00000005  0x00000006
gef&gt; info register r4 r5 r6
r4     0x4    4
r5     0x5    5
r6     0x6    6
```

当用LDMDA指令时，执行的就是反向操作了。R0指向words[3]，当加载数据时数据的加载方向变成加载words[3]，words[2]，words[1]的值到R6，R5，R4中。这种加载流程发生的原因是我们LDM指令的后缀是DA，也就是在加载操作完成后，会将指针做递减的操作。注意在做减法模式下的寄存器的操作是反向的，这么设定的原因为了保持让编号大的寄存器访问高地址的内存的原则。

多次加载，后置减法：

```
ldmda r0, `{`r4-r6`}` /* words[3] -&gt; r6 = 0x03; words[2] -&gt; r5 = 0x02; words[1] -&gt; r4 = 0x01 */
```

执行之后，R4-R6的值：



```
gef&gt; info register r4 r5 r6
r4     0x1    1
r5     0x2    2
r6     0x3    3
```

多次加载，前置减法：

```
ldmdb r0, `{`r4-r6`}` /* words[2] -&gt; r6 = 0x02; words[1] -&gt; r5 = 0x01; words[0] -&gt; r4 = 0x00 */
```

执行之后，R4-R6的值：



```
gef&gt; info register r4 r5 r6
r4 0x0 0
r5 0x1 1
r6 0x2 2
```

多次存储，后置减法：



```
stmda r2, `{`r4-r6`}` /* r6 -&gt; array_buff[2] = 0x02; r5 -&gt; array_buff[1] = 0x01; r4 -&gt; array_buff[0] = 0x00 */
执行之后，array_buff[2]，array_buff[1]，以及array_buff[0]的值：
gef&gt; x/3w 0x100D0
0x100d0 &lt;array_buff&gt;: 0x00000000 0x00000001 0x00000002
```

多次存储，前置减法：

```
stmdb r2, `{`r4-r5`}` /* r5 -&gt; array_buff[1] = 0x01; r4 -&gt; array_buff[0] = 0x00; */
```

执行之后，array_buff[1]，以及array_buff[0]的值：



```
gef&gt; x/2w 0x100D0
0x100d0 &lt;array_buff&gt;: 0x00000000 0x00000001
```



**PUSH和POP**

在内存中存在一块进程相关的区域叫做栈。栈指针寄存器SP在正常情形下指向这篇区域。应用经常通过栈做临时的数据存储。X86使用PUSH和POP来访问存取栈上数据。在ARM中我们也可以用这两条指令：

当PUSH压栈时，会发生以下事情：

SP值减4。

存放信息到SP指向的位置。

当POP出栈时，会发生以下事情：

数据从SP指向位置被加载

SP值加4。

下面是我们使用PUSH/POP以及LDMIA/STMDB命令示例:



```
.text
.global _start
_start:
   mov r0, #3
   mov r1, #4
   push `{`r0, r1`}`
   pop `{`r2, r3`}`
   stmdb sp!, `{`r0, r1`}`
   ldmia sp!, `{`r4, r5`}`
   bkpt
```

让我们来看看这段汇编的反汇编：



```
azeria@labs:~$ as pushpop.s -o pushpop.o
azeria@labs:~$ ld pushpop.o -o pushpop
azeria@labs:~$ objdump -D pushpop
pushpop: file format elf32-littlearm
Disassembly of section .text:
00008054 &lt;_start&gt;:
 8054: e3a00003 mov r0, #3
 8058: e3a01004 mov r1, #4
 805c: e92d0003 push `{`r0, r1`}`
 8060: e8bd000c pop `{`r2, r3`}`
 8064: e92d0003 push `{`r0, r1`}`
 8068: e8bd0030 pop `{`r4, r5`}`
 806c: e1200070 bkpt 0x0000
```

可以看到，我们的LDMIA以及STMDB指令被编译器换为了PUSH和POP。因为PUSH和STMDB sp!是等效的。同样的还有POP和LDMIA sp!。让我们在GDB里面跑一下上面那段汇编代码。



```
gef&gt; break _start
gef&gt; run
gef&gt; nexti 2
[...]
gef&gt; x/w $sp
0xbefff7e0: 0x00000001
```

在连续执行完前两条指令后，我们来看看SP，下一条PUSH指令会将其减8，并将R1和R0的值按序存放到栈上。



```
gef&gt; nexti
[...] ----- Stack -----
0xbefff7d8|+0x00: 0x3 &lt;- $sp
0xbefff7dc|+0x04: 0x4
0xbefff7e0|+0x08: 0x1
[...] 
gef&gt; x/w $sp
0xbefff7d8: 0x00000003
```

再之后，这两个值被出栈，按序存到寄存器R2和R3中，之后SP加8。



```
gef&gt; nexti
gef&gt; info register r2 r3
r2     0x3    3
r3     0x4    4
gef&gt; x/w $sp
0xbefff7e0: 0x00000001
```

<br>

传送门

[【系列分享】ARM 汇编基础速成1：ARM汇编以及汇编语言基础介绍](http://bobao.360.cn/learning/detail/4070.html)

[【系列分享】ARM 汇编基础速成2：ARM汇编中的数据类型](http://bobao.360.cn/learning/detail/4075.html)

[【系列分享】ARM 汇编基础速成3：ARM模式与THUMB模式](http://bobao.360.cn/learning/detail/4082.html)

**[【系列分享】ARM 汇编基础速成4：ARM汇编内存访问相关指令](http://bobao.360.cn/learning/detail/4087.html)**
