import cv2
import numpy as np
import random

msg="Hello my name is Shobhit"
# with open("input1.txt",'r') as f:
#     msg=' '.join(f.readlines())
    # print(msg)

def str_to_bin(msg):
    l=[format(ord(i),'08b') for i in msg]
    return l

def str_to_ascii(msg):
    return [ord(i) for i in msg]

def steg1(msg):
    bin_msg=str_to_bin(msg)
    index=0
    k=0
    img=cv2.imread('pic2.jpg')
    for i in range(img.shape[0]):
        if(index==len(bin_msg)):
            break
        for j in range(img.shape[1]):
            if(index==len(bin_msg)):
                break
            for l in range(3):
                if(img[i,j,l]%2==0):
                    if(bin_msg[index][k]=='1'):
                        img[i,j,l]=img[i,j,l]+1
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
                # print(bin_msg[index])
                index+=1
    cv2.imwrite('pic_pr2.png',img)

def steg1_dec():
    img=cv2.imread('pic_pr2.png')
    out=""
    k=0
    bin_out=""
    done=False
    for i in range(img.shape[0]):
        if done:
            break
        for j in range(img.shape[1]):
            if done:
                break
            for l in range(3):
                if(img[i][j][l]%2==1):
                    bin_out+='1'
                else:
                    bin_out+='0'
                k+=1
                if(k==8):
                    break
            if(k==8):
                # print(bin_out)
                out+=chr(int(bin_out,2))
                bin_out=""
                k=0
                if(img[i][j][2]%2==1):
                    done=True
                    break
    return out

steg1(msg)
print(steg1_dec())

# def steg2(msg):
#     ascii_msg=str_to_ascii(msg)
#     # print(ascii_msg)
#     index=0
#     for i in range(img.shape[0]):
#         if(index==len(ascii_msg)):
#             break
#         for j in range(img.shape[1]):
#             if(index==len(ascii_msg)):
#                 break
#             for l in range(3):
#                 if(index==len(ascii_msg)):
#                     break
#                 img[i][j][l]=(img[i][j][l]+ascii_msg[index])%256
#                 # img[i][j][l]=255
#                 index+=1
#     cv2.imwrite('pic_pr3.jpg',img)

# steg2(msg)
