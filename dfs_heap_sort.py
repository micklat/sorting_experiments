from numpy.random import randint, seed
from math import log2

# This is an in-place, stable, worst-case n*log(n) sorting algorithm with O(1) additional memory complexity.
# Unlike blocksort, it is simple, and takes less than 100 lines of code.
# Unlike quicksort, its worst-case time is n*log(n). Also, it eliminates the heuristics of pivots.
# Unlike mergesort, it only needs a constant amount of auxiliary storage.
# Unlike heapsort, it is stable.

# overview: we keep a binary tree with the heap property, where each left subtree is full and the tree is stored
# in the array in depth-first order. We run k from 1 to n-1 and use the heap property to select the k'th-smallest 
# item in O(log(n)) time.

# some non-asymptotic speed-ups are possible.
# in particular, the calls to find_smallest_from keep visiting a frontier of nodes in the tree.
# the nodes in the frontier are the right-children of ancestors of <k>. As <k> moves, the frontier changes gradually.
# also, every swap between a[k] and a[j] updates one member in the frontier.

def dfs_left_child(i, subtree_depth):
    return i+1

def dfs_right_child(i, subtree_depth):
    assert subtree_depth >= 2
    return i + (1<<(subtree_depth-1))


DEBUG = False

def dfs_heap_sort(a):
    n = len(a)
    tree_depth = n.bit_length()

    dfs_heapify(a, tree_depth)
    #check_heapiness(a, 0, tree_depth)
    root = 0
    while tree_depth > 1:
        level_stop = min(n, dfs_right_child(root, tree_depth))
        if DEBUG: print("solving a[%d:%d], tree_depth=%d" % (root, level_stop, tree_depth))
        for k in range(root, level_stop):
            j = find_smallest_from(a, k, root, tree_depth)
            if DEBUG: assert a[j] == a[k:].min()
            if j==k: continue
            exchange_rightwards(a, k, j, root, tree_depth)
            if DEBUG: assert is_sorted(a[:k+1])
        root = level_stop
        tree_depth -= 1
        #check_heapiness(a, 0, tree_depth)


def find_smallest_from(a, start, root, tree_depth):
    i = root
    n = len(a)
    subtree_depth = tree_depth
    v_smallest = a[start]
    i_smallest = start
    while i < start:
        r = dfs_right_child(i, subtree_depth) 
        if r > start: # <start> is in the left subtree of <i>
            if r<n:
                v = a[r]
                if v < v_smallest:
                    v_smallest = v
                    i_smallest = r
            i = dfs_left_child(i, subtree_depth)
        else: # <start> is in the right subtree of <i>
            #assert a[dfs_left_child(i, subtree_depth)] <= a[start]
            i = r
        subtree_depth -= 1
    assert i==start
    return i_smallest


def exchange_rightwards(a, k, j, root, tree_depth):
    assert k<j
    a[k], a[j] = a[j], a[k]
    recover_heapiness(a, j, root, tree_depth) 


def get_subtree_depth(j, i, i_subtree_depth):
    # depth of subtree rooted at <i>, if full
    subtree_depth = i_subtree_depth
    while i<j:
        r = dfs_right_child(i, subtree_depth)
        if r > j: # <j> is a left-descendant of <i>
            i = dfs_left_child(i, subtree_depth)
        else: # <j> is a right-descendant of <i>
            i = r
        subtree_depth -= 1
    assert i==j
    return subtree_depth

def recover_heapiness(a, j, i, i_subtree_depth):
    n = len(a)
    subtree_depth = get_subtree_depth(j, i, i_subtree_depth)
    del i
    vj = a[j]
    while subtree_depth >= 2:
        l = dfs_left_child(j, subtree_depth)
        if l >= n: break # this node has no children
        vl = a[l]
        smaller = l
        vs = vl
        r = dfs_right_child(j, subtree_depth)
        if r < n:
            vr = a[r]
            if vr < vs:
                smaller = r
                vs = vr
        if vs >= vj: break
        # swap j and <smaller>
        a[j], a[smaller] = vs, vj
        j = smaller # note that vj remains the same because of the swap
        subtree_depth -= 1


def dfs_heapify(a, tree_depth):
    # There are probably optimization opportunities here.
    # most of the work in recover_heapiness is often drilling down from the root to j, 
    # just to find the subtree_depth of j, especially when <a> is already sorted.
    # If we allow ourselves to traverse <a> recursively, in post-order, then we'd be 
    # able to start recover_heapiness from j instead of 0.
    # But we don't even need that. We just need to know where are the nodes of each tree layer.
    for j in range(len(a)-2, -1, -1):
        recover_heapiness(a, j, 0, tree_depth)


def is_sorted(a):
    return (a[1:] >= a[:-1]).all()


def test(n_repetitions=10):
    max_num = 1000 # just for convenience, keeping the numbers smallish
    n = 10000
    for i in range(n_repetitions):
        seed(i)
        a = randint(max_num, size=n)
        dfs_heap_sort(a)
        assert(is_sorted(a))


def check_heapiness(a, start, d):
    i = start
    n = len(a)
    if (start + 1 >= n) or (d<2): return
    l = dfs_left_child(i, d)
    r = dfs_right_child(i, d)
    i_good = (a[i] <= a[l]) and ((r>=n) or (a[r] >= a[i]))
    assert(i_good)
    check_heapiness(a, l, d-1)
    check_heapiness(a, r, d-1)


if __name__=="__main__":
    test()

