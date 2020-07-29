import cv2
import numpy as np

class Steganography:
    @staticmethod
    def str_to_bin(msg):
        l=[format(ord(i),'08b') for i in msg]
        return l

    @staticmethod
    def encrypt(msg,img):
        bin_msg=Steganography.str_to_bin(msg)
        index=0
        k=0
        for i in range(img.shape[0]):
            if(index==len(bin_msg)):
                break
            for j in range(img.shape[1]):
                if(index==len(bin_msg)):
                    break
                for l in range(3):
                    if(img[i,j,l]%2==0):
                        if(bin_msg[index][k]=='1'):
                            img[i,j,l]+=1
                    else:
                        if(bin_msg[index][k]=='0'):
                            img[i,j,l]+=1
                    k+=1
                    if(k==8):
                        break   
                if(k==8):   #Stop when last pixel is odd
                    if(index==len(bin_msg)-1):
                        if(img[i,j,2]%2==0):
                            img[i,j,2]=img[i,j,2]+1
                    else:
                        if(img[i,j,2]%2==1):
                            img[i,j,2]=img[i,j,2]+1
                    k=0
                    index+=1
        return img
        