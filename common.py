import logging
import os


LOG_LEVEL = os.environ.get('LOG_LEVEL', 'info')


def setup_logging():
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=fmt, level=getattr(logging, LOG_LEVEL.upper()))
