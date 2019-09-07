

class MyException(Exception):

    def __init__(self):
        self.status = False
        print('本次执行失败了')