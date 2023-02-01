"""
Logging module for personalmonitor_collector.
"""

from pathlib import Path
from logging import getLogger, INFO, Logger, Formatter, StreamHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler  # type: ignore
from file_read_backwards import FileReadBackwards  # type: ignore
from fastapi_template_project.settings import (
    LOG_SIZE,
    LOG_HISTORY,
    LOGGING_FMT,
    LOGGING_USE_GZIP,
    LOG_SYSTEM,
)


def make_logger(name: str) -> Logger:
    """TODO - Add description."""
    log = getLogger(name)
    Path(LOG_SYSTEM).touch(exist_ok=True)
    # Rotate log after reaching LOG_SIZE, keep LOG_HISTORY old copies.
    rotate_handler = ConcurrentRotatingFileHandler(
        LOG_SYSTEM,
        "a",
        LOG_SIZE,
        LOG_HISTORY,
        use_gzip=LOGGING_USE_GZIP,
        encoding="utf-8",
    )
    rotate_handler.setFormatter(Formatter(LOGGING_FMT))
    log.addHandler(rotate_handler)
    log.setLevel(INFO)
    formatter = Formatter(LOGGING_FMT)
    strmhandler = StreamHandler()
    strmhandler.setFormatter(formatter)
    log.addHandler(strmhandler)
    return log


def get_log_reversed(num_lines: int) -> str:
    """Returns the log in reverse line order"""
    lines = []
    remaining_lines = num_lines
    with FileReadBackwards(LOG_SYSTEM, encoding="utf-8") as frb:
        for line in frb:
            if remaining_lines <= 0:
                break
            remaining_lines -= 1
            lines.append(line)
    return "\n".join(lines)


def main() -> None:
    """TODO - Add description."""
    logger = make_logger(__name__)
    logger.info("Hello world")


if __name__ == "__main__":
    main()
