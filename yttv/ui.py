import logging
from PySide2 import QtTest
from PySide2.QtGui import QIcon, QKeySequence, QKeyEvent
from PySide2.QtCore import QUrl, Qt, QEvent, QTimer
from PySide2.QtWidgets import QMainWindow, QShortcut, QApplication
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

        if (level == QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel):
            logging.info(f"js: {message}")
        elif (level == QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel):
            logging.warn(f"js: {message}")
        else: # QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel
            logging.error(f"js: {message}")
            

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube on TV")
        self.setWindowIcon(QIcon.fromTheme("com.webyfy.yttv"))

        # Create a QShortcut for the XF86Back key
        self.xf86back_shortcut = QShortcut(QKeySequence('Back'), self)
        # Connect the shortcut to a function that emits an escape key press
        self.xf86back_shortcut.activated.connect(lambda: self.fake_key_press(Qt.Key_Escape))

        self.webview = QWebEngineView()
        self.webview.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        self.webview.setContextMenuPolicy(Qt.NoContextMenu)
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(USER_AGENT)
        webpage = WebEnginePage(self, profile, self.webview)
        webpage.windowCloseRequested.connect(self.close)
        self.webview.setPage(webpage)
        self.webview.load(QUrl("https://www.youtube.com/tv"))

        self.setCentralWidget(self.webview)

    # shamelessly copy/pasted from qute browser
    def fake_key_press(self,
                       key: Qt.Key,
                       modifier: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier) -> None:
        """Send a fake key event."""
        press_evt = QKeyEvent(QEvent.Type.KeyPress, key, modifier, 0, 0, 0)
        release_evt = QKeyEvent(QEvent.Type.KeyRelease, key, modifier,
                                0, 0, 0)
        self.send_event(press_evt)
        self.send_event(release_evt)

    def send_event(self, evt: QEvent) -> None:
        """Send the given event to the underlying widget.

        The event will be sent via QApplication.postEvent.
        Note that a posted event must not be re-used in any way!
        """
        # This only gives us some mild protection against re-using events, but
        # it's certainly better than a segfault.
        if getattr(evt, 'posted', False):
            logging.error("Can't re-use an event which was already "
                                    "posted!")
            return

        recipient = self.webview.focusProxy()
        evt.posted = True  # type: ignore[attr-defined]
        QApplication.postEvent(recipient, evt)
