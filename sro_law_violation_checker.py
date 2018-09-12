import requests
import smtplib
import time
import datetime

from bs4 import BeautifulSoup

from config.config import GMAIL_USER, GMAIL_PASSWORD, RECIPIENTS


def get_page_violation_block_content():
    r = requests.get('http://nopriz.ru/ndocs/narusheniya_sro/')
    data = r.text
    # get page block:
    soup = BeautifulSoup(data, features="html.parser")
    dump = soup.find_all('div', {'class': 'info-name'})
    page_content = ''
    for d in dump:
        page_content += d.next_element.next_element.next_element + '\n'
        page_content += d.next_sibling.next_sibling.next_element.\
                        next_element.next_element.next_element.next_element \
                        + '\n'

    return page_content


def send_email(msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    server.sendmail(GMAIL_USER,
                    RECIPIENTS,
                    ('Subject: Оповещение о нарушениях в проектных СРО'
                    '\r\n%s' % msg).encode('utf-8'))
    server.quit()


if __name__ == '__main__':
    while 1:
        page_data = get_page_violation_block_content()
        print(f'sleeping from {datetime.datetime.now()}')
        time.sleep(3600)

        if page_data != get_page_violation_block_content():
            send_email(get_page_violation_block_content())
        else:
            continue
