import vga2_16x32 as bf
from PIL import Image,ImageDraw

def show_banner(cmin,cmax):
#for i in range(33,37):
    nchars=(cmax-cmin)
    img=Image.new("1",size=(bf.WIDTH,bf.HEIGHT*nchars))
    draw = ImageDraw.Draw(img)
    bytes=bf._FONT
    x=0
    y=0
    bytes_per_char=int(bf.WIDTH*bf.HEIGHT/8)
    _from=cmin*bytes_per_char
    _to=(_from+nchars)+bytes_per_char
    for byte in bytes[_from:_to]:
        mask=128
        for j in range(0,8):
            px=0 if mask & byte == 0 else 255
            draw.point((x,y),px)
            x+=1
            mask=int(mask/2)
            if x >= bf.WIDTH:
                x=0
                y+=1
    img.show()
show_banner(32,127)