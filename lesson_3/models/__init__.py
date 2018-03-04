import json
"""
json 是一种时下非常流行的数据格式
在 python 中可以方便地使用 json 格式序列化/反序列化字典或者列表
"""

from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # json 是一个序列化/反序列化(上课会讲这两个名词) list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s)


# Model 是用于存储数据的基类
class Model(object):
    # 类属性
    count = 0 # 给id提供计数值 {还有个问题，每次重启程序即重启Model，所以count会断电丢失}
    # 如果每次关闭程序前自动把count的值保存到文件中，每次重启程序后自动加载旧的count到本程序
    # 即实现真正的数据库的id自增功能

    # def __init__(self): # 因为User和Msg会重写init，所以父类的init不需要做子类即将要做的事
    #     self.id = None # 初始为None

    # @classmethod 说明这是一个 类方法
    # 类方法的调用方式是  类名.类方法()
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是 class
        # 所以我们可以得到 class 的名字
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        # 下面一句相当于 User(form) 或者 Msg(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        """
        save 函数用于把一个 Model 的实例保存到文件中
        """
        models = self.all()
        # log('models', models)

        if self.id is None:
            Model.count = Model.count + 1 # 每次save都自增id
            self.id = Model.count
            models.append(self)
        else: # 用新的当前记录覆盖原来的旧记录，等价于操作models，然后再把models写入文件
            # 找到这条记录，并修改
            for k, v in enumerate(models): # 把list也变成一个k-v，即把k找出来 {此时的v是一个dict}
                if v.id == self.id:
                    models[k] = self # 对应修改models，然后再把更新后的models写入文件；等价于修改了文件
                    break
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def delete(self):
        models = self.all() #从文件中拿出所有记录，待会儿对他操作，然后再把更新过的models取属性再写入文件
        for k,v in enumerate(models):
            if v.id == self.id:
                models[k] = None # 本条记录清除,注意要保持{}结构完整性; {受User.txt的存储格式约束，也许还有bug}
                log("找到要delete的user了")
                break
        l = [m.__dict__ for m in models if m !=None]
        path = self.db_path()
        save(l,path)


    # 我最开始的版本，虽然正确但是不好！下方有重构版
    # @classmethod
    # def find_by(cls,**kwargs):
    #     """
    #     :param kwargs: 传入一个find条件，比如 username='gua',注：*args可当做一个list，**args可当做一个dict
    #     :return:上面这句可以返回一个 username 属性为 'gua' 的 User 实例
    #             如果有多条这样的数据, 返回第一个
    #             如果没这样的数据, 返回 None
    #     """
    #     models = cls.all()
    #     models_attr_list = [m.__dict__ for m in models]
    #     log('测试models_attr_list',models_attr_list, type(models_attr_list)) # 需要暂时关闭__repr__
    #     ret = None
    #     for mal in models_attr_list:  # 循环取出每一个待匹配用户mal ,为一个dict
    #         flag = True  # 每次待匹配mdl之前，每次更新为真
    #         for k in kwargs: # 循环取出每一个find条件，为dict的一项
    #             # log('查看kwargs',k,type(k),kwargs[k],type(kwargs[k]))
    #             # 判定kwargs_dict是否被包含于mal_dict (前者是后者的子集)
    #             # 因为有一个条件不匹配就失败，故而使用False来寻找失配的情况
    #             if k not in mal.keys(): # 找不到这个k
    #                 flag = False
    #                 continue # 本轮的mal已经失配，进入下一次外循环
    #             elif kwargs[k] != mal[k]: # k等，但两者的v不对应相等
    #                 flag = False
    #                 continue # 本轮的mal已经失配，进入下一次外循环
    #         if flag == True:  # 匹配成功，保存结果，并立刻break返回
    #             for m in models:  # 遍历每一个Model实例
    #                 if mal == m.__dict__:
    #                     ret = m
    #             break # 当前mal对应的那个User对象即为所求
    #     return ret
    @classmethod
    def find_by(cls, **kwargs):
        models = cls.all()
        for m in models: # 测试每一个已存在的model
            flag = True # 开始认为存在这个m
            for k in kwargs: # 要检查所有条件都符合才行,所以应该从反面取排除较好
                # log("m的attr", m.__dict__)
                if  hasattr(m,k) == False:
                    flag = False
                    continue # 无须再往下判断其他条件了，这个m不符合，外循环跳至下一轮
                elif getattr(m,k) != kwargs[k]: # k存在，但是对应的v不相等 {好奇怪，m.k会报错}
                    flag = False
                    continue
            if flag == True: # 所有条件都筛选完，看看flag
                return m # 这个m即为符合的model，立即返回


    # 这个版本写的不好，下面是一个重构版
    # @classmethod
    # def find_all(self,**kwargs):
    #     """
    #     :param kwargs: 传入一个find条件，比如 username='gua',注：*args可当做一个list，**args可当做一个dict
    #     :return:上面这句可以返回一个 username 属性为 'gua' 的 User 实例
    #             如果有多条这样的数据, 返回全部结果的list
    #     """
    #     models = self.all()
    #     models_attr_list = [m.__dict__ for m in models]
    #     log('测试models_attr_list',models_attr_list, type(models_attr_list)) # 需要暂时关闭__repr__
    #     ret_list = []
    #     for mal in models_attr_list:  # 循环取出每一个待匹配用户mal ,为一个dict
    #         flag = True  # 每次待匹配mdl之前，每次更新为真
    #         for k in kwargs: # 循环取出每一个find条件，为dict的一项
    #             # log('查看kwargs',k,type(k),kwargs[k],type(kwargs[k]))
    #             # 判定kwargs_dict是否被包含于mal_dict (前者是后者的子集)
    #             # 因为有一个条件不匹配就失败，故而使用False来寻找失配的情况
    #             if k not in mal.keys(): # 找不到这个k
    #                 flag = False
    #                 continue # 本轮的mal已经失配，进入下一次 外循环
    #             elif kwargs[k] != mal[k]: # k等，但两者的v不对应相等
    #                 flag = False
    #                 continue # 本轮的mal已经失配，进入下一次 外循环
    #         if flag == True:  # 匹配成功，加入到list中
    #             for m in models:  # 遍历每一个Model实例
    #                 if mal == m.__dict__:
    #                     ret_list.append(m)
    #     return ret_list
    @classmethod
    def find_all(cls, **kwargs):
        m_list = [] # 存在符合要求的所有model
        models = cls.all()
        for m in models:  # 测试每一个已存在的model
            flag = True  # 开始认为存在这个m
            for k in kwargs:  # 要检查所有条件都符合才行,所以应该从反面取排除较好
                if hasattr(m,k) == False:
                    flag = False
                    continue  # 无须再往下判断其他条件了，这个m不符合，外循环跳至下一轮
                elif getattr(m,k) != kwargs[k]:  # k存在，但是对应的v不相等
                    flag = False
                    continue
            if flag == True:  # 所有条件都筛选完，看看flag
                m_list.append(m)
        return m_list


    def __repr__(self):
        """
        这是一个 魔法函数
        不明白就看书或者 搜
        当你调用 str(o) 的时候
        实际上调用了 o.__str__()
        当没有 __str__ 的时候
        就调用 __repr__
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

# 以下两个类用于实际的数据处理
# 因为继承了 Model
# 所以可以直接 save load


