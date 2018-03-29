# coding=utf-8

# Fibonacci sequence
# 1
fib = lambda n: n if n <= 2 else fib(n - 1) + fib(n - 2)


# 2
def memo(func):
    cache = {}

    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrap


@memo
def fib(i):
    if i < 2:
        return 1
    return fib(i - 1) + fib(i - 2)


# 3
def fib(n):
    a, b = 0, 1
    for i in xrange(n):
        a, b = b, a + b
    return b


# 变态台阶
fib = lambda n: n if n < 2 else 2 * fib(n - 1)

# List去重

# 1
list(set(l))

# 2
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = {}.fromkeys(l1).keys()

# 3
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = list(set(l1))
l2.sort(key=li.index)

# 4
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = []
[l2.append(i) for i in l1 if not i in l2]


# 链表成对调换
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def swapPairs(self, head):
        if head != None and head.next != None:
            next = head.next
            head.next = self.swapPairs(next.next)
            next.next = head
            return next
        return head


# 创建字典
# 1
dict = {}

# 2
items = [('name', 'earth'), ('port', '80')]
dict2 = dict(items)
dict1 = dict((['name', 'earth'], ['port', '80']))

# 3
dict1 = {}.fromkeys(('x', 'y'), -1)
dict2 = {}.fromkeys(('x', 'y'))


# Merge two sort list
def _recursion_merge_sort(l1, l2, tmp):
    if len(l1) == 0 or len(l2) == 0:
        tmp.extend(l1)
        tmp.extend(l2)
        return tmp
    else:
        if l1[0] < l2[0]:
            tmp.append(l1[0])
            del l1[0]
        else:
            tmp.append(l2[0])
            del l2[0]
        return recursion_merge_sort(l1, l2, tmp)


def recursion_merge_sort(l1, l2):
    return _recursion_merge_sort(l1, l2, [])
