import json
import logging
import os
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from time import perf_counter
from typing import Dict, Iterator, Optional


SENSITIVE_HEADERS = {"authorization", "x-api-key"}


def _ensure_reports_dir(reports_dir: Optional[str] = None) -> Path:
    directory = Path(reports_dir or "reports").resolve()
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def redact_headers(headers: Optional[Dict[str, str]]) -> Dict[str, str]:
    if not headers:
        return {}
    redacted = dict(headers)
    for key in list(redacted.keys()):
        if key.lower() in SENSITIVE_HEADERS:
            redacted[key] = "<redacted>"
    return redacted


@contextmanager
def log_timing(logger: logging.Logger, message: str):
    start = perf_counter()
    try:
        yield
    finally:
        duration_ms = int((perf_counter() - start) * 1000)
        logger.info("%s in %dms", message, duration_ms)


class TcLogger:
    """
    Logger helper to log test names and configure handlers (console/file).
    Writes log files into ./reports by default.
    """

    __logger: Optional["TcLogger"] = None

    def __init__(self, level: int = 100, logger_name: str = "TITLE"):
        self._level = level
        self._logger_name = logger_name
        logging.addLevelName(self._level, self._logger_name)

    @classmethod
    def get_log(cls) -> "TcLogger":
        if not cls.__logger:
            cls.__logger = TcLogger()
        return cls.__logger

    def log_test_name(self, test_name: str) -> None:
        logging.log(self._level, test_name)

    @staticmethod
    def generate_logs(
        *,
        level: str = "INFO",
        detailed_logs: bool = False,
        write_to_file: bool = True,
        reports_dir: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> None:
        """
        Configure root logger handlers. If write_to_file is True, create a log file
        under ./reports (or provided reports_dir). If detailed_logs is True, also
        stream to stdout with the same formatter.
        """
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        # Avoid duplicate handlers if called multiple times
        logger.handlers = []

        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)-4s %(filename)s [LINE:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

        if detailed_logs:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(formatter)
            logger.addHandler(stdout_handler)

        if write_to_file:
            reports_path = _ensure_reports_dir(reports_dir)
            ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            file_name = filename or f"test_log_{ts}.log"
            file_handler = logging.FileHandler(str(reports_path / file_name), mode='a')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
            logger.addHandler(file_handler)
