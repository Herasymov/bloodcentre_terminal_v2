import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QLabel, QApplication, QMessageBox, QVBoxLayout, QListWidget, QScrollArea, QGridLayout,
                             QPushButton, QFrame, QSplitter, QLineEdit, QRadioButton, QComboBox, QCalendarWidget,QDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import sqlite3
import pyodbc
import os
import subprocess
from datetime import datetime, timedelta
import numpy as np


conn_str = 'db.db'

class View(QMainWindow):
    def __init__(self, model):
        super(View, self).__init__()
        self.m = model
        self.initUI()
    def initUI(self):
        self.setMaximumSize(450, 150)
        self.setMinimumSize(450, 150)
        self.setWindowTitle('Choose your role')
        self.setGeometry(600, 350, 450, 150)

        font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)

        self.LogInButton = QPushButton('CLIENT', self)
        self.LogInButton.resize(180,60)
        self.LogInButton.move(40, 40)
        self.LogInButton.setFont(QtGui.QFont("Times", 13, QtGui.QFont.Bold))
        self.LogInButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.LogInButton.clicked.connect(self.clientch)

        self.LogInButton = QPushButton('ADMIN', self)
        self.LogInButton.resize(180,60)
        self.LogInButton.move(240, 40)
        self.LogInButton.setFont(QtGui.QFont("Times", 13, QtGui.QFont.Bold))
        self.LogInButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(20, 150, 55); color:white;}')
        self.LogInButton.clicked.connect(self.admin)

    def clientch(self):
        w = Startpage(self.m)
        w.fir_step()
        w.exec_()
        self.close()

    def admin(self):
        subprocess.Popen([sys.executable, "Display.py"])
        self.close()

