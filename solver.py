import puzzle
import text
import copy
import time

PUZZLE = [[None,None,1,9,5,7,None,6,3],
          [None,None,None,8,None,6,None,7,None],
          [7,6,9,1,3,None,8,None,5],
          [None,None,7,2,6,1,3,5,None,None],
          [3,1,2,4,9,5,7,8,6],
          [None,5,6,3,7,8,None,None,None],
          [1,None,8,6,None,9,5,None,7],
          [None,9,None,7,1,None,6,None,8],
          [6,7,4,5,8,3,None,None,None]]

MEDIUM = [[None, None, 7,8]]

def update_groups(node):
    single_candidate(node.puz.rows()[node.row])
    single_candidate(node.puz.cols()[node.col])
    single_candidate(node.puz.boxs()[node.box])

def single_candidate(group):
    for node in group:
        if node.val is None:
            if node.remove_poss([n.val for n in group if n.val is not None]):
                update_groups(node)


def sc_all_groups(puz):
    n = puz.remaining
    for r in puz.rows():
        single_candidate(r)
    for c in puz.cols():
        single_candidate(c)
    for b in puz.boxs():
        single_candidate(b)
#    print n,puz.remaining
    if puz.remaining != n and puz.remaining != 0:
        sc_all_groups(puz)

def single_position(group):
    for node in group:
        if node.val is None:
            for p in node.poss:
                if p not in [x for n in group for x in n.poss if n is not node]:
                    node.remove_poss([v for v in node.poss if v is not p])
                    update_groups(node)


def candidate_lines(group, puz, val):
    rows = set([node.row for node in group if val in node.poss])
    cols = set([node.col for node in group if val in node.poss])
    boxs = set([node.box for node in group if val in node.poss])
#    print rows,cols
    if len(rows) == 1:
        for node in puz.rows()[rows.pop()]:
            if node not in group:
                if node.remove_poss([val]):
                    update_groups(node)
    elif len(cols) == 1:
        for node in puz.cols()[cols.pop()]:
            if node not in group:
                if node.remove_poss([val]):
                    update_groups(node)


def solved_group(group):
    return len([node.val for node in group if node.val is not None]) == len(set([node.val for node in group if node.val is not None]))

def solved_puz(puz):
    for r in puz.rows():
        if not solved_group(r):
            return False
    for c in puz.cols():
        if not solved_group(c):
            return False
    for b in puz.boxs():
        if not solved_group(b):
            return False
    return len(puz.unsolved) == 0



def solve(puz):
    n = puz.remaining
#    print 'begin SC'
    sc_all_groups(puz)
#    print 'end SC',n,puz.remaining
    while n != puz.remaining and puz.remaining != 0:
        for r in puz.rows():
            single_position(r)
        for c in puz.cols():
            single_position(c)
        for b in puz.boxs():
            single_position(b)
        n = puz.remaining
    if len(puz.unsolved) == 0:
        return puz
    else:
        puz = brute_force(puz)
        return puz

def brute_force(puz):
    if len(puz.unsolved) == 0:
        return puz
    remaining = sorted(puz.unsolved,key = lambda n: len(n.poss))
    node = remaining[0]
    update_groups(node)
#    text.draw_puz(node.puz)
    for v in node.poss:
        p = copy.deepcopy(puz)
        p._rows[node.row][node.col].val = v
        p._rows[node.row][node.col].poss = []
        p.unsolved.remove(p._rows[node.row][node.col])
        p.remaining -= 1
        update_groups(p._rows[node.row][node.col])
        p = brute_force(p)
        if solved_puz(p):
            return p
    return puz


def time_it(f, args):
    start = time.clock()
    f(args)
    return (time.clock() - start)*1000