import My_logger
#from homework import My_logger
import sqlite3
import re
from collections import namedtuple

class Patient:
    """Класс содержит основные данные о пациенте"""

    @My_logger.my_logging_decorator
    def __init__(self, name, surname, birth_date, phone_number, doc_type, doc_number):
        self.first_name = name
        self.last_name = surname
        self.birth_date = birth_date
        self.phone = phone_number
        self.document_type = doc_type
        self.document_id = doc_number

    def __str__(self):
        out = f"{self.first_name} " \
              + f"{self.last_name} " \
              + f"{self.birth_date} " \
              + f"{self.phone} " \
              + f"{self.document_type} " \
              + f"{self.document_id}"
        return out



    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    @My_logger.my_logging_decorator
    def first_name(self, name):
        if "_first_name" in self.__dict__:
            raise AttributeError("Нельзя изменять значения поля first_name")
        if not isinstance(name, str):
            raise TypeError(f"Неправильный тип данных поля first_name {type(name)} is not str")
        if not name.isalpha():
            raise ValueError(f"Имя должно содержать только символы {name}")
        self.__dict__["_first_name"] = name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    @My_logger.my_logging_decorator
    def last_name(self, surname):
        if "_last_name" in self.__dict__:
            raise AttributeError("Нельзя изменять значения поля last_name")
        if not isinstance(surname, str):
            raise TypeError(f"Неправильный тип данных поля last_name {type(surname)} is not str")
        if not surname.isalpha():
            raise ValueError(f"Фамилия должна содержать только символы {surname}")
        self.__dict__["_last_name"] = surname

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    @My_logger.my_logging_decorator
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
        alter_date = False
        if hasattr(self, '_birth_date'):
            alter_date = True
        self._birth_date = '-'.join([year, mounth, day])
        return namedtuple("_", "alter_flag name")(alter_date,'birth_date')


    @property
    def phone(self):
        return self._phone

    @phone.setter
    @My_logger.my_logging_decorator
    def phone(self, phone):
        if not isinstance(phone, str):
            raise TypeError(f"Неправильный тип данных поля phone {type(phone)} is not str")
        if re.search("[\+7|8]?([\(| |\-]?[\d]{3}[\)| |\-]?){2}([\-| ]?[\d]{2}[\-| ]?){2}", phone) is None:
            raise ValueError(f"Неправильный номер телефона {phone}")
        phone = ''.join(filter(str.isdigit, phone))
        if len(phone) < 11:
            phone = '7' + phone
        phone = f'+7-{phone[1:4]}-{phone[4:7]}-{phone[7:9]}-{phone[9:11]}'
        alter_phone = False
        if hasattr(self, '_phone'):
            alter_phone = True
        self._phone = phone
        return namedtuple("_", "alter_flag name")(alter_phone, 'phone')

    @property
    def document_type(self):
        return self._document_type

    @document_type.setter
    @My_logger.my_logging_decorator
    def document_type(self, document):
        if not isinstance(document, str):
            raise TypeError(f"Неправильный тип данных поля document_type {type(document)} is not str")
        document = document.lower()
        if document not in {"паспорт", "заграничный паспорт", "водительские права"}:
            raise ValueError(f"Неправильный тип документов {document}")
        alter_doc_type = False
        if hasattr(self, '_document_type'):
            alter_doc_type = True
        self._document_type = document
        return namedtuple("_", "alter_flag name")(alter_doc_type, 'document_type')


    @property
    def document_id(self):
        return self._document_id

    @document_id.setter
    @My_logger.my_logging_decorator
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
        alter_doc_id = False
        if hasattr(self, '_document_id'):
            alter_doc_id = True
        self._document_id = doc_number
        return namedtuple("_", "alter_flag name")(alter_doc_id, 'document_id')



    @staticmethod
    def create(*args):
        return Patient(*args)

    @My_logger.db_decorator
    def save(self, db_name='patients'):
        data = [self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id]
        try:
            conn = sqlite3.connect("Covid.db")
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO patients VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')""".format(*data))
            conn.commit()
        finally:
            cursor.close()
            conn.close()


class Iterator:
    """Итератор для прохождения по коллекции"""

    def __init__(self, db_name, limit=None):
        self.limit = limit
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.id = 1

    def __iter__(self):
        return self

    def __next__(self):
        line = self.cursor.execute(f'SELECT * FROM patients where rowid={self.id}')
        line = line.fetchone()
        if line is None:
            raise StopIteration
        if (self.limit is not None) and self.limit == 0:
            raise StopIteration
        if self.limit is not None:
            self.limit -= 1
        self.id += 1
        return Patient(*list(line))

    def __del__(self):
        self.cursor.close()
        self.conn.close()


class PatientCollection:

    def __init__(self, db_name='Covid.db'):
        self.db_name = db_name
        self.data = self.read_patients_from_db(self.db_name)

    def __getitem__(self, key):
        return self.data[key]


    def __iter__(self):
        return Iterator(self.db_name)

    def limit(self, limit=None):
        return Iterator(self.db_name, limit)

    @My_logger.db_decorator
    def read_patients_from_db(self, db_name):
        data = []
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            for p in cursor.execute("SELECT * FROM patients"):
                data.append(Patient(*list(p)))
        finally:
            cursor.close()
            conn.close()
        return tuple(data)
    