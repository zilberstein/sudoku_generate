# From the Python docs:
# http://docs.python.org/2/library/multiprocessing.html#using-a-pool-of-workers
from multiprocessing import Pool
import solver
import sys
import time

PROCESSES = 4

def rec(n):
    a = 999 * 999
    if n > 0:
        rec(n-1)

if __name__ == '__main__':
    pool = Pool(PROCESSES)
    start = time.clock()
    pool.map(rec, [81 for i in range(PROCESSES)])
    print 'multiprocessing time: '+str((time.clock() - start) * 1000)+'ms'
    start = time.clock()
    for i in range(PROCESSES):
        rec(81)
    print 'single thread time: '+str((time.clock() - start) * 1000)+'ms'