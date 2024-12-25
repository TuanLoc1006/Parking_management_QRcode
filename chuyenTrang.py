from PyQt5 import QtGui , QtWidgets, QtCore
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QFileDialog,QStackedWidget
import xuLyDangKy_new,xulyQuanLyXe_3cam


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

def pageDangky(): 
    app = QApplication(sys.argv)
    main_win =  xuLyDangKy_new.MainWindow()
    main_win.show()  
    sys.exit(app.exec())

def pageQuanLy():
    app = QApplication(sys.argv)
    main_win =  xulyQuanLyXe_3cam.MainWindow()
    main_win.show()  
    sys.exit(app.exec())
    
pageDangky()