class Startpage(QDialog):
    def __init__(self, model):
        super(Startpage, self).__init__()
        self.m = model
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Register form")
        self.setMaximumSize(1360,820)
        self.setMinimumSize(1360,820)
        self.setGeometry(140,0, 1360,820)
        self.setStyleSheet("background-color: white")

        self.name=""
        self.cldata=[]
        self.que = Queue([])
        self.m.createQueque(self.que)

        self.bkgrnd = QLabel(self)
        self.pixmap=QPixmap("Images/blood-bank.jpg")
        self.bkgrnd.setPixmap(self.pixmap)
        self.bkgrnd.setGeometry(900,250,self.pixmap.width(), self.pixmap.height())

        self.header = QFrame(self)
        self.header.setGeometry(0,0,1360,150)
        self.header.setStyleSheet("background-color: #E4FFF9")

        self.logo = QLabel(self.header)
        self.pixmap=QPixmap("Images/logo_ma.png")
        self.logo.setPixmap(self.pixmap)
        self.logo.setGeometry(500,0,self.pixmap.width(), self.pixmap.height())


        self.centre = QFrame(self)
        self.centre.setGeometry(450,180,460,575)
        self.centre.setStyleSheet("background-color: #B5FBDD")

        self.text = QLabel('Welcome to our centre!', self.centre)
        self.text.move(60, 15)
        self.text.setStyleSheet('color:black')
        self.text.setFont(QtGui.QFont("Times", 27))

        #----------------1 step------------
        self.application = QPushButton('Getting an Appointment', self.centre)
        self.application.resize(460,100)
        self.application.move(0, 75)
        self.application.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.application.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.application.clicked.connect(self.sec_step)

        self.checkqueue = QPushButton('Check Queue', self.centre)
        self.checkqueue.resize(460,100)
        self.checkqueue.move(0, 175)
        self.checkqueue.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.checkqueue.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.checkqueue.clicked.connect(self.chqueue)
        #----------------2 step------------
        self.regist = QPushButton('Sign up', self.centre)
        self.regist.resize(460,100)
        self.regist.move(0, 75)
        self.regist.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.regist.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.regist.clicked.connect(self.registr)

        self.login = QPushButton('Sign in', self.centre)
        self.login.resize(460,100)
        self.login.move(0, 175)
        self.login.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.login.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.login.clicked.connect(self.logina)
        self.back = QPushButton('Go to previous page', self.centre)
        self.back.resize(460,100)
        self.back.move(0, 275)
        self.back.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.back.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.back.clicked.connect(self.fir_step)
        #----------------3 step------------
        self.getanapp = QPushButton('Getting an appointment', self.centre)
        self.getanapp.resize(460,100)
        self.getanapp.move(0, 75)
        self.getanapp.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.getanapp.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.getanapp.clicked.connect(self.funcappoint)

        self.updacc = QPushButton('View, update account', self.centre)
        self.updacc.resize(460,100)
        self.updacc.move(0, 175)
        self.updacc.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.updacc.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.updacc.clicked.connect(self.changeAccount)

        self.history = QPushButton('View History', self.centre)
        self.history.resize(460,100)
        self.history.move(0, 275)
        self.history.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.history.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.history.clicked.connect(self.hist)

        self.logout = QPushButton('Log out', self.centre)
        self.logout.resize(460,100)
        self.logout.move(0, 475)
        self.logout.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.logout.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(100, 52, 155); color:white;}')
        self.logout.clicked.connect(self.fir_step)

        self.bottom = QFrame(self)
        self.bottom.setGeometry(0,770,1360,50)
        self.bottom.setStyleSheet("background-color: #E4FFF9")

        self.contact= QLabel('Contact details  Address:  26 Margaret Street London  W1W 8NB  Phone: 0300 123 23 23', self.bottom)
        self.contact.move(70, 0)
        self.contact.setStyleSheet('color:black')
        self.contact.setFont(QtGui.QFont("Times", 25))

        print(self.cldata)
    def fir_step(self):
        self.text.setText("Welcome to our centre!")
        self.application.setVisible(True)
        self.checkqueue.setVisible(True)
        self.regist.setVisible(False)
        self.login.setVisible(False)
        self.logout.setVisible(False)
        self.back.setVisible(False)
        self.getanapp.setVisible(False)
        self.updacc.setVisible(False)
        self.history.setVisible(False)
        self.checkqueue.move(0, 175)
        self.centre.setGeometry(450,180,460,275)

    def sec_step(self):
        self.text.setText("Welcome to our centre!")
        self.application.setVisible(False)
        self.checkqueue.setVisible(False)
        self.regist.setVisible(True)
        self.login.setVisible(True)
        self.logout.setVisible(False)
        self.back.setVisible(True)
        self.getanapp.setVisible(False)
        self.updacc.setVisible(False)
        self.history.setVisible(False)
        self.centre.setGeometry(450,180,460,375)

    def third_step(self):
        self.name = self.cl.getName()
        self.text.setText('Welcome, '+ self.name + "!")
        print(self.cldata)
        self.application.setVisible(False)
        self.checkqueue.setVisible(True)
        self.regist.setVisible(False)
        self.login.setVisible(False)
        self.logout.setVisible(True)
        self.back.setVisible(False)
        self.getanapp.setVisible(True)
        self.updacc.setVisible(True)
        self.history.setVisible(True)
        self.checkqueue.move(0, 375)
        self.centre.setGeometry(450,180,460,575)

    def funcappoint(self):
        str = self.m.addtoQueque(self.cl, self.que)
        w = WarningW()
        w.label.setText(str)
        w.label.move(20,35)
        w.move(500,400)
        w.resize(400,100)
        w.okButton.move(150,70)
        w.exec_()
        print(self.que.getQueue())

    def hist(self):
        w = HistoryForm(self.m, self.cl)
        w.exec_()

    def chqueue(self):
        w = QueueForm(self.que)
        w.exec_()
    def registr(self):
        w = RegisterForm(self.m)
        w.exec_()
        self.name = w.NameEntry.text()
        if (self.name!=""):
            self.cl=w.cl
            self.third_step()

    def logina(self):
        w = LoginForm(self.m)
        w.exec_()
        if (w.count1!=0):
            self.cl=w.cl
            self.third_step()

    def changeAccount(self):
        self.w1 = RegisterForm(self.m)
        self.w1.setWindowTitle("Account information")
        self.w1.submitButton.setVisible(False)
        self.w1.changeButton.setVisible(True)
        self.w1.changeButton.clicked.connect(self.confirm)
        self.w1.NameEntry.setText(self.cl.getName())
        self.w1.ageButton.setText(str(self.cl.getAge()))
        self.w1.gender.gender = str(self.cl.getGender())
        self.w1.locationEntry.setText(self.cl.getLocation())
        self.w1.phoneEntry.setText(str(self.cl.getPhone()))
        self.w1.weighEntry.setCurrentText(str(self.cl.getWeigh()))
        self.w1.bloodEntry.setCurrentIndex(self.cl.getBlood())
        self.w1.passwordEntry.setText(self.cl.getPassword())
        self.w1.exec_()

    def confirm(self):
        if self.w1.NameEntry.text() == "" or self.w1.ageButton.text() == "Select date"or self.w1.locationEntry.text() == "" or self.w1.weighEntry.currentText() == "Select" or self.w1.bloodEntry.currentText() == "Select" or self.w1.passwordEntry.text() == ""or self.w1.phoneEntry.text() == "":
            w = WarningW()
            w.move(640,400)
            w.exec_()
        else:
            conn = sqlite3.connect(conn_str)
            name = self.w1.NameEntry.text()
            age = self.w1.ageButton.text()
            gender = self.w1.gender.gender
            location = self.w1.locationEntry.text()
            weigh = self.w1.weighEntry.currentText()
            blood= self.w1.bloodEntry.currentIndex()
            phone = self.w1.phoneEntry.text()
            password = self.w1.passwordEntry.text()
            self.cl = Client(name, age, gender, location, phone, weigh, blood, password)
            conn.execute(" Update Clients (Name, birthdate, gender, location, phone, weigh, blood, password) values('" + str(self.cl.getName()) + "', '" + str(self.cl.getAge()) + "', '" + str(self.cl.getGender()) + "', '" + str(self.cl.getLocation()) + "', '" + str(self.cl.getPhone()) + "', '" + str(self.cl.getWeigh()) + "', '" + str(self.cl.getBlood()) + "', '" + str(self.cl.getPassword()) + "')")
            conn.commit()
            self.close()


