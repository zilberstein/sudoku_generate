import requests
from bs4 import BeautifulSoup, NavigableString
import puzzle as p

def get_puzzle(level=1):
    page = requests.get('http://view.websudoku.com/?level='+str(level)).text
    soup = BeautifulSoup(page)
    tags = [[soup.find(id='f'+str(i)+str(j)) for i in range(9)] for j in range(9)]
    puz  = [[int(cell['value']) if cell.has_key('value') else None for cell in col] for col in tags]
            
    return p.Puzzle(puz)