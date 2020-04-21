from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os
import sys


class Settings_Dialog(QDialog ):
    def __init__(self, main_window = None):
        super().__init__()

        print("settings dialoge created")
        self.setWindowTitle("Settings")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon(os.path.join('images', 'gear.png')))
        self.main_window = main_window
        label= QLabel("Languages:")
        self.checkbox_eng = QCheckBox("English")
        self.checkbox_pol = QCheckBox("Polski")
        self.checkbox_ger = QCheckBox("Deutsch")
        ok_button = QPushButton("OK")
        cancle_button = QPushButton("Cancle")

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        vbox.addWidget(label,30, Qt.AlignTop)
        vbox.addWidget(self.checkbox_eng,10, Qt.AlignTop)
        vbox.addWidget(self.checkbox_pol,10, Qt.AlignTop)
        vbox.addWidget(self.checkbox_ger,10, Qt.AlignTop)

        hbox.addWidget(ok_button)
        hbox.addWidget(cancle_button)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        print(self.setFixedSize(self.minimumSizeHint()))
        ok_button.clicked.connect(self.ok_button_clicked)
        cancle_button.clicked.connect(self.cancle_button_clicked)

        self.show()


        if self.main_window != None:
            languages = self.main_window.language_set.split("+")
            if 'eng' in languages:
                self.checkbox_eng.setChecked(True)
            if 'pol' in languages:
                self.checkbox_pol.setChecked(True)
            if 'deu' in languages:
                self.checkbox_ger.setChecked(True)

    def ok_button_clicked(self):
        languages = []
        if self.checkbox_eng.isChecked():
            languages.append("eng")
        if self.checkbox_pol.isChecked():
            languages.append("pol")
        if self.checkbox_ger.isChecked():
            languages.append("deu")
        if self.main_window != None:
            self.main_window.language_set = "+".join(languages)
            #print("+".join(languages))
            self.close()
        else:
            print("+".join(languages))

    def cancle_button_clicked(self):
        self.close()


if __name__ =="__main__":
    app = QApplication(sys.argv)
    settings = Settings_Dialog()
    sys.exit(app.exec_())

