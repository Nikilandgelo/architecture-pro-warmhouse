import logging


def setup_logger(name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        style="{",
        fmt="[{name}] {levelname} - {asctime}: {message}"
    ))
    logger.addHandler(handler)
    return logger

service_logger = setup_logger("Automation Engine", logging.DEBUG)
