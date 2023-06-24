from PySide2.QtGui import QIcon
from PySide2.QtCore import QUrl, Qt
from PySide2.QtWidgets import QApplication,QMainWindow
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEnginePage

USER_AGENT = 'Roku/DVP-23.0 (23.0.0.99999-02)'
WINDOW_CLOSE_ERROR = "Scripts may close only the windows that were opened by them."

class WebEnginePage(QWebEnginePage):
    def __init__(self, window, profile, webview):
        QWebEnginePage.__init__(self, profile, webview)
        self.parent_window = window
    
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):  
        if (level == QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel) and \
            WINDOW_CLOSE_ERROR.casefold() in message.casefold():
            self.parent_self.close()
        print(f"js: {message}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube on TV")
        self.setWindowIcon(QIcon.fromTheme("com.webyfy.yttv"))

        webview = QWebEngineView()
        webview.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        webview.setContextMenuPolicy(Qt.NoContextMenu)
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(USER_AGENT)
        webpage = WebEnginePage(self, profile, webview)
        webpage.windowCloseRequested.connect(self.close)
        webview.setPage(webpage)
        webview.load(QUrl("https://www.youtube.com/tv"))

        self.setCentralWidget(webview)

