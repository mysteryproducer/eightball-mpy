from PIL import Image,ImageFont, ImageDraw
import argparse

width=8
height=18
font_size=14
font_face="Monaco"

def set_width(x):
    width=x
def set_height(x):
    height=x
def set_font(x):
    font_face=x
def set_size(x):
    font_size=x

description="This tool creates bitmap font code files for use in the gc9a01 library.\n"+\
            "Fonts must be monospaced, and their width/height specified.\n"+\
            "TODO: byte alignment! Does this work for 8x8,8x16,16x16,16x32?"
args=argparse.ArgumentParser(description=description)
args.add_argument("width",action=set_width)
args.add_argument("height",action=set_height)
args.add_argument("font-face",action=set_font)
args.add_argument("font-size",action=set_size)

font=ImageFont.truetype(font_face,size=font_size)

def get_bytes(img,width,height):
    result=list()
    bit_count=0
    byte=0
    for i in range(0,height):
        for j in range(0,width):
            bit=0 if img.getpixel((j,i))==0 else 1
            byte=byte * 2 + bit
            bit_count+=1
            if bit_count==8:
                result.append(byte)
                byte=0
                bit_count=0
    return result

lines=[f"WIDTH = {width}\n",
        f"HEIGHT = {height}\n",
        "FIRST = 32\n",
        "LAST = 127\n",
        "_FONT = \\\n"]
#b'\x
#for i in range(ord("p"),ord("v")):
for i in range(32,128):
    img=Image.new("1",size=(width,height))
    draw = ImageDraw.Draw(img)
    draw.text((0,0), chr(i), font=font,fill=(255))
    bytes=get_bytes(img,width,height)
#    print(bytes)
#    img.show()
    char="b'"
    for j in range(0,len(bytes)):
        char+="\\x{:02x}".format(bytes[j])
    char+="'\\\n" if i<127 else "'\n"
    lines.append(char)
    
lines.append('\n')
lines.append("FONT = memoryview(_FONT)")
with open(f"src/fonts/monaco{font_size}.py","w") as file:
    file.writelines(lines)
