import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
for i in range(1,7):
    file_name='task3_bonus/t1_%d.jpg' % i
    out_file_name='task3_bonus/t1_ans_%d.jpg' % i
    img_rgb = cv2.imread(file_name)
    img = cv2.imread(file_name, 0)
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,37,2)
    cv2.imshow('res', img)
    cv2.waitKey(0)
    template = cv2.imread('task3_bonus/t1.png',0)
    tail = template.copy()
    tail2 = imutils.resize(tail, width=int(template.shape[1]*1))[:12,:]
    tail = imutils.resize(tail, width=int(template.shape[1]*1))[:9,:]
    template = cv2.adaptiveThreshold(template,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    tail2 = cv2.adaptiveThreshold(tail2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    tail = cv2.adaptiveThreshold(tail,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    w, h = template.shape[::-1]
    res1 = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED)
    res2 = cv2.matchTemplate(img,tail2,cv2.TM_CCORR_NORMED)
    res3 = cv2.matchTemplate(img,tail,cv2.TM_CCORR_NORMED)
    threshold1, threshold2, threshold3 = 0.80, 0.76, 0.77
    loc1 = np.where( res1 >= threshold1)
    for pt in zip(*loc1[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    loc2 = np.where( res2 >= threshold2)
    for pt in zip(*loc2[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    loc3 = np.where( res3 >= threshold3)
    for pt in zip(*loc3[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imwrite(out_file_name, img_rgb)
