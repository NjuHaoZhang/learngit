This is the practice of learning a project based on Python and flask
### lesson_1 : 
> 在本节，我学习了
* http协议的request和response的结构，并基于python解析了request和response。 
以及学习了浏览器如何发送报文给服务器，服务器如何解析报文，并返回什么response给浏览器  
以及浏览器的地址栏输入的url到底本质做了什么？并且向服务器发送了什么？
* 第二，我编写了一个程序模拟浏览器，实现了解析地址栏的url，通过url分析request的结构，并把一个url中各个组分提取出来，然后按照request的结构拼接出一个request报文，基于TCP协议使用Scoket编程把request报文发送给服务器。
* 第三，我编写了一个模拟服务器的小程序，接收浏览器通过地址栏发送的request，打印了request的结构，并学会了用chrome的F12来分析这个request。 并且根据解析后的request中的path，把响应通过TCP协议发送给，模拟浏览器。在模拟浏览器中打印了response的内容和结构。

### lesson_2:
> 在本节，我实现了一个爬虫：分析豆瓣网的Top25的最佳电影，并把结构分层次展示。

### lesson_3:
> 在本节，我实现了一个Web服务器最小框架

### lesson_4:
> 在本节，基于Cookie和Session实现了用户登录注册功能,并手写了一个ORM框架，基于以上实现了对用户的增删改查。

### lesson_5:
> 在本节，实现了TODO小站

```
测试一下代码高亮
def test():
  print("hello")
  a  = 1+2
  print(a)
```
