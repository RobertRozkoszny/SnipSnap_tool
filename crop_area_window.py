from desktopmagic.screengrab_win32 import getDisplayRects, getRectAsImage
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtGui, QtCore
from PIL import Image
import pytesseract
import sys



pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

class Crop_area_window(QWidget):
    def __init__(self , main_window = None):
        super().__init__()

        self.main_window = main_window
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.are_we_snipping = False
        self.fill_all_screens_geometry()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(0.4)
        self.show()

    def get_coordinates_for_position(self, list_of_tuples):
        """Expects a list of X and Y position in the form of ex. [(x0,y0),(x1,y1)] or[(x1,y1,x2,y2),(x3,y3,x4,y4)] etc,"""
        x_axis = []
        y_axis = []
        for element in list_of_tuples:
            for i in range(0, len(element), 2):
                x_axis.append(element[i])
                y_axis.append(element[i + 1])
        return x_axis, y_axis

    def fill_all_screens_geometry(self):
        #getDisplayRects()-> something like [(0, 0, 1280, 1024), (-1280, 0, 0, 1024), (1280, -176, 3200, 1024)]
        x_axis, y_axis = self.get_coordinates_for_position(getDisplayRects())
        left, top, right, bottom = min(x_axis), min(y_axis), abs(min(x_axis)) + max(x_axis), abs(min(y_axis)) + max(y_axis)
        self.setGeometry(left, top, right, bottom)
        return

    def get_image_of_selected_area(self):
        self.start_point = self.start_point.x(), self.start_point.y()
        self.end_point = self.end_point.x(), self.end_point.y()
        x_axis, y_axis = self.get_coordinates_for_position([self.start_point, self.end_point])
        selected_area = (min(x_axis), min(y_axis), max(x_axis), max(y_axis))
        self.img = getRectAsImage(selected_area)
        self.img.save(r'images\temporary_snip_for_display.png', format='png')
        #alternate picture to get better img to text conversion
        width, heigth = self.img.size
        newsize = (width * 3, heigth * 3)
        self.img = self.img.resize(newsize, resample=Image.BICUBIC)
        self.img.save(r'images\temporary_snip.png', format='png')
        return

    def main_window_wakeup(self):
        self.main_window.present_results()

    def finish(self):
        if self.main_window != None:
            self.main_window.text_from_image = self.text
            self.main_window_wakeup()
        else:
            print(self.text)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 4, Qt.DashLine))
        painter.setBrush(QtGui.QColor(135, 206, 250))
        if self.are_we_snipping:
            painter.drawRect(QtCore.QRect(self.start_point, self.end_point))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.are_we_snipping = True
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.are_we_snipping = False

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            print('Quit')
            self.close()
            self.main_window.show()

        elif event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            self.close()
            self.get_image_of_selected_area()
            if self.main_window != None:
               language = self.main_window.language_set
            else:
                language = "eng"
            self.text = pytesseract.image_to_string(r'images\temporary_snip.png', lang=language)
            self.finish()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Crop_area_window()
    sys.exit(app.exec_())