class RegisterForm(QDialog):
    def __init__(self, model):
        super(RegisterForm, self).__init__()
        self.m = model
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Register form")
        self.setMaximumSize(500, 820)
        self.setMinimumSize(500, 820)
        self.setGeometry(590,0, 500, 820)
        self.setStyleSheet("background-color: grey")


        self.yourInformationLabel = QLabel("Your information", self)
        self.yourInformationLabel.move(70,20)
        self.yourInformationLabel.setStyleSheet("color:white")
        self.yourInformationLabel.setFont(QtGui.QFont("Times", 35, QtGui.QFont.Bold))

        self.NameLabel = QLabel("First name", self)
        self.NameLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.NameLabel.move(20, 100)
        self.NameLabel.setStyleSheet("color: white")
        self.NameEntry = QLineEdit(self)
        self.NameEntry.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.NameEntry.move(250, 105)
        self.NameEntry.setStyleSheet("background-color:white")

        self.ageLabel = QLabel("Date of birth", self)
        self.ageLabel.move(20, 175)
        self.ageLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.ageLabel.setStyleSheet("color: white")
        self.ageButton = QPushButton("Select date", self)
        self.ageButton.setGeometry(250,180,205,25)
        self.ageButton.setStyleSheet("background-color:white")
        self.ageButton.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.ageButton.clicked.connect(self.calendar)

        self.genderLabel = QLabel("Gender", self)
        self.genderLabel.move(20, 250)
        self.genderLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.genderLabel.setStyleSheet("color: white")
        self.gender = QRadioButton('Male', self)
        self.gender.setChecked(True)
        self.gender.gender = "Male"
        self.gender.setStyleSheet("color: white")
        self.gender.move(200, 255)
        self.gender.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.gender = QRadioButton('Female', self)
        self.gender.gender = "Female"
        self.gender.setStyleSheet("color: white")
        self.gender.move(300, 255)
        self.gender.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))

        self.locationLabel = QLabel("Location", self)
        self.locationLabel.move(20, 325)
        self.locationLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.locationLabel.setStyleSheet("color: white")
        self.locationEntry = QLineEdit(self)
        self.locationEntry.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.locationEntry.move(250, 330)
        self.locationEntry.setStyleSheet("background-color:white")

        self.phoneLabel = QLabel("Phone", self)
        self.phoneLabel.move(20, 400)
        self.phoneLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.phoneLabel.setStyleSheet("color: white")
        self.phoneEntry = QLineEdit(self)
        self.phoneEntry.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.phoneEntry.move(250, 405)
        self.phoneEntry.setStyleSheet("background-color:white")

        self.weighLabel = QLabel("Weigh", self)
        self.weighLabel.move(20, 475)
        self.weighLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.weighLabel.setStyleSheet("color: white")
        self.weighEntry = QComboBox(self)
        self.weighEntry.setGeometry(QtCore.QRect(250, 480, 100, 30))
        self.weighEntry.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.weighEntry.addItems(self.m.getAllweighes())


        self.bloodLabel = QLabel("Blood type", self)
        self.bloodLabel.move(20, 550)
        self.bloodLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.bloodLabel.setStyleSheet("color: white")
        self.bloodEntry = QComboBox(self)
        self.bloodEntry.setGeometry(QtCore.QRect(250, 555, 100, 30))
        self.bloodEntry.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.bloodEntry.addItems(self.m.getAllbloodtypes())

        self.passwordLabel = QLabel("Password", self)
        self.passwordLabel.move(20, 625)
        self.passwordLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.passwordLabel.setStyleSheet("color: white")
        self.passwordEntry = QLineEdit(self)
        self.passwordEntry.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.passwordEntry.setEchoMode(QLineEdit.Password)
        self.passwordEntry.move(250, 630)
        self.passwordEntry.setStyleSheet("background-color:white")

        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.resize(150,50)
        self.cancelButton.move(60, 700)
        self.cancelButton.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.cancelButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(0, 102, 255); color:white;}')
        self.cancelButton.clicked.connect(self.close)

        self.submitButton = QPushButton("Submit", self)
        self.submitButton.resize(150,50)
        self.submitButton.move(255, 700)
        self.submitButton.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.submitButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(0, 102, 255); color:white;}')
        self.submitButton.clicked.connect(self.submit)

        self.changeButton = QPushButton("Change", self)
        self.changeButton.resize(150,50)
        self.changeButton.move(255,700)
        self.changeButton.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.changeButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(0, 102, 255); color:white;}')
        self.changeButton.setVisible(False)

    def submit(self):
        if self.NameEntry.text() == "" or self.ageButton.text() == "Select date"or self.locationEntry.text() == "" or self.weighEntry.currentText() == "Select" or self.bloodEntry.currentText() == "Select" or self.passwordEntry.text() == ""or self.phoneEntry.text() == "":
            w = WarningW()
            w.move(640,400)
            w.exec_()
        else:
            name = self.NameEntry.text()
            age = self.ageButton.text()
            gender = self.gender.gender
            location = self.locationEntry.text()
            weigh = self.weighEntry.currentText()
            blood= self.bloodEntry.currentIndex()
            phone = self.phoneEntry.text()
            password = self.passwordEntry.text()
            self.cl = Client(name, age, gender, location, phone, weigh, blood, password)
            conn = sqlite3.connect(conn_str)
            req1 = conn.execute("select count(Clients.id) from Clients where Clients.phone = '" + str(self.cl.getPhone()) + "'")
            count1 = 0
            for item in req1:
                count1 = item[0]
            if count1 != 0:
                w = WarningW()
                w.label.setText("You have already registered")
                w.label.move(20,35)
                w.move(500,400)
                w.resize(400,100)
                w.okButton.move(150,70)
                w.exec_()
            else:
                conn.execute("insert into Clients (Name, birthdate, gender, location, phone, weigh, blood, password) values('" + str(self.cl.getName()) + "', '" + str(self.cl.getAge()) + "', '" + str(self.cl.getGender()) + "', '" + str(self.cl.getLocation()) + "', '" + str(self.cl.getPhone()) + "', '" + str(self.cl.getWeigh()) + "', '" + str(self.cl.getBlood()) + "', '" + str(self.cl.getPassword()) + "')")
                conn.commit()
                self.close()
    def calendar(self):
        w = Calendar()
        w.exec_()
        self.ageButton.setText(w.s)

