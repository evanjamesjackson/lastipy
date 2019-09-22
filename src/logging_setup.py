from src import definitions
import logging
import os


def setup_logging():
    logs_directory = os.path.join(definitions.ROOT_DIR, 'logs')
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Instantiating with the name __package__ works because this file is in the topmost package
    logger = logging.getLogger(__package__)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(logs_directory, 'spotify_recommender.log'),
        maxBytes=2 * 1024 * 1024,  # 2MB
        backupCount=25,
        encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)