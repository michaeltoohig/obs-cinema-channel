import logging
import sys

import structlog

from cinema_playout.telegram import send_message


def send_telegram_alerts(
    logger: logging.Logger, method_name: str, event_dict: structlog.typing.EventDict
) -> structlog.typing.EventDict:
    """
    Error level logs or higher are sent via Telegram.
    """
    log_level = structlog.stdlib._NAME_TO_LEVEL[method_name]
    if log_level >= logging.ERROR:
        message = event_dict["event"]
        try:
            send_message(message)
        except:
            # telegram failed for some reason
            pass

    return event_dict


def configure_logger(strict, level=logging.INFO) -> None:
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        send_telegram_alerts,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.StackInfoRenderer(),
    ]
    if strict:
        processors += [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors += [
            structlog.dev.ConsoleRenderer(
                exception_formatter=structlog.dev.rich_traceback,
            ),
        ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
