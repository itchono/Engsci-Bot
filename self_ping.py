from flask import Flask
# used to create web server to keep bot actively hosted
from threading import Thread
# used to create separate parallel process to keep bot up

import logging
import os

from utils.utilities import get_uptime
from utils.logger import logger

# disable flask dumb logging
logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

app = Flask('')


@app.route('/')
def main():
    return f"Bot is online. Uptime: {get_uptime()}"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()
    logger.info("Flask server started.")
