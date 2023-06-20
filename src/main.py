#!/usr/bin/env python3

import sys
from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QApplication,QMainWindow
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEnginePage

USER_AGENT = 'Roku/DVP-23.0 (23.0.0.99999-02)'

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("YouTube on TV")

    webview = QWebEngineView()
    webview.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
    profile = QWebEngineProfile.defaultProfile()
    profile.setHttpUserAgent(USER_AGENT)
    webpage = QWebEnginePage(profile, webview)
    webpage.windowCloseRequested.connect(window.close)
    webview.setPage(webpage)
    webview.load(QUrl("https://www.youtube.com/tv"))

    window.setCentralWidget(webview)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
