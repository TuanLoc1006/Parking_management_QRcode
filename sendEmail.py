# Import smtplib module for sending email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    username='root',
    password='',
    port='3306',
    database='project_qrcode'
)


def guiMail(ma_qr):
    if mydb.is_connected():
            mycursor = mydb.cursor()
            diachi_mail = mycursor.execute("SELECT email FROM `user` WHERE ma_qr=%s AND ngay_het_han <= NOW()" ,(ma_qr,))
            mydb.commit

    print(diachi_mail)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender = 'loclamphuongtien@gmail.com'
    password = 'auht qqzq unwj zcfv'
    receiver = diachi_mail
    smtp = smtplib.SMTP(smtp_server,smtp_port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(sender,password)
    content = "Subject: Thông báo hết hạn\nThẻ gửi xe trong kí túc xá của bạn đã hết hạn, hãy đăng ký lại để tiếp tục sử dụng dịch vụ nhé!!!"

    smtp.sendmail(sender,receiver,content.encode('utf-8'))
    quit = smtp.quit()
    print("Da gui mail thanh cong !!!")
    


