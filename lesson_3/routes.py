from utils import log
from models.message import Message
from models.user import User


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
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


# message_list 存储了所有的 message
message_list = []


def route_message(request):
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('post', form)
        message_list.append(msg)
        # 应该在这里保存 message_list
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('html_basic.html')
    # '#'.join(['a', 'b', 'c']) 的结果是 'a#b#c'
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    <img src="/static?file=doge.gif"/>
    GET /static?file=doge.gif
    path, query = response_for_path('/static?file=doge.gif')
    path  '/static'
    query = {
        'file', 'doge.gif',
    }
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n'+ f.read()
        return img


def route_find_user(request):
    # 测试find_by
    #u = User.find_by(username='gua')
    #u = User.find_by(username='gua', password='123')
    #u = User.find_by(username='gua', password='1234')

    #u = User.find_by(username='bbb')
    u = User.find_by(username='bbb', password='123')
    #u = User.find_by(username='bbb', password='1234')
    log('测试find_by',u,type(u))

    # 有时间写个单元测试


def route_find_all_user(request): # 等价于实现了一个对用户的select方法
    #u = User.find_all(password='123')
    u = User.find_all(username='gua')
    log('测试find_all', u, type(u))


def route_update_user(request): # 等价于实现了一个对用户的update方法
    u = User.find_by(username='gua')
    u.password = '123_update'
    u.save()
    # return  # 因为是测试这个update的功能，所以不需要真的返回一个response
    # 因为没有返回一个response，当然会报错，不要紧

def route_delete_user(request): # 测试删除用户的功能
    u = u = User.find_by(username='aaa')
    u.delete()

route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
    '/find_user':route_find_user,
    '/find_all_user':route_find_all_user,
    '/update_user':route_update_user,
    '/delete_user':route_delete_user,
}
