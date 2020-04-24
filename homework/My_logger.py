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




def init_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = exception = None
        try:
            result = func(*args, **kwargs)
            good_log.info(f"Поступил новый пациент: {args[0]}")
            return result
        except Exception as err:
            bad_log.error(f"Ошибка записи пациента: {err}")
            exception = err
        if exception is not None:
            raise exception
    return wrapper


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = exception = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as err:
            bad_log.error(f"{err}")
            exception = err
        if exception is not None:
            raise exception
    return wrapper






