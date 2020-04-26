from homework import My_logger
import logging
import re

class Patient:
    """Класс содержит основные данные о пациенте"""

    first_name = NotImplemented
    last_name = NotImplemented

    def __init__(self, name, surname, birth_date, phone_number, doc_type, doc_number):
        self.good_log = logging.getLogger("logger_access")
        self.bad_log = logging.getLogger("logger_error")
        try:
            self.first_name_ = name
            self.last_name_ = surname
            self.birth_date = birth_date
            self.phone = phone_number
            self.document_type = doc_type
            self.document_id = doc_number
            self.good_log.info(f"Поступил новый пациент: {self}")
        except TypeError as err:
            self.bad_log.error(f"Ошибка записи пациента: {err}")
            raise err
        except ValueError as err:
            self.bad_log.error(f"Ошибка записи пациента: {err}")
            raise err
        except Exception as err:
            self.bad_log.error(f"{err}")
            raise err

    def __str__(self):
        out = f"{self._first_name} " \
              + f"{self._last_name} " \
              + f"{self.birth_date} " \
              + f"{self.phone} " \
              + f"{self.document_type} " \
              + f"{self.document_id}"
        return out



    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    @My_logger.log
    def first_name(self, name):
        raise AttributeError("Нельзя изменять значения поля first_name")


    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    @My_logger.log
    def last_name(self, name):
        raise AttributeError("Нельзя изменять значения поля last_name")


    @property
    def first_name_(self):
        return self._first_name

    @first_name_.setter
    def first_name_(self, name):
        if not isinstance(name, str):
            raise TypeError(f"Неправильный тип данных поля first_name {type(name)} is not str")
        if not name.isalpha():
            raise ValueError(f"Имя должно содержать только символы {name}")
        self._first_name = name

    @property
    def last_name_(self):
        return self._last_name

    @last_name_.setter
    def last_name_(self, surname):
        if not isinstance(surname, str):
            raise TypeError(f"Неправильный тип данных поля last_name {type(surname)} is not str")
        if not surname.isalpha():
            raise ValueError(f"Фамилия должна содержать только символы {surname}")
        self._last_name = surname

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    @My_logger.log
    def birth_date(self, date):
        if not isinstance(date, str):
            raise TypeError(f"Неправильный тип данных поля birth_date {type(date)} is not str")
        format1 = re.search("^(\d{2}[\-|\.| ]?){2}\d{4}$", date) is None
        format2 = re.search("^\d{4}[\-|\.| ]?\d{2}[\-|\.| ]\d{2}$", date) is None
        if format1 and format2:
            raise ValueError(f"Неправильная дата рождения {date}")
        if not format1:
            day, mounth, year = date[0:2], date[3:5], date[6:]
            assert (2020 - int(year)) < 150, "Неправильная дата рождения"
        else:
            year, mounth, day = date[0:4], date[5:7], date[8:]
            assert (2020 - int(year)) < 150, "Неправильная дата рождения"
        if hasattr(self, '_birth_date'):
            self.good_log.info(f"Изменение поля birth_date объекта {self}")
        self._birth_date = '-'.join([year, mounth, day])


    @property
    def phone(self):
        return self._phone

    @phone.setter
    @My_logger.log
    def phone(self, phone):
        if not isinstance(phone, str):
            raise TypeError(f"Неправильный тип данных поля phone {type(phone)} is not str")
        if re.search("[\+7|8]?([\(| |\-]?[\d]{3}[\)| |\-]?){2}([\-| ]?[\d]{2}[\-| ]?){2}", phone) is None:
            raise ValueError(f"Неправильный номер телефона {phone}")
        phone = ''.join(filter(str.isdigit, phone))
        if len(phone) < 11:
            phone = '7' + phone
        phone = f'+7-{phone[1:4]}-{phone[4:7]}-{phone[7:9]}-{phone[9:11]}'
        if hasattr(self, '_phone'):
            self.good_log.info(f"Изменение поля phone объекта {self}")
        self._phone = phone

    @property
    def document_type(self):
        return self._document_type

    @document_type.setter
    @My_logger.log
    def document_type(self, document):
        if not isinstance(document, str):
            raise TypeError(f"Неправильный тип данных поля document_type {type(document)} is not str")
        document = document.lower()
        if document not in {"паспорт", "заграничный паспорт", "водительские права"}:
            raise ValueError(f"Неправильный тип документов {document}")
        if hasattr(self, '_document_type'):
            self.good_log.info(f"Изменение поля document_type объекта {self}")
        self._document_type = document


    @property
    def document_id(self):
        return self._document_id

    @document_id.setter
    @My_logger.log
    def document_id(self, doc_number):
        if not isinstance(doc_number, str):
            raise TypeError(f"Неправильный тип данных поля document_id {type(doc_number)} is not str")
        if self.document_type == "паспорт":
            if re.search("^([\d][ |\-|\-|\/]?){10}$", doc_number) is None:
                raise ValueError(f"Неправильный номер паспорта {doc_number}")
            doc_number = ''.join(filter(str.isdigit, doc_number))
            doc_number = doc_number[:4] + " " + doc_number[4:]
        if self.document_type == "заграничный паспорт":
            if re.search("^([\d][ |\-|\-|\/]?){9}$", doc_number) is None:
                raise ValueError(f"Неправильный номер заграничного паспорта {doc_number}")
            doc_number = ''.join(filter(str.isdigit, doc_number))
            doc_number = doc_number[:2] + " " + doc_number[2:]
        if self.document_type == "водительские права":
            if re.search("^([\d][ |\-|\-|\/]?){10}$", doc_number) is None:
                raise ValueError(f"Неправильный номер прав {doc_number}")
            doc_number = ''.join(filter(str.isdigit, doc_number))
            doc_number = doc_number[:2] + " " + doc_number[2:4] + " " + doc_number[4:]
        if hasattr(self, '_document_id'):
            self.good_log.info(f"Изменение поля document_id объекта {self}")
        self._document_id = doc_number


    @staticmethod
    def create(*args):
        return Patient(*args)

    def save(self, filename="Patients.csv"):
        data = [self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id]
        data = ','.join(data)
        data += '\n'
        try:
            with open(filename, 'a', encoding="utf-8") as file:
                file.write(data)
            self.good_log.info(f"Пациент {self} записан в файл")
        except FileExistsError as err:
            self.bad_log.error(f'Файл {filename} уже существует. {err}')
        except FileNotFoundError as err:
            self.bad_log.error(f'Файла {filename} не существует. {err}')
        except IsADirectoryError as err:
            self.bad_log.error(f'{filename} это директория {err}')
        except PermissionError as err:
            self.bad_log.error(f'У вас недостаточно прав для операции записи. {err}')
        except Exception as err:
            self.bad_log.error(f"Ошибка записи в файл: {err}")


class Iterator:
    """Итератор для прохождения по коллекции"""

    def __init__(self, filename, limit=None):
        self.limit = limit
        self.file = open(filename, 'r',  encoding="utf-8")

    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()
        line = line.rstrip('\n')
        if line == "":
            raise StopIteration
        if (self.limit is not None) and self.limit == 0:
            raise StopIteration
        if self.limit is not None:
            self.limit -= 1
        return Patient(*line.split(','))

    def __del__(self):
        self.file.close()


class PatientCollection:

    def __init__(self, filename='Patients.csv'):
        self.good_log = logging.getLogger("logger_access")
        self.bad_log = logging.getLogger("logger_error")
        self.filename = filename
        self.data = self.read_patients_from_file(filename)

    def __getitem__(self, key):
        return self.data[key]


    def __iter__(self):
        return Iterator(self.filename)

    def limit(self, limit=None):
        return Iterator(self.filename, limit)

    def read_patients_from_file(self, filename):
        data = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    p = Patient(*line.split(','))
                    data.append(p)
        except Exception as err:
            self.bad_log.error(f"Ошибка {err} чтения пациентов из файла {filename}")
        finally:
            return tuple(data)
