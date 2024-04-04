import yttv.yawebview as yawebview
import logging
from yttv import utility
import atexit
import argparse

USER_AGENT = 'Roku/DVP-23.0 (23.0.0.99999-02)'
YTTV_URL = 'https://www.youtube.com/tv'

def intialize_logging(debug:bool =False):
    """
    Initialize the logging framework
    """
    # Configure logging.
    root_logger = logging.getLogger()
    log_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s]: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
    if debug:
        root_logger.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(prog='yttv', description='YouTube for 10 foot UI with D-pad navigation.')
    parser.add_argument('-d', '--debug', help='start YouTube on TV in debug mode', action='store_true')
    args = parser.parse_args()
    intialize_logging(args.debug)
    window = yawebview.Window(
        'YouTube on TV', YTTV_URL, scrollbars=False, context_menu=False, allow_scripts_to_close=True)

    icon_file = utility.get_icon_path("com.webyfy.yttv.png")
    window.set_icon("com.webyfy.yttv", [str(icon_file),])

    window.add_keymapping('Back', 'Escape')

    yawebview.start(options=yawebview.Options(
        user_agent=USER_AGENT,
        single_instance_mode=True,
        app_id="com.webyfy.yttv"
    ))

if __name__ == "__main__":
    main()
