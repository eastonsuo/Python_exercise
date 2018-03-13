#! /usr/bin/env python
# -*- coding: utf-8 -*-
print("fab_1-------")


def fab_1(max):
    n, a, b = 0, 1, 1
    while n < max:
        print(a)
        a, b = b, a + b
        n = n + 1


fab_1(5)
print("fab_2-------")


def fab_2(max):
    n, a, b = 0, 1, 1
    L = []
    while n < max:
        L.append(a)
        a, b = b, a + b
        n = n + 1
    return L


for i in fab_2(5):
    print(i)
print("fab_3-------")


class Fab_3(object):

    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 1, 1

    def __iter__(self):
        return self

    def next(self):
        if self.n < self.max:
            r = self.a
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration


for i in Fab_3(5):
    print(i)
print("fab_4-------")


def fab_4(max):
    n, a, b = 0, 1, 1
    while n < max:
        yield a
        a, b = b, a + b
        n = n + 1


for i in fab_4(5):
    print(i)
f = fab_4(5)
print(f.next())
print(f.next())

from inspect import isgeneratorfunction, isgenerator
print(isgenerator(f))
print(isgeneratorfunction(fab_4))

print("协程-生产者消费者模型------")


def consumer():
    r = ""
    while True:
        n = yield r
        if not n:
            return
        print("[consumer] consuming %s" % n)
        r = "200 ok"


def producer(consumer):
    consumer.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print("[producer] producing %s" % n)
        r = consumer.send(n)
        print("[consumser] returns: %s" % r)
    consumer.close()


c = consumer()
producer(c)

print("""receive = yield value 原本是执行g.next()时会执行到这一步，
然后返回value的值，这里多出了一个receive，就是说，允许传一个值进来，当做此时的参数，
此时不用next触发，而是用send触发。我觉得，用g.next()和g.send(None)是一个效果的。
可以先给一个g.next()来启动一下，到第一次yield处------""")


def gen():
    value = 0
    while True:
        receive = yield value
        if receive == 'e':
            break
        value = 'got %s' % receive


g = gen()
print (g.next())
print (g.next())
print (g.send(None))
print (g.send('hello'))
print (g.send(123))
print (g.send('e'))
