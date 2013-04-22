from PIL import Image, ImageFilter, ImageDraw, ImageFont

PURPLE = {'bg':(256,190,256),'fg':(256,225,256),'text':(128,0,128),'line':(0,0,0)}
YELLOW = {'bg':(256,256,190),'fg':(256,256,225),'text':(128,128,0),'line':(0,0,0)}
ORANGE = {'bg':(256,200,128),'fg':(256,225,200),'text':(100,50,0),'line':(0,0,0)}
BLUE = {'bg':(215,215,256),'fg':(225,225,256),'text':(0,0,150),'line':(0,0,0)}
RED = {'bg':(256,178,178),'fg':(256,215,215),'text':(150,0,0),'line':(0,0,0)}
BRICK = {'bg':(128,25,25),'fg':(100,0,0),'text':(256,200,200),'line':(256,256,256)}
GHOST = {'bg':(64,0,64),'fg':(32,0,64),'text':(256,128,256),'line':(256,256,256)}

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
    return img