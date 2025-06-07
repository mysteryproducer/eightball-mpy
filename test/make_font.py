from PIL import Image,ImageFont, ImageDraw

width=16
height=35

font=ImageFont.truetype("Monaco",size=28)

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
with open("monaco28.py","w") as file:
    file.writelines(lines)
