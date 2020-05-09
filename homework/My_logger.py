from functools import wraps
import logging
import sqlite3


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


def my_logging_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None and func.__name__ == "__init__":
                good_log.info(f"Поступил новый пациент: {args[0]}")
                return
            if result is None or func.__name__ == "read_patients_from_db":
                return
            # Смотрим флаг изменения поля
            if result.alter_flag == 1:
                good_log.info(f"Изменение поля {result.name} объекта {args[0]}")
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

def db_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            if result is None:
                good_log.info(f"Пациент {args[0]} записан в бд")
        except sqlite3.IntegrityError as err:
            bad_log.error(f'пользователь {args[0]} уже существует. {err}')
        except sqlite3.OperationalError as err:
            bad_log.error(f'Данной таблицы не существует. {err}')
        except Exception as err:
            bad_log.error(f"Ошибка записи в бд: {err}")
        return result
    return wrapper






