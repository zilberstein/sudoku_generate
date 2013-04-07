from PIL import Image, ImageFilter, ImageDraw, ImageFont
import math
PUZZLE = [[2,7,None, 4,1,None, 8,3,None],
          [8,None,None, None,None,9, None,1,None],
          [None,None,None, 2,8,None, None,4,5],
          [4,None,2,None,None,None,7,6,None],
          [None,None,None,6,None,2,None,None,None],
          [None,1,6,None,None,None,9,None,8],
          [1,2,None,None,6,3,None,None,None],
          [None,4,None,8,None,None,None,None,6],
          [None,3,7,None,5,4,None,8,2]]

PUZZLE_HARD = [[None,None,None,2,None,None,None,6,3],
               [3,None,None,None,None,5,4,None,1],
               [None,None,1,None,None,3,9,8,None],
               [None,None,None,None,None,None,None,9,None],
               [None,None,None,5,3,8,None,None,None],
               [None,3,None,None,None,None,None,None,None],
               [None,2,6,3,None,None,5,None,None],
               [5,None,3,7,None,None,None,None,8],
               [4,7,None,None,None,1,None,None,None],]

EVIL = [[None,2,None,None,None,8,None,None,None],
        [None,1,None,None,3,None,None,5,8],
        [None,None,6,None,4,None,1,None,None],
        [5,None,None,None,None,None,None,None,None],
        [None,7,4,None,1,None,6,8,None],
        [None,None,None,None,None,None,None,None,3],
        [None,None,7,None,6,None,4,None,None],
        [6,4,None,None,8,None,None,9,None],
        [None,None,None,9,None,None,None,1,None],]

INKALA = [[8,None,None,None,None,None,None,None,None],
          [None,None,3,6,None,None,None,None,None],
          [None,7,None,None,9,None,2,None,None],
          [None,5,None,None,None,7,None,None,None],
          [None,None,None,None,4,5,7,None,None],
          [None,None,None,1,None,None,None,3,None],
          [None,None,1,None,None,None,None,6,8],
          [None,None,8,5,None,None,None,1,None],
          [None,9,None,None,None,None,4,None,None]]

PURPLE = {'bg':(256,190,256),'fg':(256,225,256),'text':(128,0,128),'line':(0,0,0)}
YELLOW = {'bg':(256,256,190),'fg':(256,256,225),'text':(128,128,0),'line':(0,0,0)}
ORANGE = {'bg':(256,200,128),'fg':(256,225,200),'text':(100,50,0),'line':(0,0,0)}
BLUE = {'bg':(215,215,256),'fg':(225,225,256),'text':(0,0,150),'line':(0,0,0)}
def find_letter(img):
    img=img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    palette = [(0,0,0), (256,256,256)]
    img.putpalette(palette)
    img.show()

def add_text(img,string):
    draw = ImageDraw.Draw(img)
    draw.text((0,0),string)
    draw.line([(0,0),(10,20),(50,50)])
    img.show()

def draw_puz(puz, theme=PURPLE):
    w = 1024
    h = 1024
    img = Image.new("RGB", (w,h), theme['bg'])
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Arial.ttf", 75)
    font_small = ImageFont.truetype("Arial.ttf", 20)
    draw.rectangle([w/3,0,(2*w)/3,h/3],fill = theme['fg'])
    draw.rectangle([0,h/3,w/3,(2*h)/3],fill = theme['fg'])
    draw.rectangle([w/3,(2*h)/3,(2*w)/3,h],fill = theme['fg'])
    draw.rectangle([(2*w)/3,h/3,w,(2*h)/3],fill = theme['fg'])
    for i in range(1,9):
        if i % 3 == 0:
            draw.line([(i*w)/9,0,(i*w)/9,h],fill = theme['line'], width=3)
            draw.line([0,(i*h)/9,w,(i*h)/9],fill = theme['line'], width=3)
        else:
            draw.line([(i*w)/9,0,(i*w)/9,h],fill = theme['text'], width=1)
            draw.line([0,(i*h)/9,w,(i*h)/9],fill = theme['text'], width=1)
    for i in range(9):
        for j in range(9):
            val = puz._rows[j][i].val
            if val is None:
                color = theme['text']
                for v in puz._rows[j][i].poss:
                    size = draw.textsize(str(v), font=font)
                    ofsx = w*((v-1)%3)/27 + (w/9 - size[0])/6
                    ofsy = h*((v-1)/3)/27 + (h/9 - size[1])/6
                    draw.text((ofsx+(i*w)/9, ofsy+(j*h)/9), str(v), font=font_small, fill=color)
            else:
                if puz._rows[j][i].given:
                    color = theme['line']
                else:
                    color = theme['text']
                size = draw.textsize(str(val), font=font)
                ofsx = (w/9 - size[0])/2
                ofsy = (h/9 - size[1])/2
                draw.text((ofsx+(i*w)/9, ofsy+(j*h)/9), str(val), font=font, fill=color)
    img.show()

def gradient():
    img = Image.new("RGB", (1024,768))
    draw = ImageDraw.Draw(img)
    for i in range(1024):
        draw.line([i,0,i,768],fill=(128,(i*256)/1024,256))
    img.show()

def pretty_circle():
    img = Image.new("RGB", (1024,1024),(256,256,256))
    draw = ImageDraw.Draw(img)
    r = 300
    d = 5000
    for i in range(1024):
        for j in range(1024):
            dx = abs(512-i)
            dy = abs(512-j)
            d = int(math.sqrt(dx*dx + dy*dy))
            draw.point([i,j],fill=(d*256/724,d*256/724,d*256/724))
    img.show()

