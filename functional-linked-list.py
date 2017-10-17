# implementing a linked list data structure in Python using a Lisp-like functional style.
# https://dbader.org/blog/functional-linked-lists-in-python
# Nil represents the empty list
# 练习使用递归
Nil = None


# cons operation extends a list at the front by inserting a new value
def cons(x, xs=Nil):
    return (x, xs)


assert cons(0) == (0, Nil)
assert cons(1, cons(0, Nil)) == (1, (0, Nil))

# lst(1,2,3) == (1,(2,3))
# helper function lst


def lst(*xs):
    if not xs:
        return Nil
    else:
        return cons(xs[0], lst(*xs[1:]))


assert lst(1, 2, 3, 4) == (1, (2, (3, (4, Nil))))
assert lst() == Nil
assert lst(1) == (1, Nil)

# Basic operations
# head returns the first element of a list.


def head(xs):
    return xs[0]


assert head(lst(1, 2, 3, 4)) == 1

# tail returns a list containing all elements except the first.


def tail(xs):
    return xs[1]


assert tail(lst(1, 2, 3, 4)) == lst(2,3,4)


# is_empty returns True if the list contains zero elements.
def is_empty(xs):
    return xs is Nil

assert is_empty(Nil)
assert not is_empty(lst(1))


# The length operation returns the number of elements in a given list.
def length(xs):
    if xs is Nil:
        return 0
    else:
        return 1 + length(tail(xs))

assert length(Nil) == 0
assert length(lst(1,2)) == 2


# concat takes two lists as arguments and concatenates them.
# The result of concat(xs, ys) is a new list that contains all elements in xs followed by all elements in ys.
# We implement the function with a simple divide and conquer algorithm.
# hard
def concat(xs1,xs2):
    if is_empty(xs1):
        return xs2
    else:
        return cons(head(xs1),concat(tail(xs1),xs2))
assert concat(lst(1,2,3),Nil) == lst(1,2,3)
assert concat(Nil,Nil) == Nil
assert concat(Nil,lst(1,2,3)) == lst(1,2,3)
assert concat(lst(1,2,3),lst(4)) == lst(1,2,3,4)

# last returns the last element of a non-empty list
def last(xs):
    if is_empty(tail(xs)):
        return head(xs)
    else:
        return last(tail(xs))
assert last(lst(1,2,3)) == 3


# init returns all elements except the last one (the initial elements).
def init(xs):
    if length(xs) == 1:
        return Nil
    else:
        return cons(head(xs),init(tail(xs)))
assert init(lst(1,2,3)) == lst(1,2)
assert init(lst(1)) == Nil

def init2(xs):
    if is_empty(tail(tail(xs))):
        return cons(head(xs))
    else:
        return cons(head(xs), init2(tail(xs)))
assert init2(lst(1,2,3)) == lst(1,2)

# The reverse function below implements list reversa
def reverse(xs):
    if xs is Nil:
        return Nil
    elif length(xs) == 1:
        return xs
    else:
        return cons(last(xs),reverse(init(xs)))
assert reverse(lst(1,2,3,4)) == lst(4,3,2,1)
assert reverse(Nil) == Nil
assert reverse(lst(0)) == lst(0)
assert reverse(reverse(lst(1,2,3,4))) == lst(1,2,3,4)

# take and drop generalize head and tail by returning arbitrary prefixes and suffixes of a list.
# For example, take(2, xs) returns the first two elements of the list xs
# whereas drop(3, xs) returns everything except the last three elements in xs.
def take(n,xs):
    if n == 0:
        return Nil
    else:
        return cons(head(xs),take(n-1,tail(xs)))
assert take(2,lst(1,2,3)) == lst(1,2)

def drop(n,xs):
    if n == 0:
        return xs
    else:
        return drop(n-1,tail(xs))
assert drop(2,lst(1,2,3)) == lst(3)
assert drop(1,lst(1,2,3)) == lst(2,3)

#element selection
def apply(i,xs):
    return head(drop(i,xs))
assert apply(0,lst(1,2,3,4)) == 1
assert apply(2,lst(1,2,3,4)) == 3

# insertion sort using head() tail() and is_empty
# insert into a ordered list
def insert(x,xs):
    if is_empty(xs) or x < head(xs):
        return cons(x,xs)
    else:
        return cons(head(xs),insert(x,tail(xs)))
assert insert(0,lst(1,2,3,4)) == lst(0,1,2,3,4)
assert insert(5,lst(1,2,3,4)) == lst(1,2,3,4,5)
assert insert(3,lst(1,2,4)) == lst(1,2,3,4)

def isort(xs):
    if is_empty(xs):
        return xs
    else:
        return insert(head(xs),isort(tail(xs)))
assert isort(lst(1,2,3,4)) == lst(1,2,3,4)
assert isort(lst(3,2,1,4)) == lst(1,2,3,4)

# to_string operation returns a python style string
def to_string(xs,prefix="[",postfix="]"):
    def to_string(xs):
        if is_empty(xs):
            return ""
        elif is_empty(tail(xs)):
            return str(head(xs))
        else:
            return str(head(xs)) + "," + to_string(tail(xs))
    return prefix + to_string(xs) + postfix
assert to_string(lst(1,2,3,4)) == "[1,2,3,4]"
