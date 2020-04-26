from functools import wraps
import logging


formatter = logging.Formatter(
        '[%(asctime)s] - %(levelname)s - %(funcName)s - line %(lineno)d - %(module)s - %(message)s')

good_log = logging.getLogger("logger_access")
good_log.setLevel(logging.INFO)
handler_access = logging.FileHandler("access.log")
handler_access.setFormatter(formatter)
good_log.addHandler(handler_access)


bad_log = logging.getLogger("logger_error")
bad_log.setLevel(logging.ERROR)
handler_error = logging.FileHandler("error.log")
handler_error.setFormatter(formatter)
bad_log.addHandler(handler_error)

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TypeError as err:
            bad_log.error(f"Ошибка записи пациента: {err}")
            raise err
        except ValueError as err:
            bad_log.error(f"Ошибка записи пациента: {err}")
            raise err
        except Exception as err:
            bad_log.error(f"{err}")
            raise err
    return wrapper






