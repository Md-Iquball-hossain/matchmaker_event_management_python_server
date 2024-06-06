# Author: Shidul Islam
# Date: 10-11-2023
# */

from logging import LogRecord
from flask import Flask
from app.database import conn
import logging

app = Flask(__name__)


class MySqlHandler(logging.Handler):
    def emit(self, record: LogRecord):

        connection = conn.getconn()
        cursor = connection.cursor()

        cursor.callproc('insert_log', (record.created,
                        record.levelname, record.getMessage()))
        connection.commit()
