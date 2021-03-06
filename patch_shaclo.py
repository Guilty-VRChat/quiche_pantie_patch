from PIL import Image
import os
import sys
import random
import convert_shaclo as cvt

args = sys.argv
panties = os.listdir('./dream/')
stitch_correction = False
print("Shaclo pantie patcher. Options: [-r] Random pantie, [-c] Enable stitch correction")
if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    else:
        fname =  input("Type pantie name: ./dream/")
    if '-c' in args[1:]:
        stitch_correction = True
else:
    fname =  input("Type pantie name: ./dream/")

if fname in panties:
    cvt.convert2shaclo(fname, stitch_correction=stitch_correction)
    pantie = Image.open('./shaclo_pantie.png')
    origin = Image.open('body_shaclo.png')
    if stitch_correction:
        origin.paste(pantie,(49,16),pantie)
    else:
        origin.paste(pantie,(62,16),pantie)
    origin.save('patched_shaclo.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
