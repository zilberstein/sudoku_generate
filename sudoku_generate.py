import solver
import puzzle
import scraper
import draw
import time
import sys

THEMES = [draw.PURPLE, draw.YELLOW, draw.ORANGE, draw.BLUE, draw.RED, draw.BRICK, draw.GHOST]


def scrape():
    print 'Please choose a difficulty:'
    print ' (1) Easy'
    print ' (2) Medium'
    print ' (3) Hard'
    print ' (4) Extra Hard'
    level = int(raw_input('level: '))
    if level not in range(1,5):
        print 'ERROR: invalid input'
        return None
    print 'Preparing to scrape puzzle from websudoku.com...'
    return scraper.get_puzzle(level)

def from_file():
    filename = raw_input('Pease enter a file name:')
    return puzzle.from_file(filename)

def main():
    print '\n\n\nWelome to Sudoku Generate v1.0'
    print '------------------------------'
    print 'Would you like to:'
    print ' (1) Load puzzle from a file'
    print ' (2) Scrape puzzle from webudoku.com'
    choice = raw_input('enter your choice: ')
    if choice == '1':
        raw_puzzle = from_file()
    elif choice == '2':
        raw_puzzle = scrape()
    else:
        print 'ERROR: invalid input'
        sys.exit()
    if raw_puzzle is None:
        print 'No puzzle'
        sys.exit()
    print 'load successful, here is your puzzle:'
    print raw_puzzle
    name = raw_input('Please enter a puzzle name: ')
    start = time.clock()
    solved_puzzle = solver.solve(raw_puzzle)
    dt = (time.clock() - start) * 1000
    if not solver.solved_puz(solved_puzzle):
        print 'Unable to solve puzzle %(name)s' % {'name':name}
        sys.exit()
    print 'Successfully solved %(name)s in %(time)fms' % {'name':name,'time':dt}
    print 'Please specify a theme:'
    print ' (1) Purple'
    print ' (2) Yellow'
    print ' (3) Orange'
    print ' (4) Blue'
    print ' (5) Red'
    print ' (6) Brick'
    print ' (7) Ghost'
    theme = int(raw_input('theme: '))
    if theme not in range(1,8):
        print 'ERROR: invalid input'
        sys.exit()
    draw.draw_puz(raw_puzzle,THEMES[theme - 1]).save('puzzles/%(name)s_original.bmp'%{'name':name})
    draw.draw_puz(solved_puzzle,THEMES[theme - 1]).save('puzzles/%(name)s_solved.bmp'%{'name':name})
    text_puz = open('puzzles/%(name)s.puz'%{'name':name}, 'w')
    text_spz = open('puzzles/%(name)s.spz'%{'name':name}, 'w')
    text_puz.write(str(raw_puzzle))
    text_spz.write(str(solved_puzzle))
    text_puz.close()
    text_spz.close()
    print 'saved puzzle to output files... process terminated'
    

if __name__ == '__main__':
    main()