class QueueForm(QDialog):
    def __init__(self, que):
        super(QueueForm, self).__init__()
        self.title = 'Queue display'
        self.left = 700
        self.top = 340
        self.width = 256.5
        self.height = 230
        self.que = que
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.listWidget = QListWidget(self)
        for i in self.que:
            self.listWidget.addItem(str(i[0])+"     "+str(i[1]))

        self.listWidget.show()
        self.cancelButton = QPushButton("OK", self)
        self.cancelButton.resize(80,30)
        self.cancelButton.move(83, 195)
        self.cancelButton.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        self.cancelButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(0, 102, 255); color:white;}')
        self.cancelButton.clicked.connect(self.close)

class HistoryForm(QDialog):
    def __init__(self, model, client):
        super(HistoryForm, self).__init__()
        self.title = 'History display'
        self.left = 700
        self.top = 340
        self.width = 256.5
        self.height = 230
        self.m = model
        self.cl = client
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        self.listWidget = QListWidget(self)
        self.hist=self.m.createHistory(self.cl.phone)
        for i in self.hist:
            self.listWidget.addItem(i)

        self.listWidget.show()
        self.cancelButton = QPushButton("OK", self)
        self.cancelButton.resize(80,30)
        self.cancelButton.move(83, 195)
        self.cancelButton.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.cancelButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(0, 102, 255); color:white;}')
        self.cancelButton.clicked.connect(self.close)


