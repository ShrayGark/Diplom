import requests
import re


class Finder:
    # Базовый класс для поиска подстрок на основе re
    def __init__(self):
        self.input_data = None
        self.output_data = []

    def set_data(self, data):
        self.input_data = data
        self.output_data = []

    def find_email(self):
        pattern = re.compile(r'\b\w+@\w+\.\w+\b')  # email pattern
        res = pattern.findall(self.input_data)
        res = list(set(res))
        return res

    def find_phone(self):
        pattern = re.compile(r'\+?[78][ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}')  # number pattern
        res = pattern.findall(self.input_data)
        return res

    def find_fullname(self):
        pattern = re.compile(r'[А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+')  # fio pattern
        res = pattern.findall(self.input_data)
        return res

    def find_references(self, str_pattern):
        pattern = re.compile(str_pattern)
        res = pattern.findall(self.input_data)
        return res

    def get_info(self):
        return self.output_data

    def find_info(self):
        emails = self.find_email()
        numbers = self.find_phone()
        fullnames = self.find_fullname()

        maximum = max(len(emails), len(numbers), len(fullnames))
        for i in range(maximum):
            if len(emails) < maximum:
                emails.append('-')
            if len(numbers) < maximum:
                numbers.append('-')
            if len(fullnames) < maximum:
                fullnames.append('-')

        for fullname, email, number in zip(fullnames, emails, numbers):
            self.output_data.append((fullname, email, number))


class BaseParser:
    #
    def __init__(self):
        self.melon_site = ''

    def set_url(self, url):
        self.melon_site = url

    def send_request(self, url=''):
        with requests.Session() as session:
            session.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
            }
            if url:
                return session.get(url)
            else:
                return session.get(self.melon_site)

    def prepare_data(self, data):
        src = data.content
        # при возникновении ошибки необходима смена кодировки на cp1251
        return src.decode('utf8')

    def start_parse(self, finder, options):
        if options:
            result_array = []
            for i in range(options[0], options[1]):
                # print(i)
                iter_url = f'{self.melon_site}{i}'
                result_array.extend(
                    finder(str(
                        self.prepare_data(
                            self.send_request(iter_url)
                        )
                    )
                )
                )
            return result_array
        return finder(self.prepare_data(self.send_request()))