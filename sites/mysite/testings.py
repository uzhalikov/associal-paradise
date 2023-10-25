import smtplib
from email.mime.text import MIMEText

def send_message(message, subject):
    login = 'omega.notifications@inbox.ru'
    password = 'bzrhpzzCVmESTnTJHGNs'

    server = smtplib.SMTP('smtp.mail.ru')
    server.starttls()
    print('Логинюсь!')
    server.login(login, password)
    msg = MIMEText(message)
    msg['Subject'] = subject
    print('Отправляю сообщение.')
    for i in range(1, 100):
        server.sendmail(from_addr=login, to_addrs=login, msg=f'{msg.as_string()}')
    print('Сообщение отправлено!')

message = 'Доброго времени суток!'
subject = 'Хочешь покушать уток?'


send_message(message=message, subject=subject)
