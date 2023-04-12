import json
import os
from datetime import datetime

log_file = f"Resources/log_{str(datetime.now()).replace(' ', '_').replace(':', '_')}.txt"


def log_to_logging_file(message: str):
    message = f"\n{message}"
    if os.path.isfile(log_file):
        with open(log_file, 'a') as f:
            f.write(message)
    else:
        with open(log_file, 'w') as f:
            f.write(message)
