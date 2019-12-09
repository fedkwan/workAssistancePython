#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PIL import Image
import numpy
import sys

for arg in sys.argv:
    if arg.split('.')[-1] == "png":

        img_input_filename = arg.split('\\')[-1]
        img = Image.open(arg, 'r')
        pixels_list = list(img.getdata())

        pixels_alpha_list = []
        for p in pixels_list:
            pixels_alpha_list.append(p[3])

        x1, y1, x2, y2 = 0, 0, 0, 0

        if not 0 in pixels_alpha_list:
            print("该图片不是存在透明底色的png格式图片")
            
        else:
            pixels_alpha_numpy_array = numpy.array(pixels_alpha_list).reshape(
                img.height, img.width)

            #按列分割
            columns_list = numpy.hsplit(pixels_alpha_numpy_array, img.width)
            columns_transparent_list = [0 for i in range(img.height)]
            #从左往右
            for i, arr in enumerate(columns_list):
                if not (arr.flatten() == columns_transparent_list).all():
                    x1 = i
                    break
            #从右往左
            for i, arr in enumerate(reversed(columns_list)):
                if not (arr.flatten() == columns_transparent_list).all():
                    x2 = img.width - i
                    break

            #按行分割
            rows_list = numpy.vsplit(pixels_alpha_numpy_array, img.height)
            rows_transparent_list = numpy.array([0 for i in range(img.width)])
            #从上往下
            for i, arr in enumerate(rows_list):
                if not (arr[0] == rows_transparent_list).all():
                    y1 = i
                    break
            #从下往上
            for i, arr in enumerate(reversed(rows_list)):
                if not (arr[0] == rows_transparent_list).all():
                    y2 = img.height - i
                    break

        #执行切割        
        img_out = img.crop((x1, y1, x2, y2))
        img_out_filename = arg.split('\\')[-1].split('.')[0] + "_out.png"
        img_out_path = arg.replace(img_input_filename, img_out_filename)
        img_out.save(img_out_path)