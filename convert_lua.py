import os
import sys
import skimage.io as io
import skimage as ski
import skimage.transform as skt
import skimage.morphology as skm
import numpy as np
from myutil import *

def convert2lua(fname=None):
    panties = os.listdir('./dream/')
    if fname is None:
        fname =  input("Type pantie name: ./dream/")
    if fname in panties:
        pantie = io.imread('./dream/'+fname)
        mask = io.imread('./mask/mask_lua.png')
        pantie = np.bitwise_and(pantie,mask)
        
        patch = np.copy(pantie[-140:-5,546:,:])
        pantie[-115:,546:,:] = 0
        patch = skt.resize(patch[::-1,::-1,:],(patch.shape[0],65),anti_aliasing=True,mode='reflect')
        [pr,pc,d] = patch.shape
        pantie[127-5:127-5+pr,:pc,:] = np.uint8(patch*255)
        
        front = pantie[:260,:300,:]
        front = np.pad(front,[(0,0),(100,130),(0,0)],mode='constant')    
        front = perspective_transform(front,np.matrix('1, 0.12, 0; 0, 1, 0; 0.0005,0,1'))
        front = perspective_transform(front,np.matrix('1, 0.0, 0; 0, 1, 0; -0.0009,0,1'))
        front = front[:-45,70:335]
        front = resize(front,[2,2.44])[:,40:,:]
        
        back = pantie[:265,300:,:]
        back = np.pad(back,[(15,0),(0,200),(0,0)],mode='constant')
        back = affine_transform(back,-10,150,0,0,inv=True)
        back = perspective_transform(back, np.matrix('1, -0.2, 0; 0, 1, 0; -0.0001,0,1'))
        back = back[2:-24,25:-5-17,:]
        back = resize(back,[1.71,1.79])

        [fr,fc,_] = front.shape
        [br,bc,_] = back.shape
        shift_y = 20
        pantie = np.zeros((np.max([fr,br])+shift_y,fc+bc,d))
        pantie[shift_y:shift_y+fr,:fc,:] = front
        pantie[:br,fc:,:] = back

        # Finalize
        io.imsave('lua_pantie.png',pantie)
    else:
        print("Cannot find it")
        
if __name__ == '__main__':
    convert2lua()
