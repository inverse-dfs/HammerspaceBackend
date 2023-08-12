import logging
import uuid

from db import database

def insert_user(username, email, password):
    logging.basicConfig(level=logging.DEBUG, force=True)
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)
    try:
        db = database()
        query = ("SELECT * FROM User as u WHERE u.email = %s OR u.username=%s")
        result = db.execute(query, [email, username])
        if result != []:
            return "Invalid username or email provided, already exists!"
        query = "Insert into User(email, username, password) VALUES(%s, %s, %s)"
        result = db.execute(query, [email, username, password])
        return "success"

    except Exception as e:
        log.debug(e)
        return "failxure"
