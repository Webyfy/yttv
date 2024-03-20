import sys
from PySide2.QtCore import QUrl, Qt
from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtWidgets import (QApplication, QMainWindow)
from PySide2.QtWebEngineWidgets import (QWebEngineView, QWebEngineProfile,
                                        QWebEnginePage, QWebEngineSettings)

from dataclasses import dataclass


@dataclass
class Options:
    user_agent: str | None = None


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
        # self.icon = None

    def set_icon(icon: str):
        pass


class BrowserView(QMainWindow):
    def __init__(self, window: Window, options: Options):
        super(BrowserView, self).__init__()
        self.initUI(window=window, options=options)

    def initUI(self, window: Window, options: Options):
        self.webEngineView = QWebEngineView(self)
        self.webEngineView.settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, window.show_scrollbars)
        if window.disable_context_menu:
            self.webEngineView.setContextMenuPolicy(Qt.NoContextMenu)

        profile = QWebEngineProfile.defaultProfile()
        if options.user_agent:
            profile.setHttpUserAgent(options.user_agent)
        self.webEngineView.page().profile = profile

        if window.set_title_from_page:
            self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        self.webEngineView.setUrl(QUrl(window.url))

        self.setCentralWidget(self.webEngineView)

        self.setWindowTitle(window.title)
        self.resize(QGuiApplication.primaryScreen().
                    availableGeometry().size() * 0.7)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def start(user_agent: str | None = None):
    app = QApplication(sys.argv)
    _ = BrowserView(Window._instance, Options(
        user_agent=user_agent,
    ))
    sys.exit(app.exec_())
