import sys
from PySide2.QtCore import QUrl, Qt
from PySide2.QtGui import QGuiApplication, QIcon, QPixmap
from PySide2.QtWidgets import (QApplication, QMainWindow)
from PySide2.QtWebEngineWidgets import (QWebEngineView, QWebEngineProfile,
                                        QWebEnginePage, QWebEngineSettings)

from dataclasses import dataclass
from typing import List, Optional
import logging
from os import path
from yttv.yawebview.QtSingleApplication import QtSingleApplication
from yttv.yawebview import sighandler

@dataclass
class Options:
    user_agent: Optional[str] = None
    single_instance_mode: bool = False


class Window:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Window, cls).__new__(cls)
        return cls._instance

    def __init__(self, title: str, url: str, scrollbars: bool = True,
                 context_menu: bool = True, title_from_page: bool = True):
        self.title = title
        self.url = url
        self.show_scrollbars = scrollbars
        self.disable_context_menu = not context_menu
        self.set_title_from_page = title_from_page
        # self.width =
        # self.height
        self.icon_set = False

    def set_icon(self, icon_name: str, fallback_icon_files: List[str] = []):
        self.icon_set = True
        self.icon_name = icon_name
        self.fallback_icon_files = fallback_icon_files


class BrowserView(QMainWindow):
    def __init__(self, window: Window, user_agent: Optional[str] = None):
        # super(BrowserView, self).__init__()
        super().__init__()
        self.initUI(window=window, user_agent=user_agent)

    def initUI(self, window: Window, user_agent: Optional[str]):
        self.webEngineView = QWebEngineView(self)
        self.webEngineView.settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, window.show_scrollbars)
        if window.disable_context_menu:
            self.webEngineView.setContextMenuPolicy(Qt.NoContextMenu)

        profile = QWebEngineProfile.defaultProfile()
        if user_agent:
            profile.setHttpUserAgent(user_agent)
        self.webEngineView.page().profile = profile

        if window.set_title_from_page:
            self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        self.webEngineView.setUrl(QUrl(window.url))

        self.setCentralWidget(self.webEngineView)

        self.setWindowTitle(window.title)
        if window.icon_set:
            self.set_icon(window.icon_name, window.fallback_icon_files)
        self.resize(QGuiApplication.primaryScreen().
                    availableGeometry().size() * 0.7)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_icon(self, icon_name, fallback_icon_files):
        fallback_icon = QIcon()
        for filename in fallback_icon_files:
            pixmap = QPixmap()
            pixmap.load(filename)
            if pixmap.isNull():
                logging.warning(f"Failed to load {filename}")
            else:
                fallback_icon.addPixmap(pixmap)
        icon = QIcon.fromTheme(icon_name, fallback_icon)
        if icon.isNull():
            logging.warning("Failed to load icon")
        else:
            self.setWindowIcon(icon)


def start(options: Options = Options()):
    args = sys.argv
    args.append('--disable-seccomp-filter-sandbox')
    if options.single_instance_mode:
        id = path.abspath(path.realpath(__file__)).replace(path.sep, "_")
        app = QtSingleApplication(id, args)
        sighandler.crash_handler(app)
        if app.isRunning():
            logging.info("Another instance is already running")
            sys.exit(0)
    else:
        app = QApplication(args)
        sighandler.crash_handler(app)
    w = BrowserView(Window._instance, user_agent=options.user_agent)
    w.show()
    if options.single_instance_mode:
        app.setActivationWindow(w)
    sys.exit(app.exec_())
