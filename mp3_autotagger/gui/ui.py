# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(969, 824)
        MainWindow.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui/../assets/main_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setBaseSize(QtCore.QSize(1280, 720))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setIconSize(QtCore.QSize(40, 40))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_autotagger = QtWidgets.QWidget()
        self.tab_autotagger.setObjectName("tab_autotagger")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_autotagger)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_year = QtWidgets.QLineEdit(self.tab_autotagger)
        self.lineEdit_year.setEnabled(False)
        self.lineEdit_year.setText("")
        self.lineEdit_year.setObjectName("lineEdit_year")
        self.gridLayout.addWidget(self.lineEdit_year, 6, 1, 1, 3)
        self.checkBox_rename_file = QtWidgets.QCheckBox(self.tab_autotagger)
        self.checkBox_rename_file.setChecked(True)
        self.checkBox_rename_file.setObjectName("checkBox_rename_file")
        self.gridLayout.addWidget(self.checkBox_rename_file, 7, 1, 1, 3)
        self.lineEdit_title = QtWidgets.QLineEdit(self.tab_autotagger)
        self.lineEdit_title.setEnabled(False)
        self.lineEdit_title.setText("")
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.gridLayout.addWidget(self.lineEdit_title, 3, 1, 1, 3)
        self.lineEdit_genre = QtWidgets.QLineEdit(self.tab_autotagger)
        self.lineEdit_genre.setEnabled(False)
        self.lineEdit_genre.setText("")
        self.lineEdit_genre.setObjectName("lineEdit_genre")
        self.gridLayout.addWidget(self.lineEdit_genre, 5, 1, 1, 3)
        self.lineEdit_artist = QtWidgets.QLineEdit(self.tab_autotagger)
        self.lineEdit_artist.setEnabled(False)
        self.lineEdit_artist.setWhatsThis("")
        self.lineEdit_artist.setAutoFillBackground(False)
        self.lineEdit_artist.setInputMask("")
        self.lineEdit_artist.setText("")
        self.lineEdit_artist.setObjectName("lineEdit_artist")
        self.gridLayout.addWidget(self.lineEdit_artist, 2, 1, 1, 3)
        self.label_mp3_count = QtWidgets.QLabel(self.tab_autotagger)
        self.label_mp3_count.setText("")
        self.label_mp3_count.setObjectName("label_mp3_count")
        self.gridLayout.addWidget(self.label_mp3_count, 11, 0, 1, 4)
        self.pushButton_save_tags = QtWidgets.QPushButton(self.tab_autotagger)
        self.pushButton_save_tags.setEnabled(False)
        self.pushButton_save_tags.setObjectName("pushButton_save_tags")
        self.gridLayout.addWidget(self.pushButton_save_tags, 9, 2, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem, 14, 0, 1, 4)
        self.pushButton_find_and_save_all_tags = QtWidgets.QPushButton(self.tab_autotagger)
        self.pushButton_find_and_save_all_tags.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_find_and_save_all_tags.sizePolicy().hasHeightForWidth())
        self.pushButton_find_and_save_all_tags.setSizePolicy(sizePolicy)
        self.pushButton_find_and_save_all_tags.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton_find_and_save_all_tags.setMaximumSize(QtCore.QSize(441, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_find_and_save_all_tags.setFont(font)
        self.pushButton_find_and_save_all_tags.setObjectName("pushButton_find_and_save_all_tags")
        self.gridLayout.addWidget(self.pushButton_find_and_save_all_tags, 13, 0, 1, 4, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem1, 16, 0, 1, 4)
        self.label_mp3_details = QtWidgets.QLabel(self.tab_autotagger)
        self.label_mp3_details.setObjectName("label_mp3_details")
        self.gridLayout.addWidget(self.label_mp3_details, 0, 1, 1, 3)
        self.listWidget_tracks = QtWidgets.QListWidget(self.tab_autotagger)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_tracks.sizePolicy().hasHeightForWidth())
        self.listWidget_tracks.setSizePolicy(sizePolicy)
        self.listWidget_tracks.setObjectName("listWidget_tracks")
        self.gridLayout.addWidget(self.listWidget_tracks, 1, 0, 10, 1)
        spacerItem2 = QtWidgets.QSpacerItem(36, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 9, 4, 1, 1)
        self.label_autotagger_status = QtWidgets.QLabel(self.tab_autotagger)
        self.label_autotagger_status.setText("")
        self.label_autotagger_status.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_autotagger_status.setObjectName("label_autotagger_status")
        self.gridLayout.addWidget(self.label_autotagger_status, 17, 0, 1, 4)
        self.pushButton_find_tags = QtWidgets.QPushButton(self.tab_autotagger)
        self.pushButton_find_tags.setEnabled(False)
        self.pushButton_find_tags.setObjectName("pushButton_find_tags")
        self.gridLayout.addWidget(self.pushButton_find_tags, 9, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_mp3_dir = QtWidgets.QLineEdit(self.tab_autotagger)
        self.lineEdit_mp3_dir.setEnabled(True)
        self.lineEdit_mp3_dir.setReadOnly(True)
        self.lineEdit_mp3_dir.setObjectName("lineEdit_mp3_dir")
        self.horizontalLayout.addWidget(self.lineEdit_mp3_dir)
        self.pushButton_browse = QtWidgets.QPushButton(self.tab_autotagger)
        self.pushButton_browse.setObjectName("pushButton_browse")
        self.horizontalLayout.addWidget(self.pushButton_browse)
        self.gridLayout.addLayout(self.horizontalLayout, 10, 1, 1, 3)
        self.progressBar_find_and_save_all_tags = QtWidgets.QProgressBar(self.tab_autotagger)
        self.progressBar_find_and_save_all_tags.setProperty("value", 0)
        self.progressBar_find_and_save_all_tags.setObjectName("progressBar_find_and_save_all_tags")
        self.gridLayout.addWidget(self.progressBar_find_and_save_all_tags, 15, 0, 1, 5)
        spacerItem3 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem3, 12, 0, 1, 4)
        self.label_mp3_files = QtWidgets.QLabel(self.tab_autotagger)
        self.label_mp3_files.setObjectName("label_mp3_files")
        self.gridLayout.addWidget(self.label_mp3_files, 0, 0, 1, 1)
        self.lineEdit_album = QtWidgets.QLineEdit(self.tab_autotagger)
        self.lineEdit_album.setEnabled(False)
        self.lineEdit_album.setText("")
        self.lineEdit_album.setObjectName("lineEdit_album")
        self.gridLayout.addWidget(self.lineEdit_album, 4, 1, 1, 3)
        self.label_cover = QtWidgets.QLabel(self.tab_autotagger)
        self.label_cover.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_cover.sizePolicy().hasHeightForWidth())
        self.label_cover.setSizePolicy(sizePolicy)
        self.label_cover.setMinimumSize(QtCore.QSize(0, 0))
        self.label_cover.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_cover.setAutoFillBackground(False)
        self.label_cover.setFrameShape(QtWidgets.QFrame.Box)
        self.label_cover.setLineWidth(1)
        self.label_cover.setMidLineWidth(1)
        self.label_cover.setScaledContents(True)
        self.label_cover.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cover.setObjectName("label_cover")
        self.gridLayout.addWidget(self.label_cover, 1, 1, 1, 3)
        self.checkBox_replace_existing_tags = QtWidgets.QCheckBox(self.tab_autotagger)
        self.checkBox_replace_existing_tags.setObjectName("checkBox_replace_existing_tags")
        self.gridLayout.addWidget(self.checkBox_replace_existing_tags, 8, 1, 1, 2)
        self.gridLayout.setColumnStretch(0, 4)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(4, 1)
        self.gridLayout.setRowStretch(5, 1)
        self.gridLayout.setRowStretch(6, 1)
        self.gridLayout.setRowStretch(7, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("gui/../assets/autotagger_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_autotagger, icon1, "")
        self.tab_youtube2mp3 = QtWidgets.QWidget()
        self.tab_youtube2mp3.setObjectName("tab_youtube2mp3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_youtube2mp3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_download = QtWidgets.QPushButton(self.tab_youtube2mp3)
        self.pushButton_download.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_download.sizePolicy().hasHeightForWidth())
        self.pushButton_download.setSizePolicy(sizePolicy)
        self.pushButton_download.setMinimumSize(QtCore.QSize(0, 70))
        self.pushButton_download.setMaximumSize(QtCore.QSize(16777215, 70))
        self.pushButton_download.setObjectName("pushButton_download")
        self.gridLayout_4.addWidget(self.pushButton_download, 11, 3, 1, 1)
        self.label_video_url = QtWidgets.QLabel(self.tab_youtube2mp3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_video_url.sizePolicy().hasHeightForWidth())
        self.label_video_url.setSizePolicy(sizePolicy)
        self.label_video_url.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.label_video_url.setObjectName("label_video_url")
        self.gridLayout_4.addWidget(self.label_video_url, 7, 0, 1, 5)
        spacerItem4 = QtWidgets.QSpacerItem(256, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem4, 11, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout_4.addItem(spacerItem5, 12, 0, 1, 5)
        spacerItem6 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem6, 11, 4, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem7, 11, 0, 1, 1)
        self.groupBox_audio_information = QtWidgets.QGroupBox(self.tab_youtube2mp3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_audio_information.sizePolicy().hasHeightForWidth())
        self.groupBox_audio_information.setSizePolicy(sizePolicy)
        self.groupBox_audio_information.setObjectName("groupBox_audio_information")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_audio_information)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_audio_details = QtWidgets.QLabel(self.groupBox_audio_information)
        self.label_audio_details.setAlignment(QtCore.Qt.AlignCenter)
        self.label_audio_details.setObjectName("label_audio_details")
        self.verticalLayout_2.addWidget(self.label_audio_details)
        self.lineEdit_audio_details = QtWidgets.QLineEdit(self.groupBox_audio_information)
        self.lineEdit_audio_details.setEnabled(False)
        self.lineEdit_audio_details.setReadOnly(True)
        self.lineEdit_audio_details.setObjectName("lineEdit_audio_details")
        self.verticalLayout_2.addWidget(self.lineEdit_audio_details)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_2.addItem(spacerItem8)
        self.label_video_title = QtWidgets.QLabel(self.groupBox_audio_information)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_video_title.sizePolicy().hasHeightForWidth())
        self.label_video_title.setSizePolicy(sizePolicy)
        self.label_video_title.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.label_video_title.setObjectName("label_video_title")
        self.verticalLayout_2.addWidget(self.label_video_title)
        self.lineEdit_video_title = QtWidgets.QLineEdit(self.groupBox_audio_information)
        self.lineEdit_video_title.setEnabled(False)
        self.lineEdit_video_title.setToolTip("")
        self.lineEdit_video_title.setText("")
        self.lineEdit_video_title.setDragEnabled(False)
        self.lineEdit_video_title.setReadOnly(True)
        self.lineEdit_video_title.setPlaceholderText("")
        self.lineEdit_video_title.setClearButtonEnabled(False)
        self.lineEdit_video_title.setObjectName("lineEdit_video_title")
        self.verticalLayout_2.addWidget(self.lineEdit_video_title)
        spacerItem9 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_2.addItem(spacerItem9)
        self.checkBox_convert_to_mp3 = QtWidgets.QCheckBox(self.groupBox_audio_information)
        self.checkBox_convert_to_mp3.setChecked(True)
        self.checkBox_convert_to_mp3.setObjectName("checkBox_convert_to_mp3")
        self.verticalLayout_2.addWidget(self.checkBox_convert_to_mp3)
        spacerItem10 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_2.addItem(spacerItem10)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout_4.addWidget(self.groupBox_audio_information, 0, 0, 1, 5)
        spacerItem11 = QtWidgets.QSpacerItem(31, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem11, 11, 5, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout_4.addItem(spacerItem12, 14, 0, 1, 5)
        self.lineEdit_url = QtWidgets.QLineEdit(self.tab_youtube2mp3)
        self.lineEdit_url.setText("")
        self.lineEdit_url.setDragEnabled(False)
        self.lineEdit_url.setClearButtonEnabled(False)
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.gridLayout_4.addWidget(self.lineEdit_url, 8, 0, 1, 5)
        spacerItem13 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_4.addItem(spacerItem13, 1, 2, 1, 1)
        self.label_yt_status = QtWidgets.QLabel(self.tab_youtube2mp3)
        self.label_yt_status.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_yt_status.setText("")
        self.label_yt_status.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.label_yt_status.setObjectName("label_yt_status")
        self.gridLayout_4.addWidget(self.label_yt_status, 15, 0, 1, 5)
        self.progressBar_download = QtWidgets.QProgressBar(self.tab_youtube2mp3)
        self.progressBar_download.setProperty("value", 0)
        self.progressBar_download.setObjectName("progressBar_download")
        self.gridLayout_4.addWidget(self.progressBar_download, 13, 0, 1, 6)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout_4.addItem(spacerItem14, 9, 0, 1, 5)
        self.pushButton_get_audio_info = QtWidgets.QPushButton(self.tab_youtube2mp3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_get_audio_info.sizePolicy().hasHeightForWidth())
        self.pushButton_get_audio_info.setSizePolicy(sizePolicy)
        self.pushButton_get_audio_info.setMinimumSize(QtCore.QSize(0, 70))
        self.pushButton_get_audio_info.setMaximumSize(QtCore.QSize(16777215, 70))
        self.pushButton_get_audio_info.setBaseSize(QtCore.QSize(0, 0))
        self.pushButton_get_audio_info.setObjectName("pushButton_get_audio_info")
        self.gridLayout_4.addWidget(self.pushButton_get_audio_info, 11, 1, 1, 1)
        self.label_video_thumbnail = QtWidgets.QLabel(self.tab_youtube2mp3)
        self.label_video_thumbnail.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_video_thumbnail.sizePolicy().hasHeightForWidth())
        self.label_video_thumbnail.setSizePolicy(sizePolicy)
        self.label_video_thumbnail.setMaximumSize(QtCore.QSize(320, 180))
        self.label_video_thumbnail.setBaseSize(QtCore.QSize(256, 180))
        self.label_video_thumbnail.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_video_thumbnail.setFrameShape(QtWidgets.QFrame.Box)
        self.label_video_thumbnail.setLineWidth(1)
        self.label_video_thumbnail.setScaledContents(True)
        self.label_video_thumbnail.setAlignment(QtCore.Qt.AlignCenter)
        self.label_video_thumbnail.setObjectName("label_video_thumbnail")
        self.gridLayout_4.addWidget(self.label_video_thumbnail, 2, 2, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout_4.addItem(spacerItem15, 6, 0, 1, 5)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("gui/../assets/youtube2mp3_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_youtube2mp3, icon2, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setMouseTracking(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 969, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuLanguages = QtWidgets.QMenu(self.menubar)
        self.menuLanguages.setObjectName("menuLanguages")
        MainWindow.setMenuBar(self.menubar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionEnglish = QtWidgets.QAction(MainWindow)
        self.actionEnglish.setObjectName("actionEnglish")
        self.actionSpanish = QtWidgets.QAction(MainWindow)
        self.actionSpanish.setObjectName("actionSpanish")
        self.actionUpdates = QtWidgets.QAction(MainWindow)
        self.actionUpdates.setObjectName("actionUpdates")
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionUpdates)
        self.menuLanguages.addAction(self.actionEnglish)
        self.menuLanguages.addAction(self.actionSpanish)
        self.menubar.addAction(self.menuLanguages.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MP3 Autotagger"))
        self.lineEdit_year.setToolTip(_translate("MainWindow", "Year"))
        self.lineEdit_year.setPlaceholderText(_translate("MainWindow", "Year"))
        self.checkBox_rename_file.setToolTip(_translate("MainWindow", "Rename file as <ARTIST> - <Title>"))
        self.checkBox_rename_file.setText(_translate("MainWindow", "Rename file"))
        self.lineEdit_title.setToolTip(_translate("MainWindow", "Title"))
        self.lineEdit_title.setPlaceholderText(_translate("MainWindow", "Title"))
        self.lineEdit_genre.setToolTip(_translate("MainWindow", "Genre"))
        self.lineEdit_genre.setPlaceholderText(_translate("MainWindow", "Genre"))
        self.lineEdit_artist.setToolTip(_translate("MainWindow", "Artist"))
        self.lineEdit_artist.setPlaceholderText(_translate("MainWindow", "Artist"))
        self.pushButton_save_tags.setText(_translate("MainWindow", "Save tags"))
        self.pushButton_find_and_save_all_tags.setText(_translate("MainWindow", "Find and save tags for all files"))
        self.label_mp3_details.setText(_translate("MainWindow", "MP3 details"))
        self.pushButton_find_tags.setText(_translate("MainWindow", "Find tags"))
        self.pushButton_browse.setText(_translate("MainWindow", "Browse"))
        self.label_mp3_files.setText(_translate("MainWindow", "MP3 files list"))
        self.lineEdit_album.setToolTip(_translate("MainWindow", "Album"))
        self.lineEdit_album.setPlaceholderText(_translate("MainWindow", "Album"))
        self.label_cover.setToolTip(_translate("MainWindow", "Click to add new cover"))
        self.label_cover.setText(_translate("MainWindow", "Cover"))
        self.checkBox_replace_existing_tags.setToolTip(
            _translate("MainWindow", "Replace existing tags when finding tags automatically")
        )
        self.checkBox_replace_existing_tags.setText(_translate("MainWindow", "Replace existing tags"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_autotagger), _translate("MainWindow", "Autotagger"))
        self.pushButton_download.setText(_translate("MainWindow", "Download"))
        self.label_video_url.setText(_translate("MainWindow", "Video URL"))
        self.groupBox_audio_information.setTitle(_translate("MainWindow", "Audio information"))
        self.label_audio_details.setText(_translate("MainWindow", "Audio details"))
        self.label_video_title.setText(_translate("MainWindow", "Video title"))
        self.checkBox_convert_to_mp3.setToolTip(_translate("MainWindow", "Check to convert original audio to .mp3"))
        self.checkBox_convert_to_mp3.setText(_translate("MainWindow", "Convert audio to .mp3"))
        self.lineEdit_url.setPlaceholderText(_translate("MainWindow", "Enter YouTube URL"))
        self.pushButton_get_audio_info.setText(_translate("MainWindow", "Get audio information"))
        self.label_video_thumbnail.setText(_translate("MainWindow", "Video thumbnail"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_youtube2mp3), _translate("MainWindow", "Youtube2MP3"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuLanguages.setTitle(_translate("MainWindow", "Language"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionEnglish.setText(_translate("MainWindow", "English"))
        self.actionSpanish.setText(_translate("MainWindow", "Spanish"))
        self.actionUpdates.setText(_translate("MainWindow", "Check for updates"))
        self.actionUpdates.setIconText(_translate("MainWindow", "Check for updates"))
