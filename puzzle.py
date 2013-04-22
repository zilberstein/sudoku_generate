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
            self.unsolved = [n for n in self._rows]
        else:
            # Fill Nodes with values from 2D array
            self._rows = [[Node(self, g, i,arr[g][i]) for i in range(N * M)] for g in range(N * M)]
            self.remaining = 0
            for r in self._rows:
                for node in r:
                    if node.val is None:
                        self.unsolved.append(node)
        
        # Cool side note... all the lambda functions are invertible!!
        # They work for converting row, column notation to group, index notation
        # And they work to convert back too!!
        self.rows = puzIterator(self,lambda g,i: g,lambda g,i: i)
        self.cols = puzIterator(self,lambda g,i: i,lambda g,i: g)
        self.boxs = puzIterator(self,
                                lambda g,i: N * (g / N) + (i / M),
                                lambda g,i: M * (g % N) + (i % M))

    def __repr__(self):
        return '\n'.join([' '.join([str(val) for val in r]) for r in self._rows])

    def set_node(self, row, col, val):
        node = self._rows[row][col]
        node.val = val
        node.poss = []
        self.unsolved.remove(node)


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
        self.poss = self.poss - set(l)
        if len(self.poss) == 1:
            self.val = self.poss.pop()
            self.puz.unsolved.remove(self)
            return True
        return False


class puzIterator:
    """Iterator class iterates over a puzzle by group.  It takes in a puzzle, and two
        transform functions.  There functions transform the row, column notation into
        group, index notation.  A group is either a row a column, or a box.  If it is
        a row, then the group number is the row number and the index is the column in
        that row.  If the group is a column, then the group number refers to the
        column and the index refers to the row.  Box groups are indexed starting at
        from the top left.  The numbers increase across and then down.  Nodes inside
        box are indexed in the same way.  ie:
        
        0 1 2
        3 4 5
        6 7 8
        """
    
    
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
        return [self.puz._rows[self.tg(group,index)][self.ti(group,index)]
                for index in range(N * M)]
