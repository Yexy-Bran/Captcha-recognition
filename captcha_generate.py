import os
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random

def max_file_num(path):
    names = os.listdir(path)
    res = 0
    for name in names:
        index = name.rfind('.')
        name = int(name[:index])
        res = max(name,res)
    return res

def random_fond():  
    path='/Workspace/font/'
    for root,dirs,files in os.walk(path):
        files
    fond = files[random.randint(0,len(files)-1)]	    
    return path + os.path.sep + fond

def random_code(lenght=1):    
    code = ''
    for char in range(lenght):
        code += chr(random.randint(65,90)) if random.random() > 0.5 else chr(random.randint(48,57))#random.randint(97,122))
    return code

def random_color(s=1,e=255):
    return (random.randint(s,e),random.randint(s,e),random.randint(s,e))

def create_img(code,i,path,fond,width=12,height=12):
    image = Image.new('L',(width,height),255)
    font = ImageFont.truetype(fond,15)
    draw = ImageDraw.Draw(image)
    for x in range(width):
        for y in range(height):
            if random.random()>0.95:
                draw.point((x,y),fill=0) #random_color(0,0))
    
    for t in range(1):
        draw.text((t+1,-3),code[t],font=font,fill=0)
    #image = image.filter(ImageFilter.BLUR)
    code = path + os.path.sep + str(i) + '.png'
    image.save(code)
    return code,image
if __name__ == "__main__":
    n = 3000
    for j in range(36*36):
        code = random_code(1)
        path = '/Workspace/data/' + code
        if not os.path.exists(path):
            fmax = 0
            os.makedirs(path)
        else:
            fmax = max_file_num(path)
        for i in range(fmax+1, n):
	        fond = random_fond()
	        create_img(code, i+1, path,fond)
