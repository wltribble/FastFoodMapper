#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Name: Will Tribble
 Student ID: 10540462
 Email: wltribbl@go.olemiss.edu
 Course Information: CSCI 343 - Section 01
 Program Source File Name: main.py
 Programming Assignment: 04
 References: stackoverflow.com for rounding, everything else was from the book or class notes
 Program Description: this program takes sampled restaurant names and predicts where to find more of them
 Due Date: Friday, 4/12/2017, 11:59 am

 In keeping with the honor code policies of the University of Mississippi, the School of
 Engineering, and the Department of Computer and Information Science, I affirm that I have
 neither given nor received assistance on this programming assignment. This assignment
 represents my individual, original effort.
 ... My Signature is on File.
"""

# import statements
from __future__ import division

from PIL import Image
import matplotlib.pyplot as mplot
import numpy as np
import math


# define the distance formula for later
def distance(point1, point2):
    under_radical = math.pow(point1[0]-point2[0], 2)+math.pow(point1[1]-point2[1], 2)
    return math.sqrt(under_radical)


def check_pixel_color(image, row, col, color_index):
    return image[row][col][color_index]


# reading in the reference photo and making it a float32 list
reference_img = Image.open("data_ch4knn/data.png")
reference_img = np.float32(reference_img)

# reading in the reconstruction photo and making it a float32 list
reconstruction_img = Image.open("data_ch4knn/us_outline.png")
reconstruction_img = np.float32(reconstruction_img)
# creating the final image from the reconstruction image
final_img = reconstruction_img

# create an emtpy list of data points and add the raw data points from the data file
dataPoints = []
for row in range(len(reference_img)):
    for col in range(len(reference_img[row])):
        reference_img_red_value = check_pixel_color(reference_img, row, col, 0)
        reference_img_green_value = check_pixel_color(reference_img, row, col, 1)
        reference_img_blue_value = check_pixel_color(reference_img, row, col, 2)

        if reference_img_red_value == 0 and reference_img_green_value == 255 and reference_img_blue_value == 0:
            continue
        else:
            dataPoints.append([row, col, reference_img_red_value, reference_img_green_value, reference_img_blue_value])

# get a k value to use from the user, and ensure that it is a natural number 1
k = input("Enter a k value: ")
k = float(k)
k = round(k, 0)
if k < 1:
    k = 1
k = int(k)

# loop through reconstruction image
for row in range(len(reference_img)):
    for col in range(len(reference_img[row])):
        # if the pixel is NOT green, continue
        if ((reconstruction_img[row][col][0] == 0) and (reconstruction_img[row][col][1] == 255) and (reconstruction_img[row][col][2] == 0)):
            # loop through the data points and add their colors and distances from the test point to a list
            test_distance = []
            for index in range(0, len(dataPoints)):
                test_distance.append([distance((row, col), (dataPoints[index][0], dataPoints[index][1])), dataPoints[index][2], dataPoints[index][3], dataPoints[index][4]])
            # sort and trim the distance list
            test_distance.sort(key=lambda pixel: pixel[0])
            test_distance = test_distance[0:k]
            # calculate the average RGB values for the pixel from the REFERENCE image
            red_sum = 0
            green_sum = 0
            blue_sum = 0
            for index in range(0, len(test_distance)):
                red_sum += test_distance[index][1]
                green_sum += test_distance[index][2]
                blue_sum += test_distance[index][3]
            final_img[row][col] = [(red_sum / k), (green_sum / k), (blue_sum / k)]

# plot the final image
final_img = np.uint8(final_img)
mplot.imshow(final_img)
mplot.show()
