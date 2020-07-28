msg="Hello"

def str_to_bin(msg):
    l=[format(ord(i),'08b') for i in msg]
    return l

def str_to_ascii(msg):
    return [chr(int(i,2)) for i in msg]

print(msg)
print(str_to_bin(msg))
print(str_to_ascii(str_to_bin(msg)))

import cv2
import numpy as np

img=cv2.imread("pic2.jpg")
print(img.shape)