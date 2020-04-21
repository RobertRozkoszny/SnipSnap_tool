from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from settings_window import Settings_Dialog
from crop_area_window import Crop_area_window
import os
import sys

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
TEXT_EXTENSIONS = ['.txt']

def get_file_extension(passed_path):
    return os.path.splitext(passed_path)[1].lower()




class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My snipsnap tool")

        app.setWindowIcon(QIcon(os.path.join('images', 'ninja.png')))
        self.text_from_image = str
        self.snippet = None
        self.language_set = 'eng'
        self.path= ""

        #create my central peace - the tabs
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabPosition(QTabWidget.South)
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tab_first = QTextEdit(self)
        font = QFont('Times', 12)
        self.tab_first.setFont(font)
        self.tab_second = QLabel()
        self.tab_second.setAlignment(Qt.AlignCenter)
        self.tabWidget.addTab(self.tab_first, "Text")
        self.tabWidget.addTab(self.tab_second, "Snippet")
        self.tabWidget.setTabEnabled(1,False)
        self.tabWidget.currentChanged.connect(self.onChange)
        self.setCentralWidget(self.tabWidget)
        self.setContentsMargins(5,0,5,10)
        self.init_main_window_ui()

        self.show()

    def init_main_window_ui(self):

        # create menus bars
        menu_bar = self.menuBar()

        # create tool bars
        tool_bar1 = QToolBar("tool_bar1")
        tool_bar1.setIconSize(QSize(20,20))
        self.addToolBar(tool_bar1)

        # creating option "file" with suboptions
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        save_menu = menu_bar.addMenu("Save")
        settings_menu = menu_bar.addMenu("Settings")

        #create actions for menu and toolbars
        new_action = QAction(QIcon(os.path.join('images', 'text.png')), "New", self)
        new_action.setShortcut("Ctrl+N")
        open_action = QAction(QIcon(os.path.join('images', 'import.png')), "Open file...", self)
        open_action.setShortcut("Ctrl+O")
        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print", self)
        print_action.setShortcut("Ctrl+P")
        undo_action = QAction(QIcon(os.path.join('images', 'undo.png')), "Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        redo_action = QAction(QIcon(os.path.join('images', 'redo.png')), "Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        copy_action = QAction(QIcon(os.path.join('images', 'copy.png')), "Copy ", self)
        copy_action.setShortcut("Ctrl+C")
        paste_action = QAction(QIcon(os.path.join('images', 'sheet.png')), "Paste", self)
        paste_action.setShortcut("Ctrl+V")
        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setShortcut("Ctrl+X")
        font_action = QAction(QIcon(os.path.join('images', 'font.png')), "Font", self)
        font_action.setShortcut("Ctrl+F")
        save_action = QAction(QIcon(os.path.join('images', 'save.png')), "Save", self)
        save_action.setShortcut("Ctrl+S")
        save_as_action = QAction(QIcon(os.path.join('images', 'saveas.png')), "Save as", self)
        settings_action = QAction(QIcon(os.path.join('images', 'gear.png')), "Change language settings", self)
        close_action = QAction(QIcon(os.path.join('images', 'close.png')), "Close", self)

        # add status tips()
        #open_action.setStatusTip("status tip text")

        # add actions to menu bar and tool bar
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(print_action)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(font_action)
        save_menu.addAction(save_action)
        save_menu.addAction(save_as_action)
        settings_menu.addAction(settings_action)
        tool_bar1.addAction(new_action)
        tool_bar1.addAction(open_action)
        tool_bar1.addAction(print_action)
        tool_bar1.addAction(undo_action)
        tool_bar1.addAction(redo_action)
        tool_bar1.addAction(copy_action)
        tool_bar1.addAction(paste_action)
        tool_bar1.addAction(cut_action)
        tool_bar1.addAction(save_action)
        tool_bar1.addAction(close_action)

        # obsluga akcji
        new_action.triggered.connect(self.new_triggered)
        open_action.triggered.connect(self.open_triggered)
        print_action.triggered.connect(self.print_triggered)
        save_action.triggered.connect(self.save_triggered)
        save_as_action.triggered.connect(self.save_as_triggered)
        settings_action.triggered.connect(self.settings_triggered)
        copy_action.triggered.connect(self.copy_triggered)
        paste_action.triggered.connect(self.tab_first.paste)
        cut_action.triggered.connect(self.tab_first.cut)
        undo_action.triggered.connect(self.tab_first.undo)
        redo_action.triggered.connect(self.tab_first.redo)
        font_action.triggered.connect(self.font_triggered)
        close_action.triggered.connect(app.quit)


    def new_triggered(self):
        main_window.hide()
        self.snip = Crop_area_window(main_window)

    def open_triggered(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "","Image files: (*.jpg); (*.jpeg); (*.png);; Text files (*.txt)")

        if get_file_extension(path) in IMAGE_EXTENSIONS:
            try:
                print(f"path:{get_file_extension(path)}")
                self.pixmap = QPixmap(path)
                self.tab_second.setPixmap(self.pixmap)
                self.tabWidget.resize(self.pixmap.width(), self.pixmap.height())
                self.tabWidget.setTabEnabled(1, True)
                self.path = path
            except Exception as e:
                self.dialog_critical(str(e))

        elif get_file_extension(path) in TEXT_EXTENSIONS:
            try:
                with open(path, newline= None, encoding='utf-8') as f:
                    text = f.read()
                    self.tab_first.setText(text)
                    self.path = path
            except Exception as e:
                self.dialog_critical(str(e))

    def present_results(self):
        self.tab_first.setText(self.text_from_image)
        self.pixmap = QPixmap(r"images\temporary_snip_for_display.png")
        self.tabWidget.resize(self.pixmap.width(), self.pixmap.height())
        self.tab_second.setPixmap(self.pixmap)
        self.tabWidget.setTabEnabled(1, True)
        self.relocate_window()

    def relocate_window(self):
        point = QPoint()
        x, y = self.snip.get_coordinates_for_position([self.snip.start_point, self.snip.end_point])
        point.setX(min(x) - 10)
        point.setY(min(y) - 80)
        available_geometry = QDesktopWidget().availableGeometry(point)
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
        self.resize_main_window()
        self.move(point)

        if available_geometry.bottomRight().x() - self.frameGeometry().bottomRight().x() < 50 or available_geometry.bottomRight().y() - self.frameGeometry().bottomRight().y() <50:
            print("asd")
            point.setX(point.x()- abs(available_geometry.bottomRight().x() - self.frameGeometry().bottomRight().x()) )
            point.setY(point.y()- abs(available_geometry.bottomRight().y() - self.frameGeometry().bottomRight().y()) -30)
            self.move(point)
        self.show()

    def resize_main_window(self):
        new_width =  self.tabWidget.sizeHint().width() + 35
        new_height= self.tabWidget.sizeHint().height() + 35
        self.resize(new_width, new_height)

    def print_triggered(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.tab_first.print_(printer)


    def save_triggered(self):
        if self.path == "":
            #If there is no path use Save as
            return self.save_as_triggered()
        if (get_file_extension(self.path) in TEXT_EXTENSIONS) and self.tabWidget.currentIndex() == 0:
            try:
                with open(self.path, 'w') as f:
                    thing_to_be_saved = self.tab_first.toPlainText()
                    f.write(thing_to_be_saved)
            except Exception as e:
                self.dialog_critical(str(e))

        elif (get_file_extension(self.path) in IMAGE_EXTENSIONS) and self.tabWidget.currentIndex() == 1:
            try:
                thing_to_be_saved = self.tab_second.pixmap()
                thing_to_be_saved.save(self.path)
            except Exception as e:
                self.dialog_critical(str(e))
        else:
            # self.path has a path for a text that was opened with the file manager but the "save" button was
            # pressed while the snip tab was activated. Then triggering save_as is the appropriate action
            return self.save_as_triggered()

    def save_as_triggered(self):
        thing_to_be_saved = None
        save_extension = [
            "Text documents (*.txt)",
            "Image file: (*.png);; Image file: (*.jpg);;Image file: (*.jpeg)"
        ]
        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "", save_extension[self.tabWidget.currentIndex()])

        if not self.path:
            # If dialog is cancelled, will return ''
            return

        try:
            if self.tabWidget.currentIndex() == 0:
                with open(self.path, 'w') as f:
                    thing_to_be_saved = self.tab_first.toPlainText()
                    f.write(thing_to_be_saved)
            elif self.tabWidget.currentIndex() == 1:
                thing_to_be_saved = self.tab_second.pixmap()
                thing_to_be_saved.save(self.path)
        except Exception as e:
            self.dialog_critical(str(e))

    def settings_triggered(self):
        self.settings = Settings_Dialog(main_window)

    def copy_triggered(self):
        if self.tabWidget.currentIndex() == 0:
            self.tab_first.copy()
        elif self.tabWidget.currentIndex() == 1:
            self.tab_second.copy()

    def font_triggered(self):
        font, ok = QFontDialog.getFont()
        if ok:
            cursor = self.tab_first.textCursor()
            self.tab_first.setCurrentFont(font)

    def onChange(self):
        """for future development"""
        print(f"asdfa:{self.tabWidget.currentIndex()}")
        if self.tabWidget.currentIndex() == 0:
            #activate some options/deactivate others
            pass
        if self.tabWidget.currentIndex() == 1:
            #activate some options/deactivate others
            pass

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

if __name__ =="__main__":
    app = QApplication(sys.argv)
    main_window = Main_window()
    sys.exit(app.exec_())

