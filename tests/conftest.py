import os

os.environ["ENV"] = "test"  # must be specifed before importing app config

from app.config import config

config.LOGS_PATH.parent.mkdir(exist_ok=True)
config.LOGS_PATH.write_text("")  # clear test-logs before tests