class LoginForm(QDialog):
    def __init__(self, model):
        super(LoginForm, self).__init__()
        self.m = model
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Login form")
        self.setGeometry(570,350, 500, 250)
        self.setStyleSheet("background-color: grey")

        self.count1=0

        self.PhoneLabel = QLabel("Phone", self)
        self.PhoneLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.PhoneLabel.move(20, 20)
        self.PhoneLabel.setStyleSheet("color: white")
        self.PhoneEntry = QLineEdit(self)
        self.PhoneEntry.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.PhoneEntry.move(250, 25)
        self.PhoneEntry.setStyleSheet("background-color:white")

        self.passwordLabel = QLabel("Password", self)
        self.passwordLabel.move(20, 95)
        self.passwordLabel.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.passwordLabel.setStyleSheet("color: white")
        self.passwordEntry = QLineEdit(self)
        self.passwordEntry.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.passwordEntry.setEchoMode(QLineEdit.Password)
        self.passwordEntry.move(250, 100)
        self.passwordEntry.setStyleSheet("background-color:white")

        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.resize(150,50)
        self.cancelButton.move(60, 170)
        self.cancelButton.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.cancelButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(0, 102, 255); color:white;}')
        self.cancelButton.clicked.connect(self.close)

        self.submitButton = QPushButton("Submit", self)
        self.submitButton.resize(150,50)
        self.submitButton.move(295, 170)
        self.submitButton.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.submitButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(0, 102, 255); color:white;}')
        self.submitButton.clicked.connect(self.submit)

    def submit(self):
        if self.passwordEntry.text() == ""or self.PhoneEntry.text() == "":
            w = WarningW()
            w.move(640,400)
            w.exec_()
        else:
            phone = self.PhoneEntry.text()
            password = self.passwordEntry.text()
            self.cl, self.count1 = self.m.checkClient(phone, password)
            if self.count1 == 0:
                w = WarningW()
                w.label.setText("Oops, something did not work out\nIncorrect phone/password combination.")
                w.label.move(20,35)
                w.move(500,400)
                w.resize(400,100)
                w.okButton.move(150,70)
                w.exec_()
            else:
                self.close()

