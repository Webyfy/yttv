import argparse
import logging

import yawebview

from yttv import YTTV_VERSION, utility

USER_AGENT = "Roku/DVP-23.0 (23.0.0.99999-02)"
YTTV_URL = "https://www.youtube.com/tv"


def intialize_logging(debug: bool = False):
    """
    Initialize the logging framework
    """
    # Configure logging.
    root_logger = logging.getLogger()
    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s]: %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
    if debug:
        root_logger.setLevel(logging.DEBUG)


def get_parser():
    parser = argparse.ArgumentParser(
        prog="yttv",
        description="YouTube for 10 foot UI with D-pad navigation.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="start YouTube on TV in debug mode",
        action="store_true",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + YTTV_VERSION
    )
    parser.add_argument(
        "--freeze-on-focus-loss",
        help="Freeze App on losing focus",
        action="store_true",
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    intialize_logging(args.debug)
    window = yawebview.Window(
        "YouTube on TV",
        YTTV_URL,
        scrollbars=False,
        context_menu=False,
        allow_scripts_to_close=True,
        freeze_on_focus_loss=args.freeze_on_focus_loss,
    )

    icon_file = utility.get_icon_path("com.webyfy.yttv.png")
    window.set_icon(
        "com.webyfy.yttv",
        [
            str(icon_file),
        ],
    )

    window.add_keymapping("Back", "Escape")

    yawebview.start(
        options=yawebview.Options(
            user_agent=USER_AGENT,
            single_instance_mode=True,
            app_id="com.webyfy.yttv",
        )
    )


if __name__ == "__main__":
    main()
