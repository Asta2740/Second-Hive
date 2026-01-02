##https://gchq.github.io/CyberChef/#recipe=Fork('%5C%5Cn','%5C%5Cn',false)From_Base32('A-Z2-7%3D',true)XOR(%7B'option':'UTF8','string':'h0pp3r'%7D,'Standard',false)Zlib_Inflate(0,0,'Adaptive',false,false)Merge(true)Label('X1')Split('H0','H0%5C%5Cn')ROT13(true,true,false,19)Jump('X1',8)From_Base64('A-Za-z0-9%2B/%3D',true,false)Render_Image('Raw')&ieol=CRLF&oeol=CR
from PIL import Image

img = Image.open("download.png").convert("L")
raw = bytes(img.getdata())

w = 1  # width used in Generate_Image
out = bytearray()
for i in range(0, len(raw), w):
    b = raw[i]          # first pixel of each row
    if b == 0:
        break
    out.append(b)

print(out.decode("ascii"))
