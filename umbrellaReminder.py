#! /usr/bin/env python3
# umbrellaReminder.py - Checks weather for rain and sends a text reminder if it will.

from twilio.rest import Client
import requests, bs4, re

accountSID = input("Enter your Account SID: ")
authToken  = input("Enter your Authorization Token: ")
myNumber = input("Enter the receiving number: ")
twilioNumber = input("Enter your Twilio Number: ")

def textmyself(message):
    twilioCli = Client(accountSID, authToken)
    twilioCli.messages.create(body=message, from_=twilioNumber, to=myNumber)
    
def checkRain():
    res = requests.get('http://www.meteocentrum.cz/predpoved-pocasi/cz/6250/praha')
    res.raise_for_status()
    weatherSoup = bs4.BeautifulSoup(res.text, 'lxml')
    elems = weatherSoup.select('."day-time" span[class="ico ico--drops"]')
    regex = re.compile(r'\d+')
    rain = False
    for i in range(len(elems)):
        mo = regex.search(elems[i].getText()).group()
        if int(mo) > 30:
            rain = True
            break
    if rain == True:
        print('Texting', myNumber)
        textmyself('Bring an umbrella today!')
    '''
    else:
        print('Texting', myNumber)
        textmyself('Don\'t bring an umbrella today!')
    '''
checkRain()
