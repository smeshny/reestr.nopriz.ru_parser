import math

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker

from models import Companies, engine


Session = sessionmaker(bind=engine)
session = Session()


# http://reestr.nostroy.ru/clients/344
# 344 is short number
SRO_short_numbers_to_parse = [344, ]


# def get_companies_short_numbers(short_sro_number):
#     link_to_companies_list = \
#         'http://reestr.nostroy.ru/reestr/clients/' + str(short_sro_number) + \
#         '/members'
#     r = requests.get(link_to_companies_list)
#     data = r.text


def get_pages_count_to_parse(short_sro_number):
    link_to_companies_list = \
        'http://reestr.nostroy.ru/reestr/clients/' + str(short_sro_number) + \
        '/members'

    r = requests.get(link_to_companies_list)
    data = r.text

    soup = BeautifulSoup(data, features="html.parser")

    companies_count_raw = str(soup.find('div',
                                    {'class': 'tatal-count-wrapper'}).text)
    element_start = companies_count_raw.find('из ') + 3
    companies_count = int(companies_count_raw[element_start:])
    pages_count = math.ceil(companies_count/20)

    return pages_count


if __name__ == '__main__':
    print(get_pages_count_to_parse(344))