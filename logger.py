import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger('etl_application')
logger.setLevel(logging.INFO)

fh = RotatingFileHandler('logs/etl_logs.log', maxBytes=20_000_000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s'
)
fh.setFormatter(formatter)
logger.addHandler(fh)

