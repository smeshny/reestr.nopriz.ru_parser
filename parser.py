import math
import re
import datetime

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import exists

from models import Companies, engine


Session = sessionmaker(bind=engine)
session = Session()


# http://reestr.nostroy.ru/clients/344
# 344 is short number
SRO_short_numbers_to_parse = [344, ]


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
    pages_count = int(math.ceil(companies_count/20))

    return pages_count


def get_companies_short_links(short_sro_number):
    pages_count = get_pages_count_to_parse(short_sro_number)

    for page in range(1, pages_count + 1):
        link_to_companies_page = 'http://reestr.nopriz.ru/reestr/clients/' \
                                  + str(short_sro_number) + \
                                 '/members?sort=m.registryRegistrationDate&' \
                                 'direction=desc&page=' \
                                  + str(page)
        r = requests.get(link_to_companies_page)
        data = r.text

        soup = BeautifulSoup(data, features="html.parser")
        companies_on_page = soup.findAll('a', {'href': re.compile(
                                         '/reestr/clients/'
                                         + str(short_sro_number)
                                         + '/members/')})

        for company in companies_on_page:
            full_link = 'http://reestr.nopriz.ru' + str(company.get('href'))

            # check that company in database:
            c_exists = session.query(
                   exists().where(Companies.company_link == full_link)).scalar()
            if c_exists:
                continue
            else:
            # Create new database object
                c = Companies(company_name='null',
                              company_inn='null',
                              company_manager='null',
                              company_address='null',
                              company_tel='null',
                              company_link=full_link,
                              sro_belongs='null',
                              member_status='null',
                              updated_at=datetime.datetime.now())
                session.add(c)
        session.commit()


def parse_company_card(link):
    r = requests.get(link)
    data = r.text

    soup = BeautifulSoup(data, features="html.parser")
    ###
    company_name = soup.find('td', text='Сокращенное наименование:')
    company_name = company_name.next_sibling.next_element.next_element
    ###
    company_inn = soup.find('td', text='ИНН:')
    company_inn = company_inn.next_sibling.next_element.next_element
    ###
    company_manager = soup.find('td', text='ФИО, осуществляющего функции '
                                           'единоличного исполнительного '
                                           'органа юридического лица и (или) '
                                           'руководителя коллегиального '
                                           'исполнительного органа '
                                           'юридического лица:')
    company_manager = company_manager.next_sibling.next_element.next_element
    ###
    company_address = soup.find(string=re.compile("Адрес местонахождения "
                                                  "юридического лица:"))
    company_address = company_address.next_element.next_element.next_element
    ###
    company_tel = soup.find('td', text='Номер контактного телефона:')
    company_tel = company_tel.next_sibling.next_element.next_element
    ###
    sro_belongs = soup.find(string=re.compile("СРО:"))
    sro_belongs = sro_belongs.next_element.next_element.next_element
    sro_belongs = sro_belongs.rstrip().lstrip().rstrip()
    ###
    member_status = soup.find('td', text='Статус члена:')
    member_status = member_status.next_sibling.next_element.next_element
    member_status = member_status.lstrip().rstrip()

    return {'company_name': company_name,
            'company_inn': company_inn,
            'company_manager': company_manager,
            'company_address': company_address,
            'company_tel': company_tel,
            'sro_belongs': sro_belongs,
            'member_status': member_status, }


if __name__ == '__main__':
    # print(get_companies_short_links(344))
    print(parse_company_card('http://reestr.nopriz.ru/reestr/clients/344/members/6179466'))