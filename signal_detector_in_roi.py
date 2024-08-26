import time
import os
import numpy as np
import cv2 as cv

import selecting_roi_frame as srf
import color_filter as cf

def main():

    # 取得 "./images/" 資料夾下的所有檔案名稱
    img_list = ["./images/" + img for img in os.listdir("./images/")]
    
    # 建立 "./outputs_當前時間/" 資料夾
    local_time = time.strftime("%Y%m%d_%H%M%S")
    output_dir = "./outputs_" + local_time + "/"
    os.makedirs(output_dir, exist_ok=True)

    for img in img_list:
        # 建立 ROISelector 物件
        img_roi = srf.ROISelector(img)
        # 選取 ROI，並取得 ROI 座標、以及畫上 ROI frame 的圖片
        frame_list, return_img = img_roi.roi_selector(return_img=True)
        frame_list = img_roi.reorganize_frame_list()

        # 取得根據預設值過濾後的 BGR 顏色遮罩
        color_mask = cf.default_bgr_color_filter(img, return_result=False, return_mask=True)
        
        # 取得 ROI 遮罩
        roi_mask = np.zeros_like(color_mask)
        for frame in frame_list:
            roi_mask[frame[0][1]:frame[1][1], frame[0][0]:frame[1][0]] = 255
        
        # 取得 ROI 遮罩與顏色遮罩的交集
        mask = cv.bitwise_and(roi_mask, color_mask)

        # 在 return_img 上，將 mask 部分的顏色設為黃色
        return_img[mask == 255] = [0, 255, 255]

        # 顯示結果
        cv.imshow("Img of signal in ROI, press \"Enter\" to next.", return_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

        # 儲存結果於 "./outputs_當前時間/" 資料夾下
        cv.imwrite(output_dir + img.split("/")[-1], return_img)

main()