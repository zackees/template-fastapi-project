"""
Logging module for personalmonitor_collector.
"""

import os
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
    # Use an absolute path to prevent file rotation trouble.
    logfile = os.path.join(LOG_SYSTEM)
    # Rotate log after reaching LOG_SIZE, keep LOG_HISTORY old copies.
    rotate_handler = ConcurrentRotatingFileHandler(
        logfile, "a", LOG_SIZE, LOG_HISTORY, use_gzip=LOGGING_USE_GZIP, encoding="utf-8"
    )
    rotate_handler.setFormatter(Formatter(LOGGING_FMT))
    log.addHandler(rotate_handler)
    log.setLevel(INFO)
    formatter = Formatter(LOGGING_FMT)
    strmhandler = StreamHandler()
    strmhandler.setFormatter(formatter)
    log.addHandler(strmhandler)
    return log


def reverse_readline(filename, buf_size=8192):
    """A generator that returns the lines of a file in reverse order"""
    with open(filename, encoding="utf-8", mode="r") as filehandle:
        segment = None
        offset = 0
        file_size = remaining_size = filehandle.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            filehandle.seek(file_size - offset)
            buffer = filehandle.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split("\n")
            # The first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # If the previous chunk starts right from the beginning of line
                # do not concat the segment to the last line of new chunk.
                # Instead, yield the segment first
                if buffer[-1] != "\n":
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if lines[index]:
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment


def get_log_reversed(num_lines: int) -> str:
    """Returns the log in reverse line order"""
    lines = []
    remaining_lines = num_lines
    with FileReadBackwards("LOG_SYSTEM", encoding="utf-8") as frb:
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
