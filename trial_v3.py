# Python program For Birthday Reminder Application
import re
import time
from datetime import datetime, date, timedelta
import csv
import os
import smtplib
import sys

from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Setting environment variables:
load_dotenv()
USR = os.getenv('USR')
PSW = os.getenv('PSW')


def checkBirthdaysInAWeek(filePath):
    fileName = open(filePath, 'r')
    today = datetime.now().date().strftime('%m-%d')
    csvreader = csv.reader(fileName)
    next(csvreader)

    today = datetime.now().date()
    birthday_in_a_week = (today + timedelta(days=7)).strftime('%m-%d')
    print(birthday_in_a_week)
    print(time.strftime('%m-%d'))
    list_of_birthdays_in_a_week = []
    list_to_sent = []
    for item in csvreader:

        try:
            parsed_date, fmt = try_parsing_date(item[2])
            if fmt is None:
                print({'Error': "Invalid date"})
            # elif valid_date(item[2], fmt) == True:
            elif not is_date_in_past(item[2], fmt):
                print({'Error': "Date is in the future"})
            elif not is_not_empty_name(item[0]):
                print({'Error': 'Empty name field'})
            elif not is_valid_email(item[1]):
                print({'Error': 'Invalid email'})
            else:
                if parsed_date and parsed_date.strftime('%m-%d') == birthday_in_a_week:
                    # print(parsed_date.strftime('%m-%d') == birthday_in_a_week)
                    # print(parsed_date.strftime('%m-%d'))
                    # print((today + timedelta(days=7)).strftime('%m-%d'))
                    birthday_name = item[0]
                    d1 = parsed_date.strptime(item[2], '%Y-%m-%d')
                    print(d1.year, d1.month, d1.day)
                    print(type(birthday_in_a_week))
                    d2 = date(d1.year, d1.month, d1.day)
                    print(d2)
                    # date = datetime.strptime(birthday_in_a_week, '%m-%d')
                    # print(d2)
                    print(today.year, today.month, today.day)
                    # birthday_date = time.strftime('%m-%d')
                    # print('hi')
                    # print(birthday_date)
                    # days_until_birthday = birthday_date - now
                    # print(days_until_birthday)
                    # print(birthday_calculation_before_a_week(item[2]))
                    print(f'{birthday_name} will have birthday in a week')
                    list_of_birthdays_in_a_week.append(item)
                    list_of_birthdays_in_a_week.append(birthday_in_a_week)
                    days_left = calculate_time_left(list_of_birthdays_in_a_week)
                    list_of_birthdays_in_a_week.append(days_left)
                else:
                    list_to_sent.append(item)

        except Exception as error:
            print(item, error)

    print(list_of_birthdays_in_a_week)
    print(list_to_sent)
    print(calculate_time_left(list_of_birthdays_in_a_week))
    multiple_email_sends(list_of_birthdays_in_a_week, list_to_sent)
    return list_of_birthdays_in_a_week, list_to_sent


def calculate_time_left(birthdays_list):

    d0 = datetime.strptime(birthdays_list[1], '%m-%d')
    d1 = datetime.now().date()
    d2 = date(d1.year, d1.month, d1.day)
    d3 = date(d1.year, d0.month, d0.day)
    delta = d3 - d2
    if delta.days <= 7:
        return delta.days
    else:
        print("Not any birthdays expected wthin a week") # Sitas nereikalingas nes niekada nebus call'inamas


def multiple_email_sends(birthday_individual, to_sent):
    for bday in birthday_individual:
        print(bday)
        for item in to_sent:
            send_email(item[0],bday[0],6,6,item[1])


def try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%m-%d'):
        try:
            return datetime.strptime(text, fmt), fmt
        except ValueError:
            pass
    return {'error': 'Wrong format'}, None


def is_date_in_past(date, format):
    now = datetime.now().date()
    isPast = True
    if format == '%Y-%m-%d':
        if datetime.strptime(date, format).date() < now:
            print("Date is valid.")
            isPast = True
        else:
            isPast = False
    return isPast


def is_not_empty_name(name):
    if name == '':
        return False
    return True


def is_valid_email(email):
    regex = '^[a-zA-Z0-9]+[\._]?[ a-zA-Z0-9]+[@]\w+[. ]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    else:
        return False

def send_email(name,birthday_name,date,days_left,to_email):
    msg = MIMEMultipart()
    msg['From'] = USR
    msg['To'] = to_email
    msg['Subject'] = f'Birthday Reminder: {birthday_name}\'s birthday on {date}\'s'
    message = f'Hi {name}, This is a reminder that {birthday_name}\'s will be celebrating their birthday on {date}\'s. There are {days_left}s left to get a present!'
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(USR, PSW)

    mailserver.sendmail(USR,'aurimas.nausedas@gmail.com',msg.as_string())

    mailserver.quit()


if __name__ == '__main__':
    checkBirthdaysInAWeek(sys.argv[1])
    # i = '06-27'
    # # print(datetime.now().date().strftime('%m-%d'))
    # # seven_days = datetime.now().date()-timedelta(days=7)
    # # print(seven_days)
    # # print(datetime.strptime(seven_days, '%Y %m %d'))
    # d0 = datetime.strptime(i, '%m-%d')
    # d1 = datetime.now().date()
    # d2 = date(d1.year, d1.month, d1.day)
    # d3 = date(d1.year, d0.month, d0.day)
    # delta = d3 - d2
    # print(delta.days)