import sys
from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import (QApplication, QMainWindow)
from PySide2.QtWebEngineWidgets import (QWebEngineView, 
                                        QWebEngineProfile, QWebEnginePage)

USER_AGENT = 'Roku/DVP-23.0 (23.0.0.99999-02)'
YTTV_URL = QUrl('https://www.youtube.com/tv')

class YTTV(QMainWindow):
    def __init__(self):
        super(YTTV, self).__init__()
        self.initUI()

    def initUI(self):
        self.webEngineView = QWebEngineView(self)

        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(USER_AGENT)
        self.webEngineView.page().profile = profile

        self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        self.webEngineView.setUrl(YTTV_URL)

        self.setCentralWidget(self.webEngineView)

        self.setWindowTitle('YouTube on TV')
        self.resize(QGuiApplication.primaryScreen().availableGeometry().size() * 0.7)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QApplication(sys.argv)
    ex = YTTV()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()