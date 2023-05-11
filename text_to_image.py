#Importing Library
from PIL import Image
from sys import argv
import argparse
import os



parser = argparse.ArgumentParser(description='Text to image',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-f', '--filename', default='input/oposicao_sindical.txt', help='path to input file', metavar='DIR')

args = parser.parse_args()

fileName = args.filename
txt=open(fileName, "r")

BG=Image.open("myfont/bg.png") #path of page(background)photo (I have used blank page)
sheet_width=BG.width
gap, ht = 100, 21

text = txt.read().replace("\n","&")
# for each letter in the uploaded txt file, read the unicode value and replace it with
# the corresponding handwritten file in the "myfont" folder.
def set_newline_coords(gap=gap, height=ht, is_space=False):
    offset = 140
    if is_space:
        calculated_height = height + 2*offset
    else:
        calculated_height = height + offset
    return gap, calculated_height

print(text)
for i in text:
    print(i, gap, ht)
    if i == '&':
        gap, ht = set_newline_coords(height=ht, is_space=True)
        continue
    if i == '%':
        gap, ht = set_newline_coords(height=ht, is_space=False)
        continue
    

    cases = Image.open("myfont/{}.png".format(str(ord(i))))

    BG.paste(cases, (gap, ht))
    size = cases.width

    gap+=size

    if sheet_width < gap or len(i)*115 >(sheet_width-gap):
        gap, ht = set_newline_coords(height=ht, is_space=False)
        print('linebreak')
    

print(gap)
print(sheet_width)
preprocessed_path = os.path.join('output/preprocessed/', os.path.basename(fileName)[:-4])+'.png'

BG.save(preprocessed_path,"PNG")#.save("teste.RGBA")
os.system(f"python3 enhance_image.py {preprocessed_path}")