from utils import log
from models import Message
from models import User

import random


# 这个函数用来保存所有的 messages
message_list = []
# session 可以在服务器端实现过期功能
session = { # 程序自行生成这个信息
    # 'session_id': { # 扩充session的功能：增加session的过期时间
    #     'username': 'gua',
    #     'id':
    #     'note':
    #     '过期时间': '2.22 21:00:00'
    # }
}


def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def current_user(request):
    session_id = request.cookies.get('user', '')  # 其实是浏览器把用户的Token写入request，给了服务器,服务器再解析出Token
    userinfo_dict = session.get(session_id, '')  # 服务器根据用户Token来判断Token是否存在于服务器的session这个dict中
    return userinfo_dict


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    # username = current_user(request)
    body = body.replace('{{username}}', '')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def response_with_headers(headers):
    """
Content-Type: text/html
Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 210 VERY OK\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def response_redirect_with_headers(headers):
    header = 'HTTP/1.1 302 redirect\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])  # 把dict的k和v都取出，用items()
    return header


def route_login(request):  # 通过登录,生成当前用户Token,并设置服务器上的session这个dict，
                           # 然后将Token放入Set-Cookie字段，返回response给浏览器。
                           # 浏览器把Token保存在本地。
                           # 下次此浏览器再次访问服务器会自动将Token放入request，从而验证用户身份。
    """
    登录页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/', # 这是cookie方案，下面将会使用session方案
    }
    # log('login, headers', request.headers)
    log('login, cookies', request.cookies) # 第二次访问服务器时，浏览器自动把cookie加入到request中
    result = ''
    # username = current_user(request) # 第一次登录 username为空
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        # log('u的属性dict', u.__dict__)
        if u.validate_login():
            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            user = User.find_by(username=u.username)  # 从文件中找到u对应的真正的user
            session[session_id] = user.__dict__  # 把user所有属性即一个dict，放入session
            log('session[session_id]的值', session[session_id])
            headers['Set-Cookie'] = 'user={}'.format(session_id)  # 浏览器会自动识别'Set-Cookie'并保存
        else:
            result = '用户名或者密码错误'  # 重新登录
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', '')  # 完全可以去静态页把这个字段干掉不显示
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    log('login的响应', r)
    return r.encode(encoding='utf-8')

def route_profile(request):
    userinfo_dict = current_user(request)
    # log("userinfo_dict,", userinfo_dict)
    if userinfo_dict != '':
        body = template('profile.html')
        body = body.replace('{{username}}', userinfo_dict['username'])
        body = body.replace('{{id}}', '{}'.format(userinfo_dict['id']))
        body = body.replace('{{note}}', userinfo_dict['note'])
        # log('profile body', body)
        headers = {'Content-Type':'text/html'}
        header = response_with_headers(headers)
        r = header + '\r\n' + body
        log('第一次login 的响应', r)
        return r.encode(encoding='utf-8')
    else:  # 没有登录就重定向
        # log("还没有登录，需要重定向")
        headers = {'Location': '/login', 'Content-Type':'text/html'}
        header = response_redirect_with_headers(headers)
        body = template('login.html')
        r = header + '\r\n' + body
        log('重定向login的响应，', r)
        return r.encode(encoding='utf-8')

def route_register(request):
    """
    注册页面的路由函数
    """
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    """
    消息页面的路由函数
    """
    username = current_user(request)
    if username == '【游客】':
        log("**debug, route msg 未登录")
        pass
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('post', form)
        message_list.append(msg)
        # 应该在这里保存 message_list
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
    '/profile': route_profile,
}
