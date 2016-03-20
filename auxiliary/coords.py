import operator


def add((x1, y1), (x2, y2)):
    return (x1+x2, y1+y2)


def neg((x, y)):
    return -x, -y


def mul((x, y), k):
    return x*k, y*k


def div((x, y), k):
    return x/k, y/k


class Pt(tuple):
    def __new__(self, *T):
        if len(T) == 1 and T[0].__class__ == tuple is tuple:
            return tuple.__new__(Pt, *T)
        else:
            return tuple.__new__(Pt, T)

    def __add__(self, other):
        return Pt(add(self, other))

    def __neg__(self):
        return Pt(neg(self))

    def __sub__(self, other):
        return self + neg(other)

    def __mul__(self, other):
        return Pt(mul(self, other))

    def __div__(self, other):
        return Pt(div(self, other))

Pt.x = property(operator.itemgetter(0))
Pt.y = property(operator.itemgetter(1))