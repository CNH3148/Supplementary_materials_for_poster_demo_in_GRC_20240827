# Code reference: https://www.youtube.com/watch?v=xjrykYpaBBM&t=632s

import cv2 as cv
import numpy as np

def empty(v):
    pass

def hsv_color_filter(img, return_result=True, return_mask=False):
    img = cv.imread(img, cv.IMREAD_UNCHANGED)

    cv.namedWindow('Color Filter')
    
    cv.createTrackbar('Hue Min', 'Color Filter', 0, 179, empty)
    cv.createTrackbar('Hue Max', 'Color Filter', 179, 179, empty)
    cv.createTrackbar('Sat Min', 'Color Filter', 89, 255, empty)
    cv.createTrackbar('Sat Max', 'Color Filter', 255, 255, empty)
    cv.createTrackbar('Val Min', 'Color Filter', 209, 255, empty)
    cv.createTrackbar('Val Max', 'Color Filter', 255, 255, empty)
    
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    while True:

        h_min = cv.getTrackbarPos('Hue Min', 'Color Filter')
        h_max = cv.getTrackbarPos('Hue Max', 'Color Filter')
        s_min = cv.getTrackbarPos('Sat Min', 'Color Filter')
        s_max = cv.getTrackbarPos('Sat Max', 'Color Filter')
        v_min = cv.getTrackbarPos('Val Min', 'Color Filter')
        v_max = cv.getTrackbarPos('Val Max', 'Color Filter')
    
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
    
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(img, img, mask=mask)
    
        cv.imshow('img', img)
        # cv.imshow('hsv', hsv)
        cv.imshow('mask', mask)
        cv.imshow('reslut', result)

        if cv.waitKey(1) == 13:  # 當按下 Enter 鍵時
            break
    
    if return_result and return_mask:
        return result, mask
    elif return_result:
        return result
    elif return_mask:
        return mask

def bgr_color_filter(img, return_result=True, return_mask=False):
    img = cv.imread(img, cv.IMREAD_UNCHANGED)

    cv.namedWindow('Color Filter')
    
    cv.createTrackbar('Blue Min', 'Color Filter', 0, 255, empty)
    cv.createTrackbar('Blue Max', 'Color Filter', 179, 255, empty)
    cv.createTrackbar('Green Min', 'Color Filter', 89, 255, empty)
    cv.createTrackbar('Green Max', 'Color Filter', 255, 255, empty)
    cv.createTrackbar('Red Min', 'Color Filter', 209, 255, empty)
    cv.createTrackbar('Red Max', 'Color Filter', 255, 255, empty)
    
    img2 = img

    while True:
        b_min = cv.getTrackbarPos('Blue Min', 'Color Filter')
        b_max = cv.getTrackbarPos('Blue Max', 'Color Filter')
        g_min = cv.getTrackbarPos('Green Min', 'Color Filter')
        g_max = cv.getTrackbarPos('Green Max', 'Color Filter')
        r_min = cv.getTrackbarPos('Red Min', 'Color Filter')
        r_max = cv.getTrackbarPos('Red Max', 'Color Filter')
    
        lower = np.array([b_min, g_min, r_min])
        upper = np.array([b_max, g_max, r_max])
    
        mask = cv.inRange(img2, lower, upper)
        result = cv.bitwise_and(img2, img2, mask=mask)
    
        cv.imshow('img2', img2)
        cv.imshow('mask', mask)
        cv.imshow('reslut', result)

        if cv.waitKey(1) == 13:  # 當按下 Enter 鍵時
            break

    if return_result and return_mask:
        return result, mask
    elif return_result:
        return result
    elif return_mask:
        return mask
    
def default_bgr_color_filter(img, return_result=False, return_mask=True):
    img = cv.imread(img, cv.IMREAD_UNCHANGED)

    b_min = 30
    b_max = 206
    g_min = 4
    g_max = 203
    r_min = 171
    r_max = 255

    lower = np.array([b_min, g_min, r_min])
    upper = np.array([b_max, g_max, r_max])

    mask = cv.inRange(img, lower, upper)
    result = cv.bitwise_and(img, img, mask=mask)

    if return_result and return_mask:
        return result, mask
    elif return_result:
        return result
    elif return_mask:
        return mask
    
def main():
    # hsv_color_filter(img)
    bgr_color_filter(img)




if __name__ == "__main__":
    img = "./images/392_20k_19.14_660ns_33.205-33.255_0.png"
    main()
else:
    print("color_filter.py imported")