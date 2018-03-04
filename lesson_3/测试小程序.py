import time
def log(*args, **kwargs):
    """
    :param args:
    :param kwargs:
    :return:
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)
    """
    print(*args, **kwargs)


def test_1():
    d={'site':'http://www.jb51.net','name':'jb51','is_good':'yes'}
    #方法1：通过has_key # 此法在py3.5中失效{或者是pycharm的锅？}
    # print(d.has_key('site'))
    #方法2：通过in
    log('body' in d.keys())
    log(d.keys())
    log(d.values())


def test_2():
    d = dict(name='user', passwd='123')
    log(d)
    log(d.keys())
    log('name' in d.keys(), 'name1' in d.keys())
    log(d.values())
    log('user' in d.values(), '123' in d.values())


def test_3():
    log(id(1))
    log(id("abc"))
    log(id([1, 2, 3]))

# 测试整数
def test_4():
    x = 5000000 # 大整数
    y = 5000000
    log(x == y)
    log(x is y)
    log(id(x))
    log(id(y))


# 测试字符串
def test_5():
    x = "abc"
    y = "abc"
    log(x == y)
    log(x is y)
    log(id(x))
    log(id(y))


# 测试list
def test_6():
    x = [1, 2, 3]
    y = [1, 2, 3]
    log(x == y)
    log(x is y)
    log(id(x))
    log(id(y))


# 测试tuple
def test_7():
    x = (1, 2, 3)
    y = (1, 2, 3)
    log(x == y)
    log(x is y)
    log(id(x))
    log(id(y))

# 测试 dict
def test_8():
    x = {"id": 1, "name": "Tom", "age": 18}
    y = {"id": 1, "name": "Tom", "age": 18}
    log(x == y)
    log(x is y)
    log(id(x))
    log(id(y))


# 测试set
def test_9():
    x = set([1, 2, 3])
    y = set([1, 2, 3])
    log(x == y)
    log(x is y)
    log(id(x))
    log(id(y))


def test_10():
    x = [1, 2, 3]
    y = x # 说明这里是深拷贝，y和x都指向同一个对象
    log(x == y)
    log(x is y)
    log(id(x))
    log(id(y))

if __name__ == '__main__':
    # test_1()
    #test_2()
    # test_3()
    # test_4()
    # test_5()
    # test_6()
    # test_7()
    # test_8()
    # test_9()
    test_10()