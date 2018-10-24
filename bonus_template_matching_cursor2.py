import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
for i in range(8,11):
    file_name='task3_bonus/neg_%d.jpg' % i
    out_file_name='task3_bonus/t2_ans_%d.jpg' % i
    img_rgb = cv2.imread(file_name)
    lower_black, upper_black = np.array([0,0,0]), np.array([70,70,70])
    black_mask = cv2.inRange(img_rgb, lower_black, upper_black)
    img = cv2.GaussianBlur(black_mask,(5,5),0)
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)
    template = cv2.imread('task3_bonus/t2.png',0)
    template = cv2.GaussianBlur(template,(5,5),0)
    template = cv2.adaptiveThreshold(template,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)
    template = cv2.bitwise_not(template)
    w, h = template.shape[::-1]
    res1 = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED)
    threshold1 = 0.68
    loc1 = np.where( res1 >= threshold1)
    for pt in zip(*loc1[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imwrite(out_file_name, img_rgb)
