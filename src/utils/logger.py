# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\utils\\logger.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nLogging system for Shulker V2\n"""
import logging
import os
import sys
import platform
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init
init(autoreset=True)
def _get_logs_dir():
    """\nGet logs directory - hidden from users\nReturns AppData location when running as EXE, or hidden logs folder in dev mode\n"""
    is_frozen = getattr(sys, 'frozen', False)
    if is_frozen:
        if platform.system() == 'Windows':
            appdata = os.getenv('APPDATA')
            if appdata:
                logs_dir = Path(appdata) / 'ShulkerV2' / 'logs'
            else:
                logs_dir = Path.home() / '.shulkerv2' / 'logs'
        else:
            logs_dir = Path.home() / '.shulkerv2' / 'logs'
    else:
        if platform.system() == 'Windows':
            logs_dir = Path('.logs')
        else:
            logs_dir = Path('.logs')
    logs_dir.mkdir(parents=True, exist_ok=True)
    if platform.system() == 'Windows':
        try:
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(str(logs_dir), 2)
        except:
            pass
    return str(logs_dir)
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    COLORS = {'DEBUG': Fore.CYAN, 'INFO': Fore.GREEN, 'WARNING': Fore.YELLOW, 'ERROR': Fore.RED, 'CRITICAL': Fore.RED + Style.BRIGHT}
    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f'{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}'
        return super().format(record)
def setup_logger(name='shulker', level=logging.INFO):
    """\nSetup logger with console handler only (no file logging)\n\nArgs:\n    name: Logger name\n    level: Logging level\n\nReturns:\n    Logger instance\n"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:
        return logger
    else:
        is_frozen = getattr(sys, 'frozen', False)
        if not is_frozen:
            logs_dir = _get_logs_dir()
            log_file = os.path.join(logs_dir, f'shulker_{datetime.now().strftime('%Y%m%d')}.log')
            file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter('%(levelname)-8s | %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        return logger
def get_logger(name='shulker'):
    """Get existing logger instance"""
    return logging.getLogger(name)