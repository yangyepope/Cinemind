class Test(object):
    def __init__(self, name):
        self.name = name

    # 重写 | 运算符
    def __or__(self, other):
        # 当执行 a | b 时，会调用 a 的 __or__ 方法，并把 b 作为 other 传入
        # 返回一个序列对象，开始链式链接
        return MySequence(self, other)

    # 为了方便打印查看结果，增加 __str__ 方法
    def __str__(self):
        return self.name

class MySequence(object):
    def __init__(self, *args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)

    # 为序列类也重写 | 运算符，以支持 a | b | c
    def __or__(self, other):
        # 将后续的对象继续追加入序列
        self.sequence.append(other)
        return self

    # 执行方法：遍历并打印序列中所有的 Test 对象
    def run(self):
        for i in self.sequence:
            print(i)

if __name__ == '__main__':
    # 实例化对象
    a = Test('a')
    b = Test('b')
    c = Test('c')
    d = Test('d')
    e = Test('e')

    # 使用 | 符号进行链路编排
    # 这一步本质上是：d = a.__or__(b).__or__(c)
    f = a | b | c | d | e
    
    # 统一执行
    f.run()

# 总结：LangChain 中的 LCEL 语法（prompt | model）底层
# 也是通过重写了这些组件类的 __or__ 运算符来实现的。
