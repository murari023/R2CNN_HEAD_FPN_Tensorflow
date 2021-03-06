# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import cv2
from libs.label_name_dict.label_dict import LABEl_NAME_MAP
import math


def show_boxes_in_img(img, boxes_and_label):
    '''

    :param img:
    :param boxes: must be int
    :return:
    '''
    boxes_and_label = boxes_and_label.astype(np.int64)
    img = np.array(img, np.float32)
    img = np.array(img*255/np.max(img), np.uint8)
    for box in boxes_and_label:
        ymin, xmin, ymax, xmax, label = box[0], box[1], box[2], box[3], box[4]

        category = LABEl_NAME_MAP[label]

        color = (np.random.randint(255), np.random.randint(255), np.random.randint(255))
        cv2.rectangle(img,
                      pt1=(xmin, ymin),
                      pt2=(xmax, ymax),
                      color=color)
        cv2.putText(img,
                    text=category,
                    org=((xmin+xmax)//2, (ymin+ymax)//2),
                    fontFace=1,
                    fontScale=1,
                    color=(0, 0, 255))

    cv2.imshow('img_', img)
    cv2.waitKey(0)


def draw_box_cv(img, boxes, labels, scores):
    img = img + np.array([103.939, 116.779, 123.68])
    boxes = boxes.astype(np.int64)
    labels = labels.astype(np.int32)
    img = np.array(img, np.float32)
    img = np.array(img*255/np.max(img), np.uint8)

    num_of_object = 0
    for i, box in enumerate(boxes):
        ymin, xmin, ymax, xmax = box[0], box[1], box[2], box[3]

        label = labels[i]
        if label != 0:
            num_of_object += 1
            # color = (np.random.randint(255), np.random.randint(255), np.random.randint(255))
            color = (0, 255, 0)
            cv2.rectangle(img,
                          pt1=(xmin, ymin),
                          pt2=(xmax, ymax),
                          color=color,
                          thickness=2)
            category = LABEl_NAME_MAP[label]

            if scores is not None:
                cv2.rectangle(img,
                              pt1=(xmin, ymin),
                              pt2=(xmin + 120, ymin + 15),
                              color=color,
                              thickness=-1)
                cv2.putText(img,
                            text=category+": "+str(scores[i]),
                            org=(xmin, ymin+10),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))
            else:
                cv2.rectangle(img,
                              pt1=(xmin, ymin),
                              pt2=(xmin + 40, ymin + 15),
                              color=color,
                              thickness=-1)
                cv2.putText(img,
                            text=category,
                            org=(xmin, ymin + 10),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))
    cv2.putText(img,
                text=str(num_of_object),
                org=((img.shape[1]) // 2, (img.shape[0]) // 2),
                fontFace=3,
                fontScale=1,
                color=(255, 0, 0))
    return img


def draw_rotate_box_cv(img, boxes, labels, scores, head):
    img = img + np.array([103.939, 116.779, 123.68])
    boxes = boxes.astype(np.int64)
    labels = labels.astype(np.int32)
    img = np.array(img, np.float32)
    img = np.array(img*255/np.max(img), np.uint8)

    num_of_object = 0
    for i, box in enumerate(boxes):
        y_c, x_c, h, w, theta = box[0], box[1], box[2], box[3], box[4]

        label = labels[i]
        if label != 0:
            num_of_object += 1
            # color = (np.random.randint(255), np.random.randint(255), np.random.randint(255))
            color = (0, 255, 0)
            rect = ((x_c, y_c), (w, h), theta)
            rect = cv2.boxPoints(rect)
            rect = np.int0(rect)
            cv2.drawContours(img, [rect], -1, color, 2)

            category = LABEl_NAME_MAP[label]

            if scores is not None:
                # cv2.rectangle(img,
                #               pt1=(x_c, y_c),
                #               pt2=(x_c + 120, y_c + 15),
                #               color=color,
                #               thickness=-1)
                cv2.putText(img,
                            text=category+": "+str(scores[i]),
                            org=(x_c, y_c+10),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))
                cv2.putText(img,
                            text="head:{} angle:{}".format(head[i], theta),
                            org=(x_c, y_c + 30),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))
            else:
                # cv2.rectangle(img,
                #               pt1=(x_c, y_c),
                #               pt2=(x_c + 40, y_c + 15),
                #               color=color,
                #               thickness=-1)
                # cv2.putText(img,
                #             text=category,
                #             org=(x_c, y_c + 10),
                #             fontFace=1,
                #             fontScale=1,
                #             thickness=2,
                #             color=(color[1], color[2], color[0]))
                cv2.putText(img,
                            text="head:{} angle{}".format(head[i], theta),
                            org=(x_c, y_c + 30),
                            fontFace=1,
                            fontScale=1,
                            thickness=2,
                            color=(color[1], color[2], color[0]))
            img = draw_head(img, box, head[i], color)
    cv2.putText(img,
                text=str(num_of_object),
                org=((img.shape[1]) // 2, (img.shape[0]) // 2),
                fontFace=3,
                fontScale=1,
                color=(255, 0, 0))
    return img


def print_tensors(tensor, tensor_name):

    def np_print(ary):
        ary = ary + np.zeros_like(ary)
        print(tensor_name + ':', ary)

        print('shape is: ',ary.shape)
        print(10*"%%%%%")
        return ary
    result = tf.py_func(np_print,
                        [tensor],
                        [tensor.dtype])
    result = tf.reshape(result, tf.shape(tensor))
    result = tf.cast(result, tf.float32)
    sum_ = tf.reduce_sum(result)
    tf.summary.scalar('print_s/{}'.format(tensor_name), sum_)


def draw_head(img, box, head_quadrant, color):
    y_c, x_c, h, w, theta = box[0], box[1], box[2], box[3], box[4]
    if w > h:
        point1_x, point1_y = w / 2., - h / 2.
        point2_x, point2_y = w / 2., h / 2.
        point3_x, point3_y = w / 2. + np.sqrt(8.) * h / 2., 0.
        if head_quadrant == 1:
            angle = theta
        else:
            angle = theta - 180
    else:
        point1_x, point1_y = w / 2., h / 2.
        point2_x, point2_y = - w / 2., h / 2.
        point3_x, point3_y = 0, h / 2. + np.sqrt(8.) * w / 2.
        if head_quadrant == 0:
            angle = theta
        else:
            angle = theta - 180
    angle = angle / 180. * math.pi
    point1_x_ = np.cos(angle) * point1_x - np.sin(angle) * point1_y + x_c
    point1_y_ = np.sin(angle) * point1_x + np.cos(angle) * point1_y + y_c
    point2_x_ = np.cos(angle) * point2_x - np.sin(angle) * point2_y + x_c
    point2_y_ = np.sin(angle) * point2_x + np.cos(angle) * point2_y + y_c
    point3_x_ = np.cos(angle) * point3_x - np.sin(angle) * point3_y + x_c
    point3_y_ = np.sin(angle) * point3_x + np.cos(angle) * point3_y + y_c
    img = cv2.line(img, (int(point1_x_), int(point1_y_)), (int(point2_x_), int(point2_y_)),
                   color=color, thickness=2)
    img = cv2.line(img, (int(point2_x_), int(point2_y_)), (int(point3_x_), int(point3_y_)),
                   color=color, thickness=2)
    img = cv2.line(img, (int(point3_x_), int(point3_y_)), (int(point1_x_), int(point1_y_)),
                   color=color, thickness=2)
    return img
