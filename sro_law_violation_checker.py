import requests
import smtplib
import time
import datetime

from bs4 import BeautifulSoup

from config.config import GMAIL_USER, GMAIL_PASSWORD, RECIPIENTS


def get_page_data_nopriz():
    r = requests.get('http://nopriz.ru/ndocs/narusheniya_sro/')
    data = r.text

    soup = BeautifulSoup(data, features="html.parser")
    dump = soup.find_all('div', {'class': 'info-name'})
    page_content = ''
    for d in dump:
        page_content += d.next_element.next_element.next_element + '\n'
        page_content += d.next_sibling.next_sibling.next_element.\
                        next_element.next_element.next_element.next_element \
                        + '\n'

    return page_content


def get_page_data_nostroy():
    r = requests.get('http://nostroy.ru/exluded-sro/')
    data = r.text

    soup = BeautifulSoup(data, features="html.parser")
    dump = soup.find('section', {'class': 'content'})

    return dump.text


def send_email(msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    server.sendmail(GMAIL_USER,
                    RECIPIENTS,
                    ('Subject: Оповещение о нарушениях в СРО'
                    '\r\n%s' % msg).encode('utf-8'))
    server.quit()


def main():
    nopriz_data = get_page_data_nopriz()
    nostroy_data = get_page_data_nostroy()

    print(f'sleeping from {datetime.datetime.now()}')
    time.sleep(3600)

    if nopriz_data != get_page_data_nopriz():
        send_email('Обнаружено обновление в '
                   'http://nopriz.ru/ndocs/narusheniya_sro/')
    if nostroy_data != get_page_data_nostroy():
        send_email('Обнаружено обновление в '
                   'http://nostroy.ru/exluded-sro/')


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(600)
            continue
