#coding: utf-8

import socket
import re

"""
2017/02/16
作业 1


资料:
在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数的参数和 recv 函数的返回值都是 bytes 类型
其他请参考上课内容, 不懂在群里发问, 不要憋着
"""


# 1
# 补全函数
def protocol_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表协议的字符串, 'http' 或者 'https'
    '''
    
    protocol = 'http' # 默认为http
    s1 = re.split(r'\://', url) # 根据 "://" 把url分成两部分
    #print(s1)
    if len(s1) == 2:     # 的确被分割成两部分，否则就是默认的http
        protocol = s1[0]
    return protocol

def test_protocol_of_url(url):
    # res = protocol_of_url('g.cn') # 单个测试
    res = list(map(protocol_of_url, url)) # 全部测试
    print(res)

    
# 2
# 补全函数
def host_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表主机的字符串, 比如 'g.cn'
    '''
    
    # 取第二部分
    s1 = re.split(r'\://', url) # 根据 "://" 把url分成两部分,取第二部分再分析
    if len(s1) == 2:     # 的确被分割成两部分
       s2 = s1[1] # 取第二项
    else: #否则split会把url外面套一层[],返回的s1是一个单元素list
       s2 = s1[0] #恢复s1为string类型
    
    # 以/为分界符,把s1分成域名和其他部分
    s3 = re.split(r'/', s2)
    if (len(s3) == 2): # 取出第一部分
        s4 = s3[0]
    else: # 只有第一部分，所以split返回仅包含url的list，要把s2恢复成string类型的s2
        s4 = s3[0]
        
    # 以:为分隔符，取出host
    s5 = re.split(r'\:', s4)
    if (len(s5) == 2):
        s6 = s5[0] # 第一部分是host，第二部分是port
    else:
        s6 = s5[0] #恢复s5
    return s6 # 因为host不存在缺省，必须写在url中

def test_host_of_url(url):
    #host_of_url('http://g.cn/')
    s1 = list(map(host_of_url, url))
    print(s1)
    
    
# 3
# 补全函数
def port_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表端口的字符串, 比如 '80' 或者 '3000'
    注意, 如上课资料所述, 80 是默认端口
    '''
    port = 80 # 默认是80
    
    # 取第二部分
    s1 = re.split(r'\://', url) # 根据 "://" 把url分成两部分,取第二部分再分析
    if len(s1) == 2:     # 的确被分割成两部分
       s2 = s1[1] # 取第二项
    else:
       s2 = s1[0] # 恢复s1为string
    
    # 以/为分界符，取出{host:port}
    s3 = re.split(r'/', s2)
    if (len(s3) == 2):
        s4 = s3[0] # 取第一部分
    else:
        s4 = s3[0] # 恢复s3为string类型
    
    # 以:为分隔符，取出port
    s5 = re.split(r'\:', s4)
    if (len(s5) == 2): # 的确有两部分
        port = int(s5[1]) #第二部分是port,取出来
    #else: # s3只有一部分，说明只有host没有port，所以端口为默认值80  
    return port
    
def test_port_of_url(url):
    #s1 = port_of_url('g.cn')
    s1 = list(map(port_of_url, url))
    print(s1)
    
# 4
# 补全函数
def path_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表路径的字符串, 比如 '/' 或者 '/search'
    注意, 如上课资料所述, 当没有给出路径的时候, 默认路径是 '/'
    '''
    path = '/'
    
    # 取第二部分
    s1 = re.split(r'\://', url) # 根据 "://" 把url分成两部分,取第二部分再分析
    if len(s1) == 2:     # 的确被分割成两部分
       s2 = s1[1] # 取第二项
    else:
        s2 = s1[0] # 恢复s1
    
    # 以/为分界符，取第二部分
    s3 = re.split(r'/', s2)
    if (len(s3) == 2):
        path = '/'+ s3[1] # 取第二部分
    # else :,若只有一部分，就是没有path，选默认的path
    return path

def test_path_of_url(url):
    s1 = list(map(path_of_url, url))
    print(s1)
    
    
# 5
# 补全函数
def parsed_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    返回一个 tuple, 内容如下 (protocol, host, port, path)
    '''
    protocol, host, port, path = 'http', None, 80, '/' # host不可以缺省，url中必写
    #以://分割成两部分，第一部分是protocol,第二部分是其他
    s1 = re.split(r'\://', url) 
    if (len(s1) == 2):
        protocol = s1[0] # 取第一部分作为协议，否则就是默认协议http
        s2 = s1[1] # 取第二部分
    else:
        s2 = s1[0] # 因为split默认会返回一个list，所以会把url封装成list; 
        #这里是把[url] 重新恢复为一个string类型的url，并当做第二部分
        
    # 以/为分界符,分成 {host:port}和其他{即path部分}
    s3 = re.split(r'/', s2)
    if (len(s3) == 2):
        s4 = s3[0] # 取{host:port}部分
        path = '/'+s3[1] # 取剩余部分，就是path
    else: # 说明只有{host:port}，没有第二部分{因为host不能缺省！！！}
        s4 = s3[0] # 恢复s3
        # path取默认值就是'/'
    
    # 以:分界符，分成host和port,注意：host不可以省略，但是port可以省略
    s5 = re.split(r'\:', s4)
    if (len(s5) == 2):
        host = s5[0]
        port = int(s5[1])
    else:
        host = s5[0] # 只有host，恢复s5并传给host；port保持默认值80
        
    return (protocol, host, port, path)

def test_parsed_url(url):
    s1 = list(map(parsed_url, url))
    print(s1)

    
# 5
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def get(url):
    '''
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    '''
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #http连接
    # s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) # https连接
    
    protocol, host, port, path = parsed_url(url)
    #print(protocol, host, port, path, type(host), type(port))
    # 用 connect 函数连接上主机, 参数是一个 tuple
    s.connect((host, port))
    
    # 连接上后, 可以通过getsockname()得到本机的 ip 和端口
    ip, port = s.getsockname()
    print('本机 ip 和 port {} {}'.format(ip, port))
    
    # 构造一个 HTTP 请求
    http_request = 'GET {0} HTTP/1.1\r\nHost:{1}:{2}\r\n\r\n'.format(path,host,port)
    # 发送 HTTP 请求给服务器
    # send 函数只接受 bytes 作为参数
    # str.encode 把 str 转换为 bytes, 编码是 utf-8
    request = http_request.encode('utf-8')
    print('请求', request)
    s.send(request)
    
    buffersize = 1023
    response = s.recv(buffersize)
    # response = b''
    # while True:
        # tmp = s.recv(buffersize)
        # response += tmp
        # if tmp < buffersize:
            # break
    # 输出响应的数据, bytes 类型
    print('响应', response)
    # 转成 str 再输出
    print('响应的 str 格式', response.decode('utf-8'))


# 使用
def main():
    
    '''
    url = 'http://movie.douban.com/top250'
    r = get(url)
    print(r)
    '''
    
    # url = [
    # 'g.cn',
    # 'g.cn/',
    # 'g.cn:3000',
    # 'g.cn:3000/search',
    # 'http://g.cn',
    # 'https://g.cn',
    # 'http://g.cn/',
    # 'localhost/index.html'
    # ]
    
    # test_protocol_of_url(url)
    # test_host_of_url(url)
    # test_port_of_url(url)
    # test_path_of_url(url)
    # test_parsed_url(url)
    
    # #url = 'localhost:3000/'
    # url = 'localhost:3000/index.html'
    # get(url)

    
if __name__ == '__main__':
    main()
