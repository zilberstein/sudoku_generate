import text

N = 3;
M = 3;

class Puzzle(object):
    """Puzzle object stores all nodes in the puzzle.  the 2D list _rows
        should never be directly modified"""
    def __init__(self,arr=None):
        self.unsolved = []
        if arr is None:
            # Create new Nodes for each cell
            self._rows = [[Node(self, g, i) for i in range(N * M)] for g in range(N * M)]
            self.remaining = N * N * M * M
        else:
            # Fill Nodes with values from 2D array
            self._rows = [[Node(self, g, i,arr[g][i]) for i in range(N * M)] for g in range(N * M)]
            self.remaining = 0
            for r in self._rows:
                for node in r:
                    if node.val is None:
                        self.remaining += 1
                        self.unsolved.append(node)


    def __repr__(self):
        return '\n'.join([' '.join([str(val) for val in r]) for r in self._rows])

    # Cool side note... all the lambda functions are invertible!!
    # They work for converting row, column notation to group, index notation
    # And they work to convert back too!!
    def rows(self):
        return puzIterator(self,lambda g,i: g,lambda g,i: i)

    def cols(self):
        return puzIterator(self,lambda g,i: i,lambda g,i: g)

    def boxs(self):
        return puzIterator(self,
                           lambda g,i: N * (g / N) + (i / M),
                           lambda g,i: M * (g % N) + (i % M))

class Node(object):
    """Node used in a puzzle"""
    def __init__(self,puz,row,col,val=None):
        """Constructor, value of the Node is initialized to None"""
        self.puz, self.val, self.row, self.col = puz, val, row, col
        self.box = N * (row / N) + (col / M)

        if self.val is None:
            self.poss = set(range(1, M * N + 1))
            self.given = False
        else:
            self.poss = set([]);
            self.given=True

    def __repr__(self):
        if self.val is None:
            return " "
        else:
            return str(self.val)

    def remove_poss(self,l):
        """Remove the given list of values from the list of possible values"""
#        print "Remove",set(l) , "From", self.poss,"(",self.row,",",self.col,")"
        self.poss = self.poss - set(l)
        if len(self.poss) == 1:
            self.val = self.poss.pop()
            self.puz.remaining -= 1
            self.puz.unsolved.remove(self)
            return True
        return False


class puzIterator:
    """Iterator class iterates over a puzzle by group"""
    def __init__(self, puz, transform_group, transform_index):
        self.puz, self.tg, self.ti = puz, transform_group, transform_index
        # The group number
        self.group = -1

    def __iter__(self):
        self.group = -1
        return self

    def next(self):
        if self.group >= N * M - 1:
            raise StopIteration
        else:
            self.group += 1
            return self[self.group]

    def __getitem__(self, group):
        return [self.puz._rows[self.tg(group,index)][self.ti(group,index)] for index in range(N * M)]
