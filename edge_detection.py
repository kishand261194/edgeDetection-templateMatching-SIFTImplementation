import numpy as np
from math import sqrt
import cv2
grey_img=cv2.imread('task1.png', 0)
rows=len(grey_img)
columns=len(grey_img[0])
padded_img=[[ 0 for i in range(columns+1)]for j in range(rows+1)]
for i in range(1, rows):
    for j in range(1, columns):
        padded_img[i][j]=grey_img[i-1][j-1]
grey_img=padded_img
new_img_right_sobel = [[0 for i in range(columns)]for j in range(rows)]
new_img_top_sobel = [[0 for i in range(columns)]for j in range(rows)]
combined = [[0 for i in range(columns)]for j in range(rows)]
gx=[[-1,0,1],[-2,0,2],[-1,0,1]]
gy=[[1,2,1],[0,0,0],[-1,-2,-1]]
abs_max_sum1=0
abs_max_sum2=0
abs_max_sum3=0
for i in range(1, rows-1):
    for j in range(1, columns-1):
        sum1=0
        sum2=0
        for k in range(3):
            for l in range(3):
                if i+k < rows and j+l < columns:
                    sum1=sum1+(grey_img[i+k][j+l]*gy[k][l])
                    sum2=sum2+(grey_img[i+k][j+l]*gx[k][l])
                    sum3=sqrt(sum1**2 + sum2**2)
        if abs_max_sum1<abs(sum1):
            abs_max_sum1=abs(sum1)
        if abs_max_sum2<abs(sum2):
            abs_max_sum2=abs(sum2)
        if abs_max_sum3<abs(sum3):
            abs_max_sum3=abs(sum3)
        new_img_right_sobel[i][j]=sum1
        new_img_top_sobel[i][j]=sum2
        combined[i][j]=sum3
for i in range(1, rows-1):
    for j in range(1, columns-1):
        new_img_right_sobel[i][j]=abs(new_img_right_sobel[i][j])/abs_max_sum1
        new_img_top_sobel[i][j]=abs(new_img_top_sobel[i][j])/abs_max_sum2
        combined[i][j]=abs(combined[i][j])/abs_max_sum3
cv2.imshow('right_sobel' , np.asarray(new_img_right_sobel))
cv2.imshow('top_sobel' , np.asarray(new_img_top_sobel))
cv2.imshow('sobel' , np.asarray(combined))
cv2.waitKey(0)
cv2.destroyAllWindows()
