import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)
from PyQt5.QtWidgets import QMainWindow, QFileDialog,QStackedWidget
from quanLyGuiXe import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
# mo webcam
import cv2
from pyzbar.pyzbar import decode
import numpy as np 
# xu ly tu dong quet
detecter = cv2.QRCodeDetector()

# ket noi csdl
import mysql.connector
# goi thu vien thoi gian
import time
# goi thu vien de load anh len pixmap
from PyQt5.QtGui import QPixmap
#chuyen trang
import  xuLyDangKy_new
#tieng keu bip bip
import winsound
frequency1 = 2500  # Set Frequency To 2500 Hertz
frequency2 = 1500
duration = 700  # Set Duration To 1000 ms == 1 second
# Import smtplib module for sending email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="project_qrcode"
            )
        

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)

        self.uic.btn_openCamQR.clicked.connect(self.loadCamQR)
        self.uic.btn_closeCamQR.clicked.connect(self.closeCamQR)

        self.uic.btn_dangKy.clicked.connect(self.pageDangky)

    

    def pageDangky(self):
        #self.offCamera()
        self.main_win = xuLyDangKy_new.MainWindow()
        self.main_win.show()

    def closeCamQR(self):

        self.cam_0.release()

        
        
        
    def loadCamQR(self):

        self.cam_0 = cv2.VideoCapture(0)  
        self.cam_1 = cv2.VideoCapture(1)
        self.cam_2 = cv2.VideoCapture(2)

        checked_ma_qr = False     
        while True:
            try:

                _, self.frame_so_0 = self.cam_0.read()
                _, self.frame_so_1 = self.cam_1.read()
                _, self.frame_so_2 = self.cam_2.read()

                

                # xu ly nhan dien ma qr
                for code in decode(self.frame_so_0):
                    pts = np.array([code.polygon], np.int32)
                    pts = pts.reshape(((-1,1,2)))
                    cv2.polylines(self.frame_so_0, [pts], True, (0,0,255), 3)

                    # doc du lieu ma qr tu camera
                    ma_qr=code.data.decode('utf-8')
                    checked_ma_qr = True

                    winsound.Beep(frequency2, duration)

                    if checked_ma_qr == True:
                        limit_count = 0
                        
                        while(self.cam_0.isOpened()):
                            trang_thai_gui = self.getStatus(ma_qr)
                            #KIEM TRA XEM O TRONG CSDL CO NGUOI DUNG GUI XE CHUA

                            #TRUONG HOP 1: chua co xe trong bai
                            if(trang_thai_gui == 0):
                                time.sleep(1)
                                ret0, frame_truoc = self.cam_1.read()
                                ret1, frame_sau = self.cam_2.read()

                                img_name_truoc = "C:\\project_qrcode_old_3cam\\img\\gui_xe_vao\\"+ma_qr+"_0.png"
                                img_name_sau = "C:\\project_qrcode_old_3cam\\img\\gui_xe_vao\\"+ma_qr+"_1.png"
                                cv2.imwrite(img_name_truoc, frame_truoc)
                                cv2.imwrite(img_name_sau, frame_sau)

                                winsound.Beep(frequency1, duration)
                    
                                limit_count = 1
                                
                                if limit_count == 1:
                                    self.uic.label_anhTruocXeVao.setPixmap(QPixmap(img_name_truoc))
                                    self.uic.label_anhSauXeVao.setPixmap(QPixmap(img_name_sau))
                                    self.uic.label_anhTruocXeRa.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))
                                    self.uic.label_anhSauXeRa.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))
                                    #THEM MOT NGUOI DUNG VAO BANG 'quan ly gui xe' TRONG CSDL
                                    # self.getDataFromDB(ma_qr, trang_thai_gui)
                                    stt = self.addDataVao(ma_qr)
                                    self.addPathHinh(img_name_truoc, img_name_sau, ma_qr,trang_thai_gui)
                                    self.getDataFromDB(ma_qr, stt)
                                        
                                    break
                            

                            #TRUONG HOP 2: DA co xe trong bai
                            elif (trang_thai_gui != 0):
                                time.sleep(1)
                                ret0, frame_truoc = self.cam_1.read()
                                ret1, frame_sau = self.cam_2.read()

                                img_name_truoc = "C:\\project_qrcode_old_3cam\\img\\gui_xe_ra\\"+ma_qr+"_0.png"
                                img_name_sau = "C:\\project_qrcode_old_3cam\\img\\gui_xe_ra\\"+ma_qr+"_1.png"
                                cv2.imwrite(img_name_truoc, frame_truoc)
                                cv2.imwrite(img_name_sau, frame_sau)

                                winsound.Beep(frequency1, duration)

                                limit_count = 1
                                

                                if limit_count == 1:
                                    self.uic.label_anhTruocXeRa.setPixmap(QPixmap(img_name_truoc))
                                    self.uic.label_anhSauXeRa.setPixmap(QPixmap(img_name_sau))

                                    temp1 = 'C:\\project_qrcode_old_3cam\\img\\gui_xe_vao\\'+ma_qr+'_0.png'
                                    temp2 = 'C:\\project_qrcode_old_3cam\\img\\gui_xe_vao\\'+ma_qr+'_1.png'

                                    self.uic.label_anhTruocXeVao.setPixmap(QPixmap(temp1))
                                    self.uic.label_anhSauXeVao.setPixmap(QPixmap(temp2))

                                    # self.getDataFromDB(ma_qr, trang_thai_gui)
                                    self.addPathHinh(img_name_truoc, img_name_sau, ma_qr, trang_thai_gui)
                                    self.getDataFromDB(ma_qr, trang_thai_gui)
                                    break                                   

                        checked_ma_qr = False                       


                # hien len man hinh fram
                self.frame_so_0 = cv2.cvtColor(self.frame_so_0, cv2.COLOR_BGR2RGB)
                self.update()
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.cam_0.release()
                    self.cam_1.release()
                    self.cam_2.release()
                    cv2.destroyAllWindows()
                    break
            except IndexError:
                self.clearData()
                msg = QMessageBox()
                msg.setText('Ma QR khong dung, xin vui long quet lai!')
                msg.exec_()
            except TypeError:
                break
        
    def update(self):
        self.setPhoto(self.frame_so_0)
        

    def setPhoto(self,image):
        image = cv2.resize(image,(331,251))
        img = QtGui.QImage(image,image.shape[1],image.shape[0], image.strides[0],QtGui.QImage.Format_RGB888)
        self.uic.label_khungCamQR.setPixmap(QtGui.QPixmap.fromImage(img))
       

    def getDataFromDB(self,ma_qr,stt):
        # try:
            
        if mydb.is_connected():
            mycursor = mydb.cursor()

            sql1 = "SELECT * FROM user u join phuong_tien pt on u.mssv=pt.mssv WHERE ma_qr = %s"
            adr = (ma_qr, )
            mycursor.execute(sql1, adr)
            myresult1 = mycursor.fetchall()
            mssv = myresult1[0][0]
            bienSo = myresult1[0][11]
            hoten = myresult1[0][1]
            loaiXe =  myresult1[0][12]
            mauXe =  myresult1[0][14]

            anhNguoiDK = QPixmap(myresult1[0][2])
            anhXeDK = QPixmap(myresult1[0][16])
            mycursor.execute('SELECT * FROM `quan_ly_gui_xe` WHERE ma_qr = %s AND stt=%s' ,(ma_qr, stt,))
            myresult2 = mycursor.fetchall()
            if(stt == myresult2[0][0]):
                try:                    
                    tg_vao = str(myresult2[0][3])
                    tg_ra = str(myresult2 [0][4])
                    self.uic.input_gioVao.setText(tg_vao)
                    self.uic.input_gioRa.setText(tg_ra)
                except IndexError:
                    print("huhu")

            self.uic.input_bienSo.setText(bienSo)
            self.uic.input_hoTen.setText(hoten) 
            self.uic.input_loaiXe.setText(loaiXe)
            self.uic.input_mauXe.setText(mauXe) 
            self.uic.input_MSSV.setText(mssv)
            
            self.uic.label_anhNguoiDK.setPixmap(anhNguoiDK)
            self.uic.label_anhXe.setPixmap(anhXeDK) 
        else: print('ket noi co so du lieu khong thanh cong')


    def addDataVao(self,ma_qr):            
        if mydb.is_connected():
            mycursor = mydb.cursor()

            sql = "SELECT mssv FROM  `user` u  WHERE  u.ma_qr = %s"
            adr = (ma_qr, )
            mycursor.execute(sql, adr)
            myresult1 = mycursor.fetchall()
            try:
                mssv = myresult1[0][0]
                mycursor.execute('INSERT INTO `quan_ly_gui_xe` ( `stt`, `mssv` , `ma_qr`, `thoi_gian_vao`      ,`trang_thai`) VALUES (%s,%s,%s, NOW(),%s)' ,('', mssv, ma_qr, 'dang gui'))
                mydb.commit()
            except IndexError:
                print("hehe")

            #lay stt 
            sql = "SELECT stt FROM  `quan_ly_gui_xe` u  WHERE  u.ma_qr = %s AND u.trang_thai = 'dang gui'"
            adr = (ma_qr, )
            mycursor.execute(sql, adr)
            myresult2 = mycursor.fetchall()
            return myresult2[0][0]
            
        else: print('ket noi co so du lieu khong thanh cong')
       
    def getStatus(self,ma_qr):
        if mydb.is_connected():
            mycursor = mydb.cursor()

            sql = 'SELECT * FROM `quan_ly_gui_xe` WHERE `trang_thai` = %s And ma_qr = %s'
            adr = ('dang gui', ma_qr, )
            mycursor.execute(sql, adr)
            myresult2 = mycursor.fetchall()

            try:
                trang_thai_gui = myresult2[0][9]
                if(trang_thai_gui == 'dang gui'):
                    return myresult2[0][0]
            except IndexError:
                return 0
            
  
    def addPathHinh(self,img_name1, img_name2, ma_qr, stt):
        if mydb.is_connected():
            mycursor = mydb.cursor()
            if (img_name1.find('gui_xe_vao') == 30):
                mycursor.execute('UPDATE `quan_ly_gui_xe` SET `anh_pTruoc_luc_vao`=%s, `anh_pSau_luc_vao`=%s WHERE ma_qr=%s' ,(img_name1, img_name2, ma_qr,))
                mydb.commit()

            elif (img_name1.find('gui_xe_ra') == 30):
                mycursor.execute('UPDATE `quan_ly_gui_xe` SET `thoi_gian_ra`=NOW(), `anh_pTruoc_luc_ra`=%s, `anh_pSau_luc_ra`=%s, `trang_thai`=%s WHERE ma_qr=%s AND stt=%s ' ,(img_name1, img_name2,'da lay xe',ma_qr,stt,))
                mydb.commit()


    def clearData(self):
        self.uic.label_anhTruocXeVao.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))
        self.uic.label_anhSauXeVao.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))
        self.uic.label_anhTruocXeRa.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))
        self.uic.label_anhSauXeRa.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))
        
        self.uic.input_bienSo.setText('') 
        self.uic.input_hoTen.setText('') 
        self.uic.input_loaiXe.setText('')
        self.uic.input_mauXe.setText('') 
        self.uic.input_MSSV.setText('')
        self.uic.input_gioVao.setText('')
        self.uic.input_gioRa.setText('')
        
        self.uic.label_anhNguoiDK.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))
        self.uic.label_anhXe.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))

    def show(self):
        self.main_win.show()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_win = MainWindow()
#     main_win.show()
#     sys.exit(app.exec())

