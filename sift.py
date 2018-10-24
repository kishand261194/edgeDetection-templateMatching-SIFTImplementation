import numpy as np
from math import sqrt
from math import exp
import cv2

def get_gauss(sigma):
    gauss_val = [[None for i in range(7)]for j in range(7)]
    correction=0
    for m, i in enumerate(range(3,-4,-1)):
        for n, j in enumerate(range(-3, 4, 1)):
            gauss_val[m][n]=((1/(2*(22/7)*sigma*sigma))*((exp(-(i*i + j*j)/(2*sigma*sigma)))))
            correction+=gauss_val[m][n]
    correction=1/correction
    for i in range(7):
        for j in range(7):
            gauss_val[i][j]*=correction
    return gauss_val

def normalize(new_img, maximum=0, minimum = 0):
    for i in range(len(new_img)):
        for j in range(len(new_img[0])):
            if maximum < new_img[i][j] :
                maximum = new_img[i][j]
    for i in range(len(new_img)):
        for j in range(len(new_img[0])):
            new_img[i][j] = (new_img[i][j]-minimum)/(maximum - minimum)
    return new_img

def scale(img_arr, rows, columns, factor):
    new_rows, new_columns = int(rows*factor),int(columns*factor)
    scaled_image=[[ 0 for i in range(new_columns)]for j in range(new_rows)]
    for i in range(new_rows):
        for j in range(new_columns):
            unscaled_x = int(round(float(i)/float(new_rows)*float(rows)))
            unscaled_y = int(round(float(j)/float(new_columns)*float(columns)))
            unscaled_x = min(unscaled_x, rows-1)
            unscaled_y = min(unscaled_y, columns-1)
            scaled_image[i][j]=img_arr[unscaled_x][unscaled_y]
    return scaled_image

def write_images(images, name):
    for i, image in enumerate(images):
        filename = "image/"+name+"_%d.jpg"%i
        cv2.imwrite(filename, np.array(image, dtype = np.uint8 ))

#Reading the input file
grey_img=cv2.imread('task2.jpg', 0)
rows, columns=len(grey_img), len(grey_img[0])

#Adding the required padding
padded_img=[[ 0 for i in range(columns+6)]for j in range(rows+6)]
rows+=6
columns+=6
for i in range(3, rows-3):
    for j in range(3, columns-3):
        padded_img[i][j]=grey_img[i-3][j-3]
grey_img=padded_img

#scaling images
scale_values=[1, 0.5, 0.25, 0.125]
scaled_images=[]
for i, val in enumerate(scale_values):
    scaled_images.append(scale(grey_img, rows, columns, val))

blur_values=[[1/sqrt(2), 1, sqrt(2), 2, 2*sqrt(2)],
               [sqrt(2), 2, 2*sqrt(2), 4, 4*sqrt(2)],
               [2*sqrt(2), 4, 4*sqrt(2), 8, 8*sqrt(2)],
               [4*sqrt(2), 8, 8*sqrt(2), 16, 16*sqrt(2)]]

collect_images=[[None for i in range(5)] for j in range(4)]
log_without_nor=[[None for i in range(5)] for j in range(4)]
collect_log_images=[]

#Applying guassian blur and finding the DOG
for a, image in enumerate(scaled_images):
    for o in range(len(blur_values[0])):
        rows, columns=len(image), len(image[0])
        print(rows, columns)
        new_img = [[0 for i in range(columns)]for j in range(rows)]
        gauss_val = get_gauss(blur_values[a][o])
        for i in range(3, rows-3):
            for j in range(3, columns-3):
                sum=0
                for m in range(7):
                    for n in range(7):
                        if i+m < rows and j+n < columns:
                            sum=sum+(image[i+m][j+n]*gauss_val[m][n])
                new_img[i][j]=sum
        cv2.imwrite('image/guassian'+str(a)+'+'+str(o)+'.jpg',np.array(new_img, dtype = np.uint8 ))
        collect_images[a][o]=normalize(new_img)
        if o!=0:
            prev_image=collect_images[a][o-1]
            log_img = [[0 for i in range(columns)]for j in range(rows)]
            for i in range(rows):
                for j in range(columns):
                    log_img[i][j]=prev_image[i][j]-new_img[i][j]
            collect_log_images.append(log_img)
write_images(collect_log_images, 'dog')
imgs, max_min , q = collect_log_images, [], 0
collect=[]
for k in range(0,16,4):
    for h in range(2):
        one_image, two_image, three_image=imgs[k+h], imgs[k+1+h], imgs[k+2+h]
        arr=[[0 for i in range(len(imgs[k+h][0]))] for j in range(len(imgs[k+h]))]
        for i in range(3, len(imgs[k+h])-3):
            for j in range(3, len(imgs[k+h][0])-3):
                points  =   [one_image[i+1][j+1],one_image[i+1][j],one_image[i+1][j-1],one_image[i][j+1],
                             one_image[i][j],one_image[i][j-1],one_image[i-1][j+1],one_image[i-1][j],
                             one_image[i-1][j-1],three_image[i+1][j+1],three_image[i+1][j],three_image[i+1][j-1],
                             three_image[i][j+1],three_image[i][j],three_image[i][j-1],three_image[i-1][j+1],
                             three_image[i-1][j],three_image[i-1][j-1], two_image[i+1][j+1],two_image[i+1][j],
                             two_image[i+1][j-1],two_image[i][j+1], two_image[i][j-1],two_image[i-1][j+1],
                             two_image[i-1][j],two_image[i-1][j-1]]
                maximum, minimum = max(points), min(points)
                if(maximum<two_image[i][j] or minimum>two_image[i][j]):
                    scaled_images[q][i][j],arr[i][j]=255,255
                    collect.append([i,j])
        max_min.append(arr)
    print(sorted(collect, key= lambda x: x[1])[:5])
    collect=[]
    q+=1
write_images(max_min, 'key_points')
write_images(scaled_images, 'result')
