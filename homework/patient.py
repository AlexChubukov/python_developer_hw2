#from hw2.python_developer_hw2.homework import My_logger
from homework import My_logger
import re

class Patient:

    first_name = NotImplemented
    last_name = NotImplemented


    @My_logger.init_log
    def __init__(self, name, surname, birth_date, phone_number, doc_type, doc_number):
        self.good_log = My_logger.logging.getLogger("logger_access")
        self.bad_log = My_logger.logging.getLogger("logger_error")


        self._first_name = name
        self._last_name = surname
        self.birth_date = birth_date
        self.phone = phone_number
        self.document_type = doc_type
        self.document_id = doc_number

    #def __del__(self):
    #    self.handler_access.close()
    #    self.handler_error.close()
        #self.good_log.removeHandler(self.handler_access)
        #self.bad_log.removeHandler(self.handler_error)
        #del self.good_log
        #del self.bad_log

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
        return self.__first_name

    @first_name.setter
    @My_logger.log
    def first_name(self, name):
        raise AttributeError("Нельзя изменять значения поля first_name")


    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    @My_logger.log
    def last_name(self, name):
        raise AttributeError("Нельзя изменять значения поля last_name")


    @property
    def _first_name(self):
        return self.__first_name

    @_first_name.setter
    def _first_name(self, name):
        if not isinstance(name, str):
            raise TypeError("Неправильный тип данных поля first_name")
        if name.isalpha() != True:
            raise ValueError("Name must contain only characters")
        self.__first_name = name

    @property
    def _last_name(self):
        return self.__last_name

    @_last_name.setter
    def _last_name(self, surname):
        if not isinstance(surname, str):
            raise TypeError("Неправильный тип данных поля last_name")
        if surname.isalpha() != True:
            raise ValueError("Surname must contain only characters")
        self.__last_name = surname

    @property
    def birth_date(self):
        return self.__birth_date

    @birth_date.setter
    @My_logger.log
    def birth_date(self, date):
        if not isinstance(date, str):
            raise TypeError("Неправильный тип данных поля birth_date")
        format1 = re.search("^(\d{2}[\-|\.| ]?){2}\d{4}$", date) is not None
        format2 = re.search("^\d{4}[\-|\.| ]?\d{2}[\-|\.| ]\d{2}$", date) is not None
        if not (format1 or format2):
            raise ValueError("Неправильная дата рождения")
        day, mounth, year = '', '', ''
        if format1:
            day, mounth, year = date[0:2], date[3:5], date[6:]
            assert (2020 - int(year)) < 150, "Неправильная дата рождения"
        else:
            year, mounth, day = date[0:4], date[5:7], date[8:]
            assert (2020 - int(year)) < 150, "Неправильная дата рождения"
        try:
            self.birth_date
            self.good_log.info(f"Изменение поля birth_date объекта {self}")
            self.__birth_date = '-'.join([year, mounth, day])
        except AttributeError:
            self.__birth_date = '-'.join([year, mounth, day])


    @property
    def phone(self):
        return self.__phone

    @phone.setter
    @My_logger.log
    def phone(self, phone):
        if not isinstance(phone, str):
            raise TypeError("Неправильный тип данных поля phone")
        if re.search("[\+7|8]?([\(| |\-]?[\d]{3}[\)| |\-]?){2}([\-| ]?[\d]{2}[\-| ]?){2}", phone) is None:
            raise ValueError("Неправильный номер телефона")
        phone = ''.join(filter(str.isdigit, phone))
        if len(phone) < 11:
            phone = '7' + phone
        phone = f'+7-{phone[1:4]}-{phone[4:7]}-{phone[7:9]}-{phone[9:11]}'
        try:
            self.phone
            self.good_log.info(f"Изменение поля phone объекта {self}")
            self.__phone = phone
        except AttributeError:
            self.__phone = phone

    @property
    def document_type(self):
        return self.__document_type

    @document_type.setter
    @My_logger.log
    def document_type(self, document):
        if not isinstance(document, str):
            raise TypeError("Неправильный тип данных поля document_type")
        document = document.lower()
        if document not in {"паспорт", "заграничный паспорт", "водительские права"}:
            raise ValueError("Неправильный тип документов")
        try:
            self.document_type
            self.good_log.info(f"Изменение поля document_type объекта {self}")
            self.__document_type = document
        except AttributeError:
            self.__document_type = document


    @property
    def document_id(self):
        return self.__document_id

    @document_id.setter
    @My_logger.log
    def document_id(self, doc_number):
        if not isinstance(doc_number, str):
            raise TypeError("Неправильный тип данных поля document_id")
        if self.document_type == "паспорт":
            if re.search("^([\d][ |\-|\-|\/]?){10}$", doc_number) is None:
                raise ValueError("Неправильный номер паспорта")
            doc_number = ''.join(filter(str.isdigit, doc_number))
            doc_number = doc_number[:4] + " " + doc_number[4:]
        if self.document_type == "заграничный паспорт":
            if re.search("^([\d][ |\-|\-|\/]?){9}$", doc_number) is None:
                raise ValueError("Неправильный номер заграничного паспорта")
            doc_number = ''.join(filter(str.isdigit, doc_number))
            doc_number = doc_number[:2] + " " + doc_number[2:]
        if self.document_type == "водительские права":
            if re.search("^([\d][ |\-|\-|\/]?){10}$", doc_number) is None:
                raise ValueError("Неправильный номер прав")
            doc_number = ''.join(filter(str.isdigit, doc_number))
            doc_number = doc_number[:2] + " " + doc_number[2:4] + " " + doc_number[4:]
        try:
            self.document_id
            self.good_log.info(f"Изменение поля document_id объекта {self}")
            self.__document_id = doc_number
        except AttributeError:
            self.__document_id = doc_number


    @classmethod
    def create(cls, name, surname, birth_date, phone_number, doc_type, doc_number):
        return cls(name, surname, birth_date, phone_number, doc_type, doc_number)

    def save(self, filename="Patients.csv"):
        data = [self._first_name, self._last_name, self.birth_date, self.phone, self.document_type, self.document_id]
        data = ','.join(data)
        data += '\n'
        try:
            with open(filename, 'a') as file:
                file.write(data)
            self.good_log.info(f"Пациент {self} записан в файл")
        except Exception as err:
            self.bad_log.error(f"Ошибка записи в файл: {err}")


class Iterator:
    """Итератор для прохождения по коллекции"""

    def __init__(self, collection, filename, limit=None):
        self.collection = collection
        self.limit = limit
        self.file = open(filename, 'r')

    def __iter__(self):
        return self

    def __next__(self):
        try:
            line = self.file.readline()
            line = line.rstrip('\n')
            assert line is not ""
            if self.limit is not None:
                assert self.limit != 0
                self.limit -= 1
            return Patient(*line.split(','))
        except AssertionError:
            raise StopIteration


    def __del__(self):
        self.file.close()


class PatientCollection:

    def __init__(self, filename='Patients.csv'):
        self.good_log = My_logger.logging.getLogger("logger_access")
        self.bad_log = My_logger.logging.getLogger("logger_error")
        self.filename = filename
        self.data = self.read_patients_from_file(filename)

    def __getitem__(self, key):
        return self.data[key]


    def __iter__(self):
        return Iterator(self.data, self.filename)

    def limit(self, limit=None):
        return Iterator(self.data,self.filename, limit)


    @staticmethod
    def read_patients_from_file(filename):
        data = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    p = Patient.Patient(*line.split(','))
                    data.append(p)
        except Exception:
            self.bad_log.error(f"Ошибка чтения пациентов из файла {filename}")
        finally:
            return tuple(data)
