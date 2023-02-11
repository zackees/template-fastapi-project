"""
Logging module for personalmonitor_collector.
"""

from logging import INFO, Formatter, Logger, StreamHandler, getLogger
from pathlib import Path

from concurrent_log_handler import ConcurrentRotatingFileHandler  # type: ignore
from file_read_backwards import FileReadBackwards  # type: ignore

from androidmonitor_backend.settings import (
    LOG_HISTORY,
    LOG_SIZE,
    LOG_SYSTEM,
    LOGGING_FMT,
    LOGGING_USE_GZIP,
)


def make_logger(name: str, logname: str | None = None) -> Logger:
    """TODO - Add description."""
    log = getLogger(name)
    logname = logname or LOG_SYSTEM
    Path(logname).touch(exist_ok=True)
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
