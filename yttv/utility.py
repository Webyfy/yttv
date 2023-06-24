import logging

def intialize_logging(debug):
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