class Calendar(QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        now = QDate.currentDate()
        self.s = now.toString(Qt.ISODate)
        self.setWindowTitle("Select date")
        vbox = QVBoxLayout(self)
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked[QDate].connect(self.showDate)
        cal.clicked[QDate].connect(self.close)
        vbox.addWidget(cal)

    def showDate(self, date):
        self.s = date.toString(Qt.ISODate)

class WarningW(QDialog):
    def __init__(self):
        super(WarningW, self).__init__()
        self.setWindowTitle("Warning")
        self.setGeometry(250,350,250,100)
        self.label = QLabel("Please fill in all fields", self)
        self.label.move(40,35)
        #self.anotherLabel = QLabel()
        self.label.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.okButton = QPushButton("OK", self)
        self.okButton.move(80,70)
        self.okButton.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.okButton.setStyleSheet('QPushButton:hover { background-color: rgb(51, 51, 255);text-decoration: underline;} QPushButton:!hover { background-color: rgb(0, 102, 255); color:white;}')
        self.okButton.clicked.connect(self.close)


class Model:
    def __init__(self):
        self.conn = sqlite3.connect(conn_str)
        self.cursor = self.conn.cursor()
        self.client = self.conn.cursor()


    def getAllbloodtypes(self):
        req = self.conn.execute("select title from bloodtype")
        l1 = ["Select"]
        for row in req:
            l1.append(row[0])
        return l1

    def getAllweighes(self):
        a=[str(x) for x in range(50,161)]
        weight_list=["Select"]
        weight_list+=a
        return weight_list

    def getClient(self, phone, passw):
        req = self.conn.execute("select * from Clients where Clients.phone = '" + str(phone) + "' and Clients.password = '" + str(passw) + "'")
        cl = Client()
        for item in req:
            cl.setName(item[1])
            cl.setAge(item[2])
            cl.setGender(item[3])
            cl.setLocation(item[4])
            cl.setPhone(item[5])
            cl.setWeigh(item[6])
            cl.setBlood(item[7])
            cl.setPassword(item[8])
        return cl

    def checkClient(self, phone, passw):
        count = 0
        collection = []
        #print(s)
        req = self.conn.execute("select Clients.name from Clients where Clients.phone = '" + str(phone) + "' and Clients.password = '" + str(passw) + "'")
        for item in req:
            count = item[0]
        if count != 0:
            cl=self.getClient(phone, passw)
        return cl, count

    def createQueque(self, q):
        req = self.conn.execute("select cl.name, ap.id, cl.id from Clients as cl Join Applications  as ap on ap.Client = cl.id  where ap.Status != '" + 'Processed' + "'")
        for item in req:
            q.setQueue([item[0], item[1], item[2]])

    def addtoQueque(self, client, que):
        count=0
        rnum = self.conn.execute("select id from Clients where Clients.phone = '" + str(client.phone) + "'")
        for item in rnum:
            self.id=item[0]
        for i in que.queue:
            count=i[1]
            if i[2] == self.id:
                return "You're already in the queue, plz wait"

        req = self.conn.execute("insert into Applications (time, Client, Status) values('" + str(datetime.now()) + "', '" + str(self.id) + "', '"  + 'Waiting' + "')")
        self.conn.commit()
        que.setQueue([client.name, count+1, self.id])
        return "Successfully Added"

    def createHistory(self, client):
        hist=[]
        req = self.conn.execute("select cl.name, ap.id, ap.time, ap.Status from Clients as cl Join Applications  as ap on ap.Client = cl.id  where cl.phone = '" + str(client) + "'")
        for item in req:
            hist.append(str(item[0])+" "+str(item[1])+" "+str(item[2])+" "+str(item[3])+" ")
        return hist
class Client:

    def __init__(self, name = "", age = "", gender = "", location = "", phone = "", weigh = "", blood = "", password = ""):
        self.name = name
        self.age = age
        self.gender = gender
        self.location = location
        self.phone = phone
        self.weigh = weigh
        self.blood = blood
        self.password = password

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getGender(self):
        return self.gender

    def getLocation(self):
        return self.location

    def getPhone(self):
        return self.phone

    def getWeigh(self):
        return self.weigh

    def getBlood(self):
        return self.blood

    def getPassword(self):
        return self.password

    def setName(self, name):
        self.name = name

    def setAge(self, age):
        self.age = age

    def setGender(self, gender):
        self.gender = gender

    def setLocation(self, location):
        self.location = location

    def setPhone(self, phone):
        self.phone = phone

    def setWeigh(self, weigh):
        self.weigh = weigh

    def setBlood(self, blood):
        self.blood = blood

    def setPassword(self, password):
        self.password = password

class Queue:
    class queue_iter:
        def __init__(self, clients):
            self._clients = clients
            self.cur = 0

        def __next__(self):
            i = self.cur
            if i >= len(self._clients):
                raise StopIteration
            self.cur += 1
            return self._clients[i]
    def __init__(self, queue):
        self.queue = queue
    def getQueue(self):
        return self.queue
    def setQueue(self, client):
        self.queue.append(client)
    def removeQueue(self, client):
        self.queue.pop(0)
    def __iter__(self):
        return Queue.queue_iter(self.queue)

class Controller:
    def __init__(self):
        app = QApplication(sys.argv)
        self.model = Model()
        self.view = View(self.model)
        self.view.show()
        app.exec_()

c = Controller()
