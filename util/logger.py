import logging
import logging.config
import inspect
import re
from django.conf import settings
from typing import Any


class Logger():
    def __init__(self):
        config = {
            'version': 1,
            'filters': {
                'trid': {
                    '()': 'middleware.context.TRIDFilter'
                }
            },
            'formatters': {
                'standard': {
                    'class': 'logging.Formatter',
                    'format': '{"l":"%(levelname)s","trid":"%(trid)s","t":"%(asctime)s",%(message)s}',
                    'datefmt': '%Y/%m/%d %H:%I:%S%z',
                },
            },
            'handlers': {
                'app': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard',
                    'filters': ['trid'],
                },
            },
            'loggers': {
                'root': {
                    'handlers': ['app'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
            },
        }
        logging.config.dictConfig(config)

    def _getPrev(self) -> dict[str, str | int]:
        frame = inspect.currentframe()
        if frame != None and frame.f_back != None and frame.f_back.f_back != None and frame.f_back.f_back.f_back != None:
            frame = frame.f_back.f_back.f_back
        
        if frame == None:
            return {
                'file': 'UnKnonw',
                'line': 'UnKnonwn',
            }
        
        file = re.sub(rf'^{settings.BASE_DIR}/', '',
                      frame.f_code.co_filename)
        return {
            'file': file,
            'line': frame.f_lineno,
        }

    def __getFmtMsg(self, msg: str, **kwargs) -> str:
        fmtMsg = ''
        if msg != '':
            fmtMsg = f'"msg":"{msg}"'

        for key, val in kwargs.items():
            fmtMsg += f',"{key}":"{val}"'

        prev = self._getPrev()
        fmtMsg += f',"caller":"{prev["file"]}:{prev["line"]}"'
        return fmtMsg

    def __getRoot(self) -> logging.Logger:
        return logging.getLogger()

    def info(self, msg: str, **kwargs) -> None:
        self.__getRoot().info(self.__getFmtMsg(msg, **kwargs))

    def warning(self, msg: str, **kwargs) -> None:
        self.__getRoot().warning(self.__getFmtMsg(msg, **kwargs))

    def error(self, msg: str, **kwargs) -> None:
        self.__getRoot().error(self.__getFmtMsg(msg, **kwargs))

    def debug(self, msg: str, **kwargs) -> None:
        self.__getRoot().warning(self.__getFmtMsg(msg, **kwargs))


logger = Logger()
