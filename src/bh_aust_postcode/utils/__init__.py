"""
Some generic helper functions.
"""

def print_log(logger: object, msg: str, cateogry: str):
    """Print to stdout and log to file a message. 

    :param object logger: the actual logger instance.
    :param str msg: the message to print and to log.
    :param str cateogry: the logging cateogry -- info, debug, error, exception.
    """

    print(msg)
    method = getattr(logger, cateogry, None)
    method(msg)
