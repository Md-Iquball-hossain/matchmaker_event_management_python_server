# Author: Shidul Islam
# Date: 10-11-2023
# */

from app.database import conn


def create_exception_service(payload):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        # connection.autocommit = True
        # cursor.execute(
        #     "SELECT * from dbo.log_exception(%s, %s)", payload)
        print("payload", payload)
        error_body = (
            payload['stack_trace'], payload['user_id'], payload['exception_message'], payload['exception_type'])
        print("error_body", error_body)
        # cursor.callproc('dbo.log_exception', error_body)
        cursor.execute(
            "SELECT * from dbo.log_exception(%s, %s, %s, %s)", error_body)
        exception_id = cursor.fetchone()[0]
        # cursor.close()

        return exception_id
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
