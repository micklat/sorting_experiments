from pylab import *
from dfs_heap_sort import dfs_heap_sort
from numpy import random
from timeit import timeit


def get_scaling(max_n=50000):
    full_a = random.randint(1000, size=max_n)
    ns = []
    ts = []
    n = max_n
    reps = 3
    while n>50:
        a = full_a[:n]
        assert a.base is full_a # a is a view, not a copy
        a[:] = random.randint(1000, size=n)
        t = timeit(lambda: dfs_heap_sort(a), number=reps) / reps
        ns.append(n)
        ts.append(t)
        print(n,t)
        n = n//2
    return ns,ts


if __name__=="__main__":
    ns,ts = get_scaling()
    plot(ns,ts)
    ylabel("seconds")
    xlabel("n")
    show()
