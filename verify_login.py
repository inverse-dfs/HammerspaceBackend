import logging

from db import database

def verify_login(username, password):
    logging.basicConfig(level=logging.DEBUG, force=True)
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)
    try:
        db = database()
        query = ("SELECT u.user_pass FROM User as u WHERE u.username = %s")
        result = db.execute(query, [username])
        log.debug("starting password comp")
        for r in result:
            password = (password,)
            log.debug(r)
            log.debug(password)
            if r == password:
                return "Login Validated"
        return "Login Rejected"
    except Exception as e:
        log.error("I have failed brother")
        log.debug(e)
        return "Server Error"