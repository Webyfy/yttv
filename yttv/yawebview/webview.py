import sys
from PySide2.QtCore import QUrl, Qt, QEvent
from PySide2.QtGui import QGuiApplication, QIcon, QPixmap, QKeySequence, QKeyEvent
from PySide2.QtWidgets import (QApplication, QMainWindow, QShortcut)
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
        self.keymappings : Dict[str, str] = {}

    def set_icon(self, icon_name: str, fallback_icon_files: List[str] = []):
        self.icon_set = True
        self.icon_name = icon_name
        self.fallback_icon_files = fallback_icon_files

    def add_keymapping(self, src_key_sequence: str, dest_key_sequence: str):
        self.keymappings[src_key_sequence] = dest_key_sequence



class BrowserView(QMainWindow):
    def __init__(self, window: Window, user_agent: Optional[str] = None):
        super().__init__()
        self.initUI(window=window, user_agent=user_agent)

    def initUI(self, window: Window, user_agent: Optional[str]):
        for src_seq in window.keymappings.keys():
            src_q_key_seq = QKeySequence(src_seq)
            if src_q_key_seq.toString() == "":
                logging.warning(f"Invalid key sequence '{src_seq}'")
                continue
            dest_seq = window.keymappings[src_seq]
            dest_q_key_seq =QKeySequence(dest_seq)
            if dest_q_key_seq.toString() == "":
                logging.warning(f"Invalid key sequence '{dest_seq}'")
                continue
            shortcut = QShortcut(src_q_key_seq, self)
            # Hacky solution, but works for my requirements
            shortcut.activated.connect(lambda: self.fake_key_press(dest_q_key_seq[0]))

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

        recipient = self.webEngineView.focusProxy()
        evt.posted = True  # type: ignore[attr-defined]
        QApplication.postEvent(recipient, evt)

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
