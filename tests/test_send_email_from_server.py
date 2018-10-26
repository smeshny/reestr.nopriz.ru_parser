import sys
sys.path.append('../')  # for import config.config

import smtplib


from config.config import GMAIL_USER, GMAIL_PASSWORD, RECIPIENTS


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


if __name__ == '__main__':
    send_email('''Обнаружено обновление в
                   http://nopriz.ru/ndocs/narusheniya_sro/''')
