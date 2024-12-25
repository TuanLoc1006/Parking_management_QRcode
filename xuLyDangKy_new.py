import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QFileDialog,QMessageBox
from dangKy_new import Ui_MainWindow
from PyQt5.QtGui import QPixmap

import xulyQuanLyXe_3cam

# import tao ma qr
import qrcode
from PIL import Image
#ket noi voi xampp
import mysql.connector

# import regex
import re


mydb = mysql.connector.connect(
    host='localhost',
    username='root',
    password='',
    port='3306',
    database='project_qrcode'
)


# link_name_user_pic = []

# link_name_xe_pic = []
class MainWindow:
   
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        
        self.uic.btn_imgUser.clicked.connect(self.linkToUser)
        self.uic.btn_imgXe.clicked.connect(self.linkToXe)
        self.uic.btn_luuThongTin.clicked.connect(self.tao_QrCode)
        self.uic.btn_quanLy.clicked.connect(self.pageQuanLy)
        self.uic.btn_clear_input.clicked.connect(self.clear_input)

       
    def pageQuanLy(self):
        self.main_win =  xulyQuanLyXe_3cam.MainWindow()
        self.main_win.show()  

    def linkToUser(self):
        global link_name_user_pic
        #tim duong dan         
        link_name_user_pic = QFileDialog.getOpenFileName(filter='*.jpg *.png')
        #mo hinh anh len
        self.uic.label_user.setPixmap(QPixmap(link_name_user_pic[0]))
        # print('link ',link_name_user_pic)

    def linkToXe(self):
        global link_name_xe_pic
        #tim duong dan
        link_name_xe_pic = QFileDialog.getOpenFileName(filter='*.jpg *.png')   
        #mo hinh anh len
        self.uic.label_xe.setPixmap(QPixmap(link_name_xe_pic[0]))
        # print('link ',link_name_xe_pic)
      
    def clear_input(self):
        self.uic.label_user.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))
        self.uic.label_xe.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\sample\\anh_mau_xam.jpg"))
        self.uic.input_hoTen.setText('') 
        self.uic.input_maSo.setText('') 
        self.uic.input_phone.setText('') 
        self.uic.input_email.setText('') 
        self.uic.input_tenXe.setText('') 
        self.uic.input_mauXe.setText('') 
        self.uic.input_soKhung.setText('') 
        self.uic.input_soMay.setText('') 
        self.uic.input_dungTich.setText('') 
        self.uic.input_bienSo.setText('') 
           
    def tao_QrCode(self):
        if self.check_information() == 10:
            createQR = 1
            name = self.uic.input_hoTen.text()
            maSo = self.uic.input_maSo.text()
            bienSo = self.uic.input_bienSo.text()
            loaiXe = self.uic.input_loaiXe.currentText()

            soDienThoai = self.uic.input_phone.text()
            email = self.uic.input_email.text()
            ngayDangky = self.uic.input_ngayDk.text()
            gioiTinh = self.uic.input_gioiTinh.currentText()
            tenXe = self.uic.input_tenXe.text()
            mauXe = self.uic.input_mauXe.text()
            soKhung = self.uic.input_soKhung.text()
            soMay = self.uic.input_soMay.text()
            dungTich = self.uic.input_dungTich.text()
            thoiHan = self.uic.input_thoiHanDK.currentText()


            qr = qrcode.QRCode(version=5,error_correction=qrcode.ERROR_CORRECT_M,box_size=5,border=3)
            maQr = str(hash(name+maSo+bienSo+loaiXe))
            qr.add_data(maQr)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black',black_color='white')
            img.save("C:\\project_qrcode_old_3cam\\img\\user\\"+maQr+".png")
            anh_user = ""
            anh_xe = ""

            try:
                anh_user = link_name_user_pic[0]
                anh_xe = link_name_xe_pic[0]
            except NameError:
                msg = QMessageBox()
                msg.setText("Bạn chưa chọn ảnh đăng ký!!!")
                msg.exec_()
                createQR = 0            
            
            if createQR != 0:
            #mo hinh anh QRcode len
                self.uic.label_qr.setPixmap(QPixmap("C:\\project_qrcode_old_3cam\\img\\user\\"+maQr+".png"))
                if mydb.is_connected():
                    mycursor = mydb.cursor()                        
                    mycursor.execute("SELECT phi_xe FROM `bang_gia` WHERE loai_xe=%s",(loaiXe,))
                    # mydb.commit()
                    gia = mycursor.fetchone()
                    mycursor.execute("INSERT INTO `user`(`mssv`, `ten`, `anh_nguoi_dang_ky`, `gioi_tinh`, `ma_qr`, `ngay_dang_ky`, `thoi_han`, `sdt`, `email`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (maSo, name, anh_user, gioiTinh, maQr, ngayDangky, thoiHan, soDienThoai, email))

                if thoiHan == "3 phút" :
                    mycursor.execute("UPDATE `user` SET `ngay_het_han`= DATE_ADD(ngay_dang_ky, INTERVAL 3 HOUR_MINUTE) WHERE mssv= %s",(maSo,))
                    gia1 = gia[0]*1
                elif thoiHan == "1 ngày" :
                    mycursor.execute("UPDATE `user` SET `ngay_het_han`= DATE_ADD(ngay_dang_ky, INTERVAL 1 DAY) WHERE mssv= %s",(maSo,))
                    gia1 = gia[0]*1
                elif thoiHan == "1 tuần" :
                    mycursor.execute("UPDATE `user` SET `ngay_het_han`= DATE_ADD(ngay_dang_ky, INTERVAL 1 WEEK) WHERE mssv= %s",(maSo,))
                    gia1 = gia[0]*7
                elif thoiHan == "1 tháng" :
                    mycursor.execute("UPDATE `user` SET `ngay_het_han`= DATE_ADD(ngay_dang_ky, INTERVAL 1 MONTH) WHERE mssv= %s",(maSo,))
                    gia1 = gia[0]*30
                elif thoiHan == "1 học kì" :
                    mycursor.execute("UPDATE `user` SET `ngay_het_han`= DATE_ADD(ngay_dang_ky, INTERVAL 5 MONTH) WHERE mssv= %s",(maSo,))
                    gia1 = gia[0]*150
                elif thoiHan == "1 năm" :
                    mycursor.execute("UPDATE `user` SET `ngay_het_han`= DATE_ADD(ngay_dang_ky, INTERVAL 1 YEAR) WHERE mssv= %s",(maSo,))
                    gia1 = gia[0]*30*12


                mycursor.execute("INSERT INTO `phuong_tien`(`bien_so`, `mssv`, `loai_xe`, `ten_xe`, `mau_xe`, `anh_xe_dang_ky`, `dung_tich`, `so_khung`, `so_may` ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (bienSo, maSo, loaiXe, tenXe, mauXe, anh_xe, dungTich, soKhung, soMay ))
                mydb.commit()
                print(type(gia1))
                mycursor.execute("UPDATE `user` SET phi_nop=%s WHERE mssv=%s" ,(gia1 ,maSo))
                mydb.commit()
            else:
                print("error updating")

    def updatePhinop(self,loaiXe,maSo):
        if mydb.is_connected():
            mycursor = mydb.cursor()
            if (loaiXe == '3 phút'):
                    mycursor.execute("UPDATE user SET phi_nop = 1*(SELECT bang_gia.phi_xe FROM bang_gia, phuong_tien,user WHERE phuong_tien.loai_xe = bang_gia.loai_xe AND phuong_tien.mssv = user.mssv AND user.mssv=%s)", (maSo))
                    mydb.commit()
            elif (loaiXe == '1 ngày'):
                    mycursor.execute("UPDATE user SET phi_nop = 1*(SELECT bang_gia.phi_xe FROM bang_gia, phuong_tien,user WHERE phuong_tien.loai_xe = bang_gia.loai_xe AND phuong_tien.mssv = user.mssv AND user.mssv=%s)", (maSo))
                    mydb.commit()
            elif (loaiXe == '1 tuần'):
                    mycursor.execute("UPDATE user SET phi_nop = 7*(SELECT bang_gia.phi_xe FROM bang_gia, phuong_tien,user WHERE phuong_tien.loai_xe = bang_gia.loai_xe AND phuong_tien.mssv = user.mssv AND user.mssv=%s)", (maSo))
                    mydb.commit()
            elif (loaiXe == '1 tháng'):
                    mycursor.execute("UPDATE user SET phi_nop = 30*(SELECT bang_gia.phi_xe FROM bang_gia, phuong_tien,user WHERE phuong_tien.loai_xe = bang_gia.loai_xe AND phuong_tien.mssv = user.mssv AND user.mssv=%s)" , (maSo))
                    mydb.commit()
            elif (loaiXe == '1 học kì'):
                    mycursor.execute("UPDATE user SET phi_nop = 30*5*(SELECT bang_gia.phi_xe FROM bang_gia, phuong_tien,user WHERE phuong_tien.loai_xe = bang_gia.loai_xe AND phuong_tien.mssv = user.mssv AND user.mssv=%s)", (maSo))
                    mydb.commit()
            elif (loaiXe == '1 năm'):
                    mycursor.execute("UPDATE user SET phi_nop = 30*12*(SELECT bang_gia.phi_xe FROM bang_gia, phuong_tien,user WHERE phuong_tien.loai_xe = bang_gia.loai_xe AND phuong_tien.mssv = user.mssv AND user.mssv='b2004732')")
                    mydb.commit()


    regex_email = re.compile(r"^[A-Za-z0-9\.\+\_-]+@[A-Za-z0-9\._-]+\.[A-Za-z]+$")
    def validate_email(self,email):
        # Sử dụng phương thức fullmatch để so khớp với chuỗi
        if self.regex_email.fullmatch(email):
            return True
        else:
            return False
        
    regex_name = re.compile(r"^[A-Za-z\s'-]+$")
    def validate_name(self,name):
        if self.regex_name.fullmatch(name) and not self.uic.input_hoTen.text().isspace():
            return True
        else:
            self.uic.input_hoTen.setFocus()
            return False
     
    def check_information(self,):
        count = 0
        message = ""
        if self.validate_email(self.uic.input_email.text()):
            count+=1
        else:
            message+= ('Email bạn nhập không đúng\n')
        
        if self.validate_name(self.uic.input_hoTen.text()):
            count+=1
        else:
            message+= ('Bạn chưa nhập họ tên\n')
        if len(str(self.uic.input_phone.text()))<12:
            message+=('SDT bạn nhập chưa chưa đúng\n')
        else: 
            count+=1
        if len(str(self.uic.input_maSo.text()))==0:
            message+=('MSSV bạn nhập chưa chưa đúng\n')
        else: 
            count+=1

        if len(str(self.uic.input_tenXe.text()))==0:
            message+=('Bạn chưa nhập tên xe\n')
        else: 
            count+=1
        if len(str(self.uic.input_mauXe.text()))==0:
            message+=('Bạn chưa nhập màu xe\n')
        else: 
            count+=1

        if len(str(self.uic.input_bienSo.text()))==0:
            message+=('Bạn chưa nhập biển số\n')
        else: 
            count+=1

        if len(str(self.uic.input_soKhung.text()))==0:
            message+=('Bạn chưa nhập số khung\n')
        else: 
            count+=1
        if len(str(self.uic.input_soMay.text()))==0:
            message+=('Bạn chưa nhập số máy\n')
        else: 
            count+=1
        if len(str(self.uic.input_dungTich.text()))==0 :
            message+=('Bạn chưa nhập dung tích\n')
        else: 
            count+=1
       
        # if anh_hop_le == False:
        #     message+=('Bạn chưa chọn ảnh đăng ký\n')

        # else:
        #     count+=1
       
        print("so luong input checked: ",count)
        if(count<10):
            msg = QMessageBox()
            message+=('Vui lòng nhập lại!!!\n')
            msg.setText(message)
            msg.exec_()
        
        return count
          

    def show(self):
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
