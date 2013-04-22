import requests
from bs4 import BeautifulSoup
import puzzle as p

def get_puzzle(level=1):
    """ Scrapes a sudoku puzzle from the website websudoku.com
        There are 4 difficulty labels (1-4) where 1 is the easiest
        and 4 is the hardest.  The default is to grab an easy
        puzzle."""
    page = requests.get('http://view.websudoku.com/?level='+str(level)).text
    soup = BeautifulSoup(page)
    # find all the tags containing the puzzle values
    tags = [[soup.find(id='f'+str(i)+str(j)) for i in range(9)]
            for j in range(9)]
    # transform the tags into integers (or None)
    puz  = [[int(cell['value']) if cell.has_key('value') else None for cell in col]
            for col in tags]
            
    return p.Puzzle(puz)
