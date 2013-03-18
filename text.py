from PIL import Image, ImageFilter, ImageDraw, ImageFont
PUZZLE = [[2,7,None, 4,1,None, 8,3,None],
          [8,None,None, None,None,9, None,1,None],
          [None,None,None, 2,8,None, None,4,5],
          [4,None,2,None,None,None,7,6,None],
          [None,None,None,6,None,2,None,None,None],
          [None,1,6,None,None,None,9,None,8],
          [1,2,None,None,6,3,None,None,None],
          [None,4,None,8,None,None,None,None,6],
          [None,3,7,None,5,4,None,8,2]]
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

def draw_puz(puz):
    w = 1024
    h = 1024
    fg = (256,225,256)
    bg = (256,190,256)
    img = Image.new("RGB", (w,h), bg)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Arial.ttf", 75)
    draw.rectangle([w/3,0,(2*w)/3,h/3],fill = fg)
    draw.rectangle([0,h/3,w/3,(2*h)/3],fill = fg)
    draw.rectangle([w/3,(2*h)/3,(2*w)/3,h],fill = fg)
    draw.rectangle([(2*w)/3,h/3,w,(2*h)/3],fill = fg)
    for i in range(1,9):
        if i % 3 == 0:
            draw.line([(i*w)/9,0,(i*w)/9,h],fill = (0,0,0), width=2)
            draw.line([0,(i*h)/9,w,(i*h)/9],fill = (0,0,0), width=2)
        else:
            draw.line([(i*w)/9,0,(i*w)/9,h],fill = (128,128,128), width=1)
            draw.line([0,(i*h)/9,w,(i*h)/9],fill = (128,128,128), width=1)
    for i in range(9):
        for j in range(9):
            if puz[j][i] is not None:
                size = draw.textsize(str(puz[j][i]), font=font)
                ofsx = (w/9 - size[0])/2
                ofsy = (h/9 - size[1])/2
                draw.text((ofsx+(i*w)/9, ofsy+(j*h)/9), str(puz[j][i]), font=font, fill=(0,0,0))
    img.show()