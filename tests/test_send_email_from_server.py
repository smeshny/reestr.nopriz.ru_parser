import smtplib


from config.config import GMAIL_USER, GMAIL_PASSWORD, RECIPIENTS


def send_email(msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    server.sendmail(GMAIL_USER,
                    RECIPIENTS,
                    ('Subject: Тестовое сообщение\r\n%s' % msg).encode('utf-8'))
    server.quit()


if __name__ == '__main__':
    send_email('Проверка отправки почты с сервера')