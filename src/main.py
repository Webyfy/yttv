#!/usr/bin/env python3

import sys
from PySide2.QtCore import QUrl
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
            self.parent_window.close()
        print(f"js: {message}")


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("YouTube on TV")

    webview = QWebEngineView()
    webview.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
    profile = QWebEngineProfile.defaultProfile()
    profile.setHttpUserAgent(USER_AGENT)
    webpage = WebEnginePage(window, profile, webview)
    webpage.windowCloseRequested.connect(window.close)
    webview.setPage(webpage)
    webview.load(QUrl("https://www.youtube.com/tv"))

    window.setCentralWidget(webview)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
