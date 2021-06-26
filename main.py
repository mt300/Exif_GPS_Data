from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS
import csv
from os import listdir
from os.path import isfile,join
import re


_TAGS_r = dict(((v,k) for k,v in TAGS.items()))
_GPSTAGS_r = dict(((v,k) for k, v in GPSTAGS.items()))

def img_process(img_file):
    img = Image.open(img_file)
    #print(img.info.keys())
    #print(len(img.info['exif']))
    exifd = img._getexif()
    #print(type(exifd))
    #print(exifd.keys())


    if type(exifd) == dict:
        keys = list(exifd.keys())      
        keys = [k for k in keys if k in TAGS]

        #print("\n".join([TAGS[k] for k in keys]))

        #print("\n".join([str((TAGS[k], exifd[k])) for k in keys]))
        ##geting imgage height and width
        for k in keys:
            if TAGS[k] == "ExifImageWidth":
                img.x = exifd[k]
                #print(img.x)
            if TAGS[k] == "ExifImageHeight":
                img.y = exifd[k]
                #print(img.y)
        ##geting image coordinates
        for k in keys:
            if TAGS[k] == "GPSInfo":
                print(exifd[k])
                img.latitude = (exifd[k][2][0][0]/exifd[k][2][0][1],exifd[k][2][1][0]/exifd[k][2][1][1],exifd[k][2][2][0]/exifd[k][2][2][1])
                #print(img.latitude)
                img.longitude = (exifd[k][4][0][0]/exifd[k][4][0][1],exifd[k][4][1][0]/exifd[k][4][1][1],exifd[k][4][2][0]/exifd[k][4][2][1])
                #print(img.longitude)
                img.altitude = (exifd[k][6][0]/exifd[k][6][1])
                #print(img.altitude)

        #print(type(img))
        img_name = img_file.split(".",1)

        return(img_name[0], img.x,img.y,img.latitude, img.longitude, img.altitude)
    else:
        return('error: o arquivo {} não tem informações de metadados completa'.format(img_file))


file_name_list = [f for f in listdir() if isfile(join(f))]
#print(file_name_list)
for k in file_name_list:
    #FILTRO PARA JPG
    if re.search(".JPG",k) != None:
        results = img_process(k)
        print(results)
        nome = k.split(".",1)
        nome = str(nome[0])
        file = open(nome+".txt","w")
        file.write("\n"+str(results))
        file.close()
    else:
        print("ERROR: {} is not an .JPG with EXIF".format(k))


## nome X Y coordenadas