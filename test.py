import os
from PIL import Image
l = os.listdir('./Database/val/cloth/')
cloth = []
for i in range(0,len(l)) :
    temp = './Database/val/cloth/'+l[i]
    l[i] = l[i].split('_')[0]
    print(temp)
    print(l[i])
    cloth.append(Image.open(temp))
