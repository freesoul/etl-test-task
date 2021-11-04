import logging


def configure_root_logger():
    import logging.handlers

    f = logging.Formatter(fmt="%(asctime)s %(levelname)s :%(name)s: %(message)s ", datefmt="%Y-%m-%d %H:%M:%S")
    handlers = [
        logging.handlers.RotatingFileHandler("%s.log" % __name__, encoding="utf8", maxBytes=100000, backupCount=1),
        logging.StreamHandler(),
    ]
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    for h in handlers:
        h.setFormatter(f)
        h.setLevel(logging.DEBUG)
        root_logger.addHandler(h)
    logging.getLogger("requests").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    return root_logger