import requests
import smtplib
import time
import datetime
import difflib

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


def check_difference_between_pages(old_page, new_page):
    diff = difflib.ndiff(old_page, new_page)
    changes = [l for l in diff if l.startswith('+ ')]

    if changes:
        raw_data = ''.join(changes)
        clean_data = raw_data.replace('+ ', '')
        return clean_data
    else:
        return False


def main():
    nopriz_data = get_page_data_nopriz()
    nostroy_data = get_page_data_nostroy()

    print(f'sleeping from {datetime.datetime.now()}')
    time.sleep(1800)

    nopriz_changes = check_difference_between_pages(nopriz_data,
                                                    get_page_data_nopriz())
    nostroy_changes = check_difference_between_pages(nostroy_data,
                                                     get_page_data_nostroy())

    if nopriz_changes:
        send_email(f'''Обнаружено обновление в http://nopriz.ru/ndocs/narusheniya_sro/' + {nopriz_changes}''')
    if nostroy_changes:
        send_email(f'''Обнаружено обновление в http://nostroy.ru/exluded-sro/' + {nostroy_changes}''')


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(600)
            continue
