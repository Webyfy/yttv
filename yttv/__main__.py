#!/usr/bin/env python3
import argparse
import logging
import sys

from yttv import utility
from yttv.QtSingleApplication import QtSingleApplication
from yttv.ui import MainWindow

APP_ID = "com.webyfy.yttv"

def main():
    parser = argparse.ArgumentParser(prog='yttv', description='YouTube for 10 foot UI with D-pad navigation.')
    parser.add_argument('-d', '--debug', help='start YouTube on TV in debug mode', action='store_true')
    args = parser.parse_args()
    utility.intialize_logging(args.debug)

    app = QtSingleApplication(APP_ID, sys.argv)
    utility.crash_handler(app)
    if app.isRunning():
        logging.info("YouTube on TV is already running")
        sys.exit(0)
    
    w = MainWindow()
    w.show()
    app.setActivationWindow(w)
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
