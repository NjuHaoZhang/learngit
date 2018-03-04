from models import Model
from utils import log

class User(Model):

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.id = form.get('id', None) # 如果id获取不到，默认取None

    def validate_login(self):
        users_instance = self.all()
        users_list = [u.__dict__ for u in users_instance] # 包含了干扰项id
        for ul in users_list: # 取每一个user进行匹配
            if (self.username == ul['username']) and (self.password == ul['password']):
                return True
        return False # 所有用户都失配，即匹配失败

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


