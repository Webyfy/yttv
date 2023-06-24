import logging

def intialize_logging(debug):
    """
    Initialize the logging framework
    """
    # Configure logging.
    root_logger = logging.getLogger()
    log_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s]: %(message)s')
    if debug:
        root_logger.setLevel(logging.DEBUG)