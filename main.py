import logging

from settings import Config
from watcher.watcher import Watcher

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

if __name__ == "__main__":
    config = Config()
    config.load_required()

    watcher = Watcher(config)
    watcher.run()
