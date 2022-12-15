# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conway.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(471, 681)
        font = QtGui.QFont()
        font.setPointSize(14)
        Form.setFont(font)
        Form.setStyleSheet("background-color:dimgrey;color:darkorange;")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 471, 681))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setObjectName("gridLayout")
        self.winsize_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.winsize_label.setFont(font)
        self.winsize_label.setObjectName("winsize_label")
        self.gridLayout.addWidget(self.winsize_label, 12, 0, 1, 1)
        self.cellsize_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cellsize_edit.setFont(font)
        self.cellsize_edit.setStyleSheet("color:white;")
        self.cellsize_edit.setObjectName("cellsize_edit")
        self.gridLayout.addWidget(self.cellsize_edit, 2, 1, 1, 3)
        self.cycle_comment = QtWidgets.QLabel(self.gridLayoutWidget)
        self.cycle_comment.setObjectName("cycle_comment")
        self.gridLayout.addWidget(self.cycle_comment, 19, 0, 1, 4)
        self.go_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go_button.sizePolicy().hasHeightForWidth())
        self.go_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.go_button.setFont(font)
        self.go_button.setStyleSheet("color:white")
        self.go_button.setObjectName("go_button")
        self.gridLayout.addWidget(self.go_button, 23, 0, 1, 1)
        self.color_comment = QtWidgets.QLabel(self.gridLayoutWidget)
        self.color_comment.setObjectName("color_comment")
        self.gridLayout.addWidget(self.color_comment, 7, 0, 1, 4)
        self.cycle_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cycle_label.setFont(font)
        self.cycle_label.setObjectName("cycle_label")
        self.gridLayout.addWidget(self.cycle_label, 18, 0, 1, 1)
        self.winsize_w_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.winsize_w_edit.setStyleSheet("color:white;")
        self.winsize_w_edit.setObjectName("winsize_w_edit")
        self.gridLayout.addWidget(self.winsize_w_edit, 12, 1, 1, 1)
        self.spheric_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spheric_label.setFont(font)
        self.spheric_label.setObjectName("spheric_label")
        self.gridLayout.addWidget(self.spheric_label, 14, 0, 1, 1)
        self.cycletime_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cycletime_label.setFont(font)
        self.cycletime_label.setObjectName("cycletime_label")
        self.gridLayout.addWidget(self.cycletime_label, 20, 0, 1, 1)
        self.winsize_comment = QtWidgets.QLabel(self.gridLayoutWidget)
        self.winsize_comment.setObjectName("winsize_comment")
        self.gridLayout.addWidget(self.winsize_comment, 13, 0, 1, 4)
        self.wallpaper_comment = QtWidgets.QLabel(self.gridLayoutWidget)
        self.wallpaper_comment.setObjectName("wallpaper_comment")
        self.gridLayout.addWidget(self.wallpaper_comment, 11, 0, 1, 4)
        self.cellsize_comment = QtWidgets.QLabel(self.gridLayoutWidget)
        self.cellsize_comment.setObjectName("cellsize_comment")
        self.gridLayout.addWidget(self.cellsize_comment, 4, 0, 1, 4)
        self.fgcolor_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fgcolor_label.setFont(font)
        self.fgcolor_label.setObjectName("fgcolor_label")
        self.gridLayout.addWidget(self.fgcolor_label, 6, 0, 1, 1)
        self.fgcolor_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.fgcolor_edit.setStyleSheet("color:white;")
        self.fgcolor_edit.setObjectName("fgcolor_edit")
        self.gridLayout.addWidget(self.fgcolor_edit, 6, 1, 1, 3)
        self.spheric_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.spheric_button.setStyleSheet("color:white;")
        self.spheric_button.setCheckable(True)
        self.spheric_button.setObjectName("spheric_button")
        self.gridLayout.addWidget(self.spheric_button, 14, 1, 1, 1)
        self.bgcolor_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.bgcolor_edit.setStyleSheet("color:white;")
        self.bgcolor_edit.setObjectName("bgcolor_edit")
        self.gridLayout.addWidget(self.bgcolor_edit, 5, 1, 1, 3)
        self.bgcolor_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bgcolor_label.setFont(font)
        self.bgcolor_label.setObjectName("bgcolor_label")
        self.gridLayout.addWidget(self.bgcolor_label, 5, 0, 1, 1)
        self.winsize_sep_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.winsize_sep_label.setObjectName("winsize_sep_label")
        self.gridLayout.addWidget(self.winsize_sep_label, 12, 2, 1, 1)
        self.wallpaper_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.wallpaper_button.setStyleSheet("color:white;")
        self.wallpaper_button.setCheckable(True)
        self.wallpaper_button.setObjectName("wallpaper_button")
        self.gridLayout.addWidget(self.wallpaper_button, 10, 1, 1, 1)
        self.winsize_h_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.winsize_h_edit.setStyleSheet("color:white")
        self.winsize_h_edit.setObjectName("winsize_h_edit")
        self.gridLayout.addWidget(self.winsize_h_edit, 12, 3, 1, 1)
        self.steps_comment = QtWidgets.QLabel(self.gridLayoutWidget)
        self.steps_comment.setObjectName("steps_comment")
        self.gridLayout.addWidget(self.steps_comment, 17, 0, 1, 4)
        self.title_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.gridLayout.addWidget(self.title_label, 0, 0, 1, 4)
        self.cellsize_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cellsize_label.setFont(font)
        self.cellsize_label.setObjectName("cellsize_label")
        self.gridLayout.addWidget(self.cellsize_label, 2, 0, 1, 1)
        self.cycletime_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.cycletime_edit.setStyleSheet("color:white;")
        self.cycletime_edit.setObjectName("cycletime_edit")
        self.gridLayout.addWidget(self.cycletime_edit, 20, 1, 1, 3)
        self.cycle_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.cycle_button.setStyleSheet("color:white;")
        self.cycle_button.setCheckable(True)
        self.cycle_button.setObjectName("cycle_button")
        self.gridLayout.addWidget(self.cycle_button, 18, 1, 1, 1)
        self.steps_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.steps_label.setFont(font)
        self.steps_label.setObjectName("steps_label")
        self.gridLayout.addWidget(self.steps_label, 16, 0, 1, 1)
        self.spheric_comment = QtWidgets.QLabel(self.gridLayoutWidget)
        self.spheric_comment.setObjectName("spheric_comment")
        self.gridLayout.addWidget(self.spheric_comment, 15, 0, 1, 4)
        self.fullscreen_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fullscreen_label.setFont(font)
        self.fullscreen_label.setObjectName("fullscreen_label")
        self.gridLayout.addWidget(self.fullscreen_label, 8, 0, 1, 1)
        self.fullscreen_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.fullscreen_button.setStyleSheet("color:white;")
        self.fullscreen_button.setCheckable(True)
        self.fullscreen_button.setObjectName("fullscreen_button")
        self.gridLayout.addWidget(self.fullscreen_button, 8, 1, 1, 1)
        self.fullscreen_comment = QtWidgets.QLabel(self.gridLayoutWidget)
        self.fullscreen_comment.setObjectName("fullscreen_comment")
        self.gridLayout.addWidget(self.fullscreen_comment, 9, 0, 1, 4)
        self.steps_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.steps_edit.setStyleSheet("color:white;")
        self.steps_edit.setObjectName("steps_edit")
        self.gridLayout.addWidget(self.steps_edit, 16, 1, 1, 3)
        self.cycletime_comment = QtWidgets.QLabel(self.gridLayoutWidget)
        self.cycletime_comment.setObjectName("cycletime_comment")
        self.gridLayout.addWidget(self.cycletime_comment, 21, 0, 1, 4)
        self.wallpaper_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.wallpaper_label.setFont(font)
        self.wallpaper_label.setObjectName("wallpaper_label")
        self.gridLayout.addWidget(self.wallpaper_label, 10, 0, 1, 1)
        self.sep_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.sep_1.setText("")
        self.sep_1.setObjectName("sep_1")
        self.gridLayout.addWidget(self.sep_1, 1, 0, 1, 4)
        self.demo_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.demo_button.sizePolicy().hasHeightForWidth())
        self.demo_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.demo_button.setFont(font)
        self.demo_button.setStyleSheet("color:darkorange;")
        self.demo_button.setObjectName("demo_button")
        self.gridLayout.addWidget(self.demo_button, 23, 3, 1, 1)
        self.sep_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.sep_2.setText("")
        self.sep_2.setObjectName("sep_2")
        self.gridLayout.addWidget(self.sep_2, 22, 0, 1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.winsize_label.setText(_translate("Form", "Window Size"))
        self.cellsize_edit.setText(_translate("Form", "16"))
        self.cycle_comment.setText(_translate("Form", "Completely renew board or random drops of \"life\" and \"death\""))
        self.go_button.setText(_translate("Form", "Go!"))
        self.color_comment.setText(_translate("Form", "Check: https://www.pygame.org/docs/ref/color_list.html"))
        self.cycle_label.setText(_translate("Form", "Cycle mode"))
        self.winsize_w_edit.setText(_translate("Form", "800"))
        self.spheric_label.setText(_translate("Form", "Spheric Board"))
        self.cycletime_label.setText(_translate("Form", "Cycle period"))
        self.winsize_comment.setText(_translate("Form", "Ignored if Fulscreen or Wallpaper mode. Affects performance"))
        self.wallpaper_comment.setText(_translate("Form", "At bottom, Fullscreen, no focus, no input"))
        self.cellsize_comment.setText(_translate("Form", "Size of each \"cell\", in pixels. It drastically affects performance"))
        self.fgcolor_label.setText(_translate("Form", "Foreground color"))
        self.fgcolor_edit.setText(_translate("Form", "darkorange3"))
        self.spheric_button.setText(_translate("Form", "OFF"))
        self.bgcolor_edit.setText(_translate("Form", "gray12"))
        self.bgcolor_label.setText(_translate("Form", "Background color"))
        self.winsize_sep_label.setText(_translate("Form", ","))
        self.wallpaper_button.setText(_translate("Form", "ON"))
        self.winsize_h_edit.setText(_translate("Form", "800"))
        self.steps_comment.setText(_translate("Form", "Speed in steps per second. Also affecs performance"))
        self.title_label.setText(_translate("Form", "Conway\'s Game of Life Settings"))
        self.cellsize_label.setText(_translate("Form", "Cell size"))
        self.cycletime_edit.setText(_translate("Form", "3"))
        self.cycle_button.setText(_translate("Form", "ON"))
        self.steps_label.setText(_translate("Form", "Steps / second"))
        self.spheric_comment.setText(_translate("Form", "Board has borders (it physically ends) or not (like a sphere)"))
        self.fullscreen_label.setText(_translate("Form", "Fullscreen mode"))
        self.fullscreen_button.setText(_translate("Form", "ON"))
        self.fullscreen_comment.setText(_translate("Form", "Fullscreen or windowed"))
        self.steps_edit.setText(_translate("Form", "1"))
        self.cycletime_comment.setText(_translate("Form", "Time in minutes to renew board"))
        self.wallpaper_label.setText(_translate("Form", "Set as wallpaper"))
        self.demo_button.setText(_translate("Form", "or Demo..."))
