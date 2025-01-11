from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QMessageBox, QScrollArea, QListWidget, QListWidgetItem, QStackedWidget, QFileDialog
from PySide6.QtGui import QFont, QDesktopServices, QPalette, QColor
from PySide6.QtCore import Qt, QUrl
from CueSpliter import CueSpliter
import os
import threading
import time

RATIO_BASED_RESOLUTION = 1728 * 1117
DYNAMIC_FONT_SIZE = 30
FONT_RATIO = DYNAMIC_FONT_SIZE / RATIO_BASED_RESOLUTION
DYNAMIC_LIST_FONT_SIZE = 24
LIST_FONT_RATIO = DYNAMIC_LIST_FONT_SIZE / RATIO_BASED_RESOLUTION
DYNAMIC_LIST_FIXED_WIDTH = 600
LIST_FIXED_WIDTH_RATIO = DYNAMIC_LIST_FIXED_WIDTH / RATIO_BASED_RESOLUTION
WINDOW_TITLE = "Cue Spliter"
TOP_LABEL_DEFAULT_TEXT = "请拖动 CUE 文件到窗口内以打开它"
TOP_LABEL_HOVER_TEXT = "松开鼠标以打开文件"
OR_LABEL_TEXT = "或者"
BUTTON_TEXT = "点击我选择 CUE 文件"
ERROR_TEXT = "错误"
NORMAL_TEXT = "提示"


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        self.init_page = QWidget()
        self.__setupInitPage(screen_geometry)
        self.cover_page = QWidget()
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.init_page)
        self.stacked_widget.addWidget(self.cover_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        window_width = int(screen_geometry.width() * 0.5)
        window_height = int(screen_geometry.height() * 0.6)

        self.resize(window_width, window_height)

        # 居中显示
        window_x = int((screen_geometry.width() - window_width) / 2)
        window_y = int((screen_geometry.height() - window_height) / 2)
        self.move(window_x, window_y)

        self.setWindowTitle(WINDOW_TITLE)
        self.setAcceptDrops(True)

    def __createButton(self, button_text):
        button = QPushButton(button_text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2a80eb;
                color: white;
                font-size: %dpx;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #4178d8;
            }
            QPushButton:pressed {
                background-color: #3d71cd;
            }
            QPushButton:disabled {
                background-color: gray;
            }
        """ % (DYNAMIC_FONT_SIZE))
        return button

    def __setupInitPage(self, screen_geometry):
        DYNAMIC_FONT_SIZE = int(FONT_RATIO * screen_geometry.width()
                                * screen_geometry.height())
        DYNAMIC_LIST_FONT_SIZE = int(LIST_FONT_RATIO * screen_geometry.width()
                                     * screen_geometry.height())
        DYNAMIC_LIST_FIXED_WIDTH = int(LIST_FONT_RATIO * screen_geometry.width()
                                       * screen_geometry.height())
        self.label = QLabel(TOP_LABEL_DEFAULT_TEXT, self)
        self.label.setStyleSheet(f"font-size: {DYNAMIC_FONT_SIZE}px;")
        self.or_label = QLabel(OR_LABEL_TEXT, self)
        self.or_label.setStyleSheet(f"font-size: {DYNAMIC_FONT_SIZE}px;")

        self.button = self.__createButton(BUTTON_TEXT)
        self.button.clicked.connect(self.__selectCueFile)
        self.button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.addWidget(
            self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(
            self.or_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(
            self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.init_page.setLayout(layout)

    def __setupCoverPage(self, items, file_path):
        if not self.cover_page.layout():
            self.cue_path = file_path
            self.output_path = ""
            layout = QVBoxLayout()
            self.path_label = QLabel(f"当前文件：{file_path}")
            self.path_label.setStyleSheet(f"font-size: {DYNAMIC_FONT_SIZE}px;")
            self.path_label.setWordWrap(True)
            self.song_list = self.__createListWidget(items)

            scroll_area = QScrollArea(self)
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.song_list)
            scroll_area.setFixedWidth(DYNAMIC_LIST_FIXED_WIDTH)

            self.output_path_label = QLabel()
            self.output_path_label.setStyleSheet(
                f"font-size: {DYNAMIC_FONT_SIZE}px;")
            self.output_path_label.setWordWrap(True)

            self.select_output_path_button = self.__createButton("选择保存路径")
            self.select_output_path_button.clicked.connect(
                self.__selectOutputFolder)
            self.start_button = self.__createButton("开始切分")
            self.start_button.clicked.connect(self.__startSplit)

            button_layout = QHBoxLayout()
            button_layout.addWidget(self.select_output_path_button)
            button_layout.addWidget(self.start_button)

            layout.addWidget(
                self.path_label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(
                scroll_area, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.output_path_label,
                             alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addLayout(button_layout)
            self.cover_page.setLayout(layout)
        else:
            self.cue_path = file_path
            self.path_label.setText(f"当前文件：{file_path}")
            self.__updateListWidget(items, self.song_list)

    def __startSplit(self):
        if not os.path.isfile(self.cue_path):
            self.__showErrorMessage(f"打开 \"{self.cue_path}\" 失败，它不是一个文件")
        elif not os.path.isdir(self.output_path):
            self.__showErrorMessage(f"打开 \"{self.output_path}\" 失败，它不是一个目录")
        else:
            origin_path_label_text = self.path_label.text()
            self.path_label.setText("正在处理，请稍后...")
            self.start_button.setEnabled(False)
            self.select_output_path_button.setEnabled(False)

            result = []
            thread = threading.Thread(
                target=lambda: result.append(CueSpliter.doSplit(
                    self.cue_path, self.output_path))
            )
            thread.start()
            # TODO: not a good design
            while thread.is_alive():
                QApplication.processEvents()
                time.sleep(0.1)

            ret = result[0]
            if not ret.isOk:
                self.__showErrorMessage(f"文件切分失败!\n{ret.errMsg}")
            else:
                self.__showNormalMessage("文件切分成功!")
                QDesktopServices.openUrl(
                    QUrl.fromLocalFile(self.output_path))
            self.path_label.setText(origin_path_label_text)
            self.start_button.setEnabled(True)
            self.select_output_path_button.setEnabled(True)

    def __selectCueFile(self):
        file = QFileDialog.getOpenFileName(
            self, '选择 .cue 文件')
        if file and file[0]:
            self.__displayCueInfo(file[0])

    def __selectOutputFolder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if folder:
            self.output_path = folder
            self.output_path_label.setText(f'文件将被保存到: {folder}')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setText(TOP_LABEL_HOVER_TEXT)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.label.setText(TOP_LABEL_DEFAULT_TEXT)

    def __showErrorMessage(self, message):
        QMessageBox.critical(self, ERROR_TEXT, message)
        self.label.setText(TOP_LABEL_DEFAULT_TEXT)

    def __showNormalMessage(self, message):
        QMessageBox.information(self, NORMAL_TEXT, message)
        self.label.setText(TOP_LABEL_DEFAULT_TEXT)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            files = [url.toLocalFile() for url in event.mimeData().urls()]
            if len(files) > 1 or len(files) < 1:
                self.__showErrorMessage('仅支持同时打开一个 CUE 文件')
            else:
                self.__displayCueInfo(files[0])
        else:
            event.ignore()

    def __displayCueInfo(self, cue_path):
        ret = CueSpliter.getCueInfo(cue_path)
        if not ret.isOk:
            self.__showErrorMessage(f"读取 CUE 文件失败!\n{ret.errMsg}")
            return

        cue_titles = self.__getCueTitles(ret.data)
        self.__setupCoverPage(cue_titles, cue_path)
        self.stacked_widget.setCurrentIndex(1)

    def __getCueTitles(self, cue_info):
        cue_titles = []
        for i in range(len(cue_info)):
            cue_titles.append(cue_info[i]["TITLE"])
        return cue_titles

    def __createListWidget(self, items):
        list_widget = QListWidget()
        for i in range(len(items)):
            list_widget.addItem(self.__createListWidgetItem(
                items[i], DYNAMIC_LIST_FONT_SIZE))
        return list_widget

    def __updateListWidget(self, items, list_widget):
        list_widget.clear()
        for i in range(len(items)):
            list_widget.addItem(self.__createListWidgetItem(
                items[i], DYNAMIC_LIST_FONT_SIZE))

    def __createListWidgetItem(self, item_str, font_size):
        item = QListWidgetItem(item_str)
        font = QFont()
        font.setPointSize(font_size)
        item.setFont(font)
        return item
