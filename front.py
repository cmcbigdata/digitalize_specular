import sys
import cv2
import numpy as np
import glob
from PyQt5.QtWidgets import *

class DIMISampleApp (QWidget):
    global ori_path, new_path
    ori_path = new_path = ""
    
    def __init__ (self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("DIMI Sample Program")
        
        self.pushButton1 = QPushButton("Set original Image Directory")
        self.pushButton1.clicked.connect(self.pushButtonForOriImagePathClicked)
        self.label1 = QLabel()
        
        self.pushButton2 = QPushButton("Set New Image Directory")
        self.pushButton2.clicked.connect(self.pushButtonForNewImagePathClicked)
        self.label2 = QLabel()
        
        self.pushButton3 = QPushButton("Open Image File")
        self.pushButton3.clicked.connect(self.pushButtonForOpenImageFileClicked)
        self.label3 = QLabel()
        
        layout = QVBoxLayout()
        
        layout.addWidget(self.pushButton1)
        layout.addWidget(self.label1)
        
        layout.addWidget(self.pushButton2)
        layout.addWidget(self.label2)
        
        layout.addWidget(self.pushButton3)
        layout.addWidget(self.label3)
        
        self.setLayout(layout)
        
    def pushButtonForOriImagePathClicked(self):
        global ori_path
        ori_path = QFileDialog.getExistingDirectory(self)
        self.label1.setText(ori_path)
        
    def pushButtonForNewImagePathClicked(self):
        global new_path
        new_path = QFileDialog.getExistingDirectory(self)
        self.label2.setText(new_path)
        
    def pushButtonForOpenImageFileClicked(self):
        global x0, y0, img, isDragging, img_process
        
        fname = QFileDialog.getOpenFileName(self)
        self.label3.setText(fname[0])
        
        img = cv2.imread(fname[0])
        
        x0, y0, w, h = -1, -1, -1, -1
        blue, red = (255, 0, 0), (0, 0, 255)
        isDragging = False
        
        def onMouse (event, x, y, flags, param):
            global x0, y0, img, isDragging, img_process
            if event == cv2.EVENT_LBUTTONDOWN:
                isDragging = True
                x0 = x
                y0 = y
            elif event == cv2.EVENT_MOUSEMOVE:
                if flags == cv2.EVENT_FLAG_LBUTTON:
                    isDragging = True
                    img_draw = img_process.copy()
                    cv2.rectangle(img_draw, (x0, y0), (x, y), blue, 2)
                    cv2.imshow('img', img_draw)
            elif event == cv2.EVENT_LBUTTONUP:
                isDragging = False
                w = x-x0
                h = y-y0
                print ("x: %d, y: %d, w: %d, h: %d"%(x0, y0, w, h))
                if w>0 and h>0:
                    img_draw = img_process
                    cv2.rectangle(img_draw, (x0, y0), (x, y), red, 2)
                    cv2.imshow('img', img_draw)
                    roi = img[y0:y0+h, x0:x0+w]
                    cv2.imshow('cropped', roi)
                    cv2.moveWindow('cropped', 0, 0)
                    print('cropped')
            else:
                cv2.imshow('img', img)
                print("좌측 상단에서 우측 하단으로 영역을 드래그하세요.")
                
        cv2.imshow('img', img)
        img_process = img.copy()
        cv2.setMouseCallback('img', onMouse)
        while True:
            if cv2.waitKey(0)&0xFF == 27:
                break
            if cv2.waitKey(0) == ord('c'):
                img_process = img.copy()
                cv2.imshow('img', img_process)
        cv2.destroyAllWindows()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DIMISampleApp()
    ex.show()
    sys.exit(app.exec_())