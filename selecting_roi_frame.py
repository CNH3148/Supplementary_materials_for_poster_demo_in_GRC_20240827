# -*- coding: utf-8 -*-
""" """

import cv2 as cv

class ROISelector():
    def __init__(self, img):
        self.__img = cv.imread(img)       # 原始影像；限傳入影像路徑
        self.__img2 = self.__img.copy()   # 第一個繪圖層 ()
        self.__img3 = self.__img2.copy()  # 第二個繪圖層 (用於顯示即時動畫)
        self.__start_x = None             # 起始點的 x 座標
        self.__start_y = None             # 起始點的 y 座標
        self.__end_x = None               # 結束點的 x 座標
        self.__end_y = None               # 結束點的 y 座標
        self.frame_lists = []             # 儲存選取的 ROI 座標 (起點、終點)
        self.__drawing = False            # 是否正在繪製矩形

    def select_roi_and_draw_frame(self, event, x, y, flags, param):
        """
        Handle mouse events to select a region of interest (ROI) and draw a frame.

        This method is designed to be used as a callback for OpenCV mouse events.
        It allows the user to select a rectangular ROI by clicking and dragging the mouse.
        The selected ROI is then drawn on the image.

        Parameters:
        event (int): The type of mouse event (e.g., cv.EVENT_LBUTTONDOWN, cv.EVENT_MOUSEMOVE, cv.EVENT_LBUTTONUP).
        x (int): The x-coordinate of the mouse event.
        y (int): The y-coordinate of the mouse event.
        flags (int): Any relevant flags passed by OpenCV.
        param (any): Any extra parameters supplied by OpenCV.

        Attributes:
        __drawing (bool): A flag indicating whether the user is currently drawing a rectangle.
        __start_x (int): The x-coordinate of the starting point of the rectangle.
        __start_y (int): The y-coordinate of the starting point of the rectangle.
        __end_x (int): The x-coordinate of the ending point of the rectangle.
        __end_y (int): The y-coordinate of the ending point of the rectangle.
        __img2 (numpy.ndarray): The original image.
        __img3 (numpy.ndarray): A copy of the original image used for drawing.
        frame_lists (list): A list of tuples containing the coordinates of the selected ROIs.

        Returns:
        None
        """

        if event == cv.EVENT_LBUTTONDOWN:             # 當點擊滑鼠左鍵
            self.__drawing = True                     # 設定正在繪製矩形
            self.__start_x, self.__start_y = x, y     # 取得起始點的座標
            print(f"Start from: ({self.__start_x}, {self.__start_y})")
        
        if event == cv.EVENT_MOUSEMOVE:               # 當滑鼠移動時
            self.__img3 = self.__img2.copy()          # 複製第二個圖層，準備在第三圖層繪圖
            cv.line(self.__img3, (x-10, y), (x+-1, y), (0, 0, 0), 1)  # 繪製游標十字，保留中心點為原始圖片之像素顏色
            cv.line(self.__img3, (x+1, y), (x+10, y), (0, 0, 0), 1)   # 同上
            cv.line(self.__img3, (x, y-10), (x, y-1), (0, 0, 0), 1)   # 同上
            cv.line(self.__img3, (x, y+1), (x, y+10), (0, 0, 0), 1)   # 同上
            cv.imshow('Please select the ROI (one or more); Then press "Enter" to finish.', self.__img3)  # 顯示繪製後的影像

            if self.__drawing:                        # 如果正在繪製矩形
                cv.rectangle(self.__img3, (self.__start_x, self.__start_y), (x, y), (0, 0, 0), 1)  # 繪製矩形
                cv.imshow('Please select the ROI (one or more); Then press "Enter" to finish.', self.__img3) # 顯示繪製後的影像

        if event == cv.EVENT_LBUTTONUP:               # 當釋放滑鼠左鍵
            self.__drawing = False                    # 設定停止繪製矩形
            self.__end_x, self.__end_y = x, y         # 取得結束點的座標
            print(f"End at: ({self.__end_x}, {self.__end_y})")
            print(f"Height × Width: {abs(self.__end_y-self.__start_y)} × {abs(self.__end_x-self.__start_x)}")
            cv.rectangle(                             # 紀錄最終的 ROI 矩形，
                self.__img2,                          # 於第一繪圖層
                (self.__start_x, self.__start_y), 
                (self.__end_x, self.__end_y), 
                (0, 255, 0), 1  
                )
            cv.imshow(                                # 顯示第一繪圖層的影像
                'Please select the ROI (one or more); Then press "Enter" to finish.', 
                self.__img2
                )

            if self.__start_x and self.__start_y and self.__end_x and self.__end_y:  # 如果有選取 ROI
                self.frame_lists.append(                                             # 儲存 ROI 座標
                    [
                        [self.__start_x, self.__start_y], 
                        [self.__end_x, self.__end_y]
                        ]
                    )
                # 清空起始與結束座標
                self.__start_x, self.__start_y, self.__end_x, self.__end_y = None, None, None, None
                print(self.frame_lists)
        
    def roi_selector(self, return_img=False):
        """
        This method displays the image in a window and sets a mouse callback to handle
        the selection of ROIs using the `select_roi_and_draw_frame` method. The user can
        select multiple ROIs by clicking and dragging the mouse. The selection process
        continues until the user presses the "Enter" key.

        Parameters:
        None

        Attributes:
        __img (numpy.ndarray): The image to be displayed for ROI selection.

        Returns:
        self.frame_lists
        """
        cv.imshow(                     # 以如下名稱之視窗開啟，並顯示讀入影像
            'Please select the ROI (one or more); Then press "Enter" to finish.', 
            self.__img
            )
        cv.setMouseCallback(
            'Please select the ROI (one or more); Then press "Enter" to finish.', 
            self.select_roi_and_draw_frame  # 重要：設定滑鼠回呼函數為上一個自訂函式
            )

        while True:
            if cv.waitKey(0) == 13:  # 當按下 Enter 鍵時
                break
        cv.destroyAllWindows()

        if return_img:
            return self.frame_lists, self.__img2
        else:
            return self.frame_lists
        
    def reorganize_frame_list(self):
        """
        This method reorganizes the frame_list attribute to ensure that the starting
        coordinates are always less than the ending coordinates.

        Parameters:
        None

        Returns:
        None
        """
        for i, frame in enumerate(self.frame_lists):
            if frame[0][0] > frame[1][0]:
                self.frame_lists[i][0][0], self.frame_lists[i][1][0] = self.frame_lists[i][1][0], self.frame_lists[i][0][0]
            if frame[0][1] > frame[1][1]:
                self.frame_lists[i][0][1], self.frame_lists[i][1][1] = self.frame_lists[i][1][1], self.frame_lists[i][0][1]
        
        return self.frame_lists

if __name__ == "__main__":  # 當此模組被當作主程式執行時
    img = "./images/392_20k_19.14_660ns_33.205-33.255_0.png"
    img_roi = ROISelector(img)
    img_roi.roi_selector()
else:
    print("selecting_roi_frame.py imported")  # 當此模組被當作模組引入時，印出此訊息