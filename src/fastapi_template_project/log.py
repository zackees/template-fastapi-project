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
    LOG_DIR,
    LOGGING_FMT,
    LOGGING_USE_GZIP,
)


def _get_log_path(logname: str | None = None) -> str:
    """TODO - Add description."""
    if logname is None:
        logname = LOG_SYSTEM
    else:
        # if not an absolute path
        if not Path(logname).is_absolute():
            # make it relative to the project root
            logname = str(Path(LOG_DIR, logname))
    Path(logname).touch(exist_ok=True)
    return logname


def make_logger(name: str, logname: str | None = None) -> Logger:
    """TODO - Add description."""
    log = getLogger(name)
    logpath = _get_log_path(logname)
    # Rotate log after reaching LOG_SIZE, keep LOG_HISTORY old copies.
    rotate_handler = ConcurrentRotatingFileHandler(
        logpath,
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
