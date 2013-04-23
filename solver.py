import puzzle
import copy

from multiprocessing import Pool

def update_groups(node):
    """Run single candidates method on every group that contains
        the given Node"""
    single_candidate(node.puz.rows[node.row])
    single_candidate(node.puz.cols[node.col])
    single_candidate(node.puz.boxs[node.box])

def single_candidate(group):
    """Basic logic solving method.  Removes the values of every node
        in the group from the list of possibilities of all other nodes
        in that group"""
    for node in group:
        if node.val is None:
            # if remove_poss reports that the value has been updated,
            # then the groups need to be updated to reflect the change
            if node.remove_poss([n.val for n in group if n.val is not None]):
                update_groups(node)

def sc_all_groups(puz):
    """Run single_candidate on all groups in the puzzle until no more
        changes are possible"""
    n = puz.remaining
    for r in puz.rows:
        single_candidate(r)
    for c in puz.cols:
        single_candidate(c)
    for b in puz.boxs:
        single_candidate(b)
    if puz.remaining != n and puz.remaining != 0:
        sc_all_groups(puz)

def single_position(group):
    """ Simple logic solver that determined if there is only one possible
        space for a value in a group """
    for node in group:
        if node.val is None:
            for p in node.poss:
                if p not in [x for n in group for x in n.poss if n is not node]:
                    node.remove_poss([v for v in node.poss if v is not p])
                    update_groups(node)
#
#
#def candidate_lines(group, puz, val):
#    rows = set([node.row for node in group if val in node.poss])
#    cols = set([node.col for node in group if val in node.poss])
#    boxs = set([node.box for node in group if val in node.poss])
##    print rows,cols
#    if len(rows) == 1:
#        for node in puz.rows[rows.pop()]:
#            if node not in group:
#                if node.remove_poss([val]):
#                    update_groups(node)
#    elif len(cols) == 1:
#        for node in puz.cols[cols.pop()]:
#            if node not in group:
#                if node.remove_poss([val]):
#                    update_groups(node)


def solved_group(group):
    """Check if a group has been solved. ie each node contains a value between
        1 and 9 and each value appears only once"""
    return set([node.val for node in group if node.val is not None]) == set(range(1,10))

def solved_puz(puz):
    """Check if the entire puzzle is solved and correct"""
    # All groups are solved
    for r in puz.rows:
        if not solved_group(r):
            return False
    for c in puz.cols:
        if not solved_group(c):
            return False
    for b in puz.boxs:
        if not solved_group(b):
            return False
    # And no nodes are unsolved
    return len(puz.unsolved) == 0



def solve(puz):
    """ Solve any sudoku puzzle using a combination of simple logic and
        resursive backtracking.  Any 'easy' puzzle should be solvable using
        logic alone.  Medium or hard puzzles will require recursive
        backtracking"""
    puz = copy.deepcopy(puz) # copy puz so as not to modify the original
    n = len(puz.unsolved)
    sc_all_groups(puz)
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
        # Only resort to recursive backtracking is the puzzle cannot
        # be solved by simple logic
        return recursive_backtrack(puz)

def recursive_backtrack(puz):
    """ Use recursive backtracking to solve the puzzle.  All the unsolved nodes
        are sorted by number of remaining possibilities so the nodes with the
        fewest remaining possibilities (ie hifher chance of success) are solved
        first.  After a value is inserted, the groups of that node are updated
        so as to require less guessing"""
    if len(puz.unsolved) == 0:
        return puz
    # sort the unsolved nodes by number of possibilities so as to have a higher
    # probability of guessing correctly
    remaining = sorted(puz.unsolved,key = lambda n: len(n.poss))
    node = remaining[0]
    update_groups(node)
    r, c = node.row, node.col
    for v in node.poss:
        p = copy.deepcopy(puz)
        p.rows[r][c].val = v
        p.rows[r][c].poss = []
        p.unsolved.remove(p._rows[r][c])
        update_groups(p.rows[r][c])
        p = recursive_backtrack(p)
        if solved_puz(p):
            return p
    return puz
