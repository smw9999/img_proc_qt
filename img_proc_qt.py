from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage

import sys
import cv2
import numpy as np

# class Ui(QtWidgets.QDialog):
#     def __init__(self):
#         super(Ui, self).__init__()
#         uic.loadUi('img_proc_qt.ui', self)
#         self.btn_load = self.findChild(QtWidgets.QPushButton, 'btn_load')
#         self.btn_load.clicked.connect(self.btn_load_clicked)
#         self.btn_run = self.findChild(QtWidgets.QPushButton, 'btn_run')
#         self.btn_run.clicked.connect(self.btn_run_clicked)
#         self.lbl_src = self.findChild(QtWidgets.QLabel, 'lbl_src')
#         self.lbl_dst = self.findChild(QtWidgets.QLabel, 'lbl_dst')
#         self.line_edit = self.findChild(QtWidgets.QLineEdit, 'line_edit')
#         self.line_edit.clear()
#         self.show()
#
#     #cv2.imread가 한글 지원하지 않으므로 새로운 방식으로 파일 조합
#     def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
#         try:
#             n = np.fromfile(filename, dtype)
#             img = cv2.imdecode(n, flags)
#             return img
#         except Exception as e:
#             print(e)
#             return None
#
#     def btn_load_clicked(self):
#         path = 'PCB1'
#         filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
#         fname = QtWidgets.QFileDialog.getOpenFileName(self, "파일로드", path, filter)
#         filename = str(fname[0])
#         self.line_edit.setText(filename)
#         self.img_src = self.imread(filename)
#         self.display_output_image(self.img_src, 0)
#
#     def btn_run_clicked(self):
#         img_gray = cv2.cvtColor(self.img_src, cv2.COLOR_BGR2GRAY)
#         ret, img_binary = cv2.threshold(img_gray, 50, 255, cv2.THRESH_OTSU)
#         self.display_output_image(img_binary, 1)
#         img_tmp = cv2.pyrDown(img_binary)
#         cv2.imshow('dst', img_tmp)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#
#     def display_output_image(self, img, mode):
#         h, w = img.shape[:2]  # 그레이영상의 경우 ndim이 2이므로 h,w,ch 형태로 값을 얻어올수 없다
#
#         if img.ndim == 2:
#             qImg = QImage(img, w, h, w * 1, QImage.Format_Grayscale8)
#         else:
#             bytes_per_line = img.shape[2] * w
#             qImg = QImage(img, w, h, bytes_per_line, QImage.Format_BGR888)
#
#         pixmap = QtGui.QPixmap(qImg)
#         pixmap = pixmap.scaled(600, 450, QtCore.Qt.KeepAspectRatio)  # 이미지 비율유지
#         #pixmap = pixmap.scaled(600, 450, QtCore.Qt.IgnoreAspectRatio)  # 이미지를 프레임에 맞춤
#
#         if mode == 0:
#             self.lbl_src.setPixmap(pixmap)
#             self.lbl_src.update()  # 프레임 띄우기
#         else:
#             self.lbl_dst.setPixmap(pixmap)
#             self.lbl_dst.update()  # 프레임 띄우기
#
# app = QtWidgets.QApplication(sys.argv)
# window = Ui()
# app.exec_()



class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('img_proc_qt.ui', self)
        self.btn_load = self.findChild(QtWidgets.QPushButton, 'btn_load')
        self.btn_load.clicked.connect(self.btn_load_clicked)
        self.btn_run = self.findChild(QtWidgets.QPushButton, 'btn_run')
        self.btn_run.clicked.connect(self.btn_run_clicked)
        self.lbl_src = self.findChild(QtWidgets.QLabel, 'lbl_src')
        self.lbl_dst = self.findChild(QtWidgets.QLabel, 'lbl_dst')
        self.line_edit = self.findChild(QtWidgets.QLineEdit, 'line_edit')
        self.line_edit.clear()
        self.show()

    #cv2.imread가 한글 지원하지 않으므로 새로운 방식으로 파일 조합
    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None

    def btn_load_clicked(self):
        path = 'PCB1'
        filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "파일로드", path, filter)
        filename = str(fname[0])
        self.line_edit.setText(filename)
        self.img_src = self.imread(filename)
        self.display_output_image(self.img_src, 0)

    def btn_run_clicked(self):
        img_gray = cv2.cvtColor(self.img_src, cv2.COLOR_BGR2GRAY)
        img_dst=self.img_src.copy()
        ret, img_binary = cv2.threshold(img_gray, 50, 255, cv2.THRESH_OTSU)
        # circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1,
        #                            minDist=100, param1=250, param2=10,
        #                            minRadius=80, maxRadius=120)
        #
        # for i, circle in enumerate(circles[0]):
        #     # 값이 실수로 들어오므로 정수로 변환하여야 표시가 됨
        #     cv2.circle(img_dst,(int(circle[0]), int(circle[1])), int(circle[2]),(255, 255, 255), 3)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (7, 7))

        # OPENING 5번은 erode 5번 진행후 dilate 5번 진행하는것과 같다.
        img_morp1 = cv2.erode(img_binary, kernel, iterations=2)
        img_morp1 = cv2.dilate(img_morp1, kernel, iterations=5)
        contours, hierarchy = cv2.findContours(img_morp1, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

        my_color = (0, 255, 0)  # (B,G,R)
        text_color = (255, 0, 0)  # (B,G,R)
        thickness = 5


        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            # contourArea()함수로 객체의 면적을 구하고 면적기준으로 임계값보다
            # 큰 객체만 외곽선을 그리고 면적정보를 표시한다.
            if(area>10000):
                cv2.drawContours(img_dst, contours, i, my_color, thickness)
                # 모멘트 그리기(무게중심)
                mu = cv2.moments(contour)
                cx = int(mu['m10'] / (mu['m00'] + 1e-5))
                cy = int(mu['m01'] / (mu['m00'] + 1e-5))
                cv2.circle(img_dst, (cx, cy), 10, (0, 180, 255), -1)
                cv2.putText(img_dst, f'{i}: {int(area)}', (cx - 50, cy +50), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                            text_color, 2)




        self.display_output_image(img_dst, 1)
        img_tmp = cv2.pyrDown(img_dst)
        cv2.imshow('dst', img_tmp)
        # abc= cv2.pyrDown(img_binary)
        # cv2.imshow('dst1', abc)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def display_output_image(self, img, mode):
        h, w = img.shape[:2]  # 그레이영상의 경우 ndim이 2이므로 h,w,ch 형태로 값을 얻어올수 없다

        if img.ndim == 2:
            qImg = QImage(img, w, h, w * 1, QImage.Format_Grayscale8)
        else:
            bytes_per_line = img.shape[2] * w
            qImg = QImage(img, w, h, bytes_per_line, QImage.Format_BGR888)

        pixmap = QtGui.QPixmap(qImg)
        pixmap = pixmap.scaled(600, 450, QtCore.Qt.KeepAspectRatio)  # 이미지 비율유지
        #pixmap = pixmap.scaled(600, 450, QtCore.Qt.IgnoreAspectRatio)  # 이미지를 프레임에 맞춤

        if mode == 0:
            self.lbl_src.setPixmap(pixmap)
            self.lbl_src.update()  # 프레임 띄우기
        else:
            self.lbl_dst.setPixmap(pixmap)
            self.lbl_dst.update()  # 프레임 띄우기

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

