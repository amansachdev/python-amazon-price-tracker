#!/usr/bin/pythongh
# -*- coding: utf-8 -*-
#commit
import os
import re
import json
import time
import requests
import smtplib
import argparse
import urllib.parse
import datetime,random
import UserAgent
import telegram
import sys
import proxies
from scraper_api import ScraperAPIClient
from proxies import random_proxy
from copy import copy
from lxml import html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, datetime, timedelta
client = ScraperAPIClient('b66f202cc1b0e68243a7d91bbfe81674') 
#iplist = ['162.208.48.84:8118','165.138.4.41:8080']
#proxies = {'https':random.choice(iplist) }
#print(proxies)

ua = UserAgent.UserAgent()
#imported_proxy = random_proxy.random_proxies()
#print(imported_proxy)
intervalTimeBetweenCheck = 0
dateIndex = datetime.now()
emailinfo = {}

IFTTT_Key = ""
IFTTT_EventName = ""



# msg_content format
# msg_content['Subject'] = 'Subject'
# msg_content['Content'] = 'This is a content'
def isbotalive():
    botToken = "1458960461:AAGNsxDSNl-begwUquQu1NgkilJ_hc5szA0"
    chatId = "-1001388198553"
    bot = telegram.Bot(botToken)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    bot.send_message(chat_id=chatId, text="hello there i am still working for you and time is \n"+ current_time)

def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

def send_Notification(msg_content):
    global send_Mode
    if send_Mode == 1:
        send_email(msg_content)
    elif send_Mode == 2:
        IFTTT_alert(msg_content)
    elif send_Mode == 3:
        telegram_alert(msg_content)

def telegram_alert(msg_content):
    global botToken
    global chatId

    # 1 is success
    # 2 is server working msg
    # 3 is server shutdown
    if msg_content['code'] == 1:
        message = "BIS Rs." + str(msg_content['Price']) + "\n" + "\n" + msg_content['Product'] + "\n" + "\n" + msg_content['URL'] +"??tag=nishchal-21"

    elif msg_content['code'] == 2:
        message = '🔴' + msg_content['Content']

    elif msg_content['code'] == 3:
        message = msg_content['Content']

    bot.send_message(chat_id=chatId, text=message)
    print("Mesage posted to telegram:",chatId)

def IFTTT_alert(msg_content):
    global IFTTT_EventName
    global IFTTT_Key

    requestBody = {}

    # 1 is success
    # 2 is server working msg
    # 3 is server shutdown
    if msg_content['code'] == 1:
        requestBody["value1"] = msg_content['Product']
        requestBody["value2"] = msg_content['Price']
        requestBody["value3"] = msg_content['URL']

    elif msg_content['code'] == 2:
        requestBody["value1"] = msg_content['Content']

    elif msg_content['code'] == 3:
        requestBody["value1"] = msg_content['Content']

    url = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (IFTTT_EventName,IFTTT_Key)
    requests.post(url, data=requestBody) 
    print("IFTTT post success  ",url)

def send_email(msg_content):
    global emailinfo

    try:
        # Try to login smtp server
        s = smtplib.SMTP("smtp.gmail.com:587")
        s.ehlo()
        s.starttls()
        s.login(emailinfo['sender'], emailinfo['sender-password'])
    except smtplib.SMTPAuthenticationError:
        # Log in failed
        print(smtplib.SMTPAuthenticationError)
        print('[Mail]\tFailed to login')
    else:
        # Log in successfully
        print('[Mail]\tLogged in! Composing message..')

        for receiver in emailinfo['receivers']:

            msg = MIMEMultipart('alternative')
            msg['Subject'] = msg_content['Subject']
            msg['From'] = emailinfo['sender']
            msg['To'] = receiver
            
            text = msg_content['Content']

            part = MIMEText(text, 'plain')
            msg.attach(part)
            s.sendmail(emailinfo['sender'], receiver, msg.as_string())
            print(('[Mail]\tMessage has been sent to %s.' % (receiver)))

# send notified mail once a day.
def checkDayAndSendMail():
    todayDate = datetime.now()
    start = datetime(todayDate.year, todayDate.month, todayDate.day)
    end = start + timedelta(days=1)
    global dateIndex

    # if change date
    if dateIndex < end :
        dateIndex = end
        # send mail notifying server still working
        msg_content = {}
        msg_content['Subject'] = '[Amazon Price Alert] Server working !'
        msg_content['Content'] = 'Amazon Price Alert still working until %s !' % (todayDate.strftime('%Y-%m-%d %H:%M:%S'))
        msg_content['Price'] = ""
        msg_content['Time'] = todayDate.strftime('%Y-%m-%d %H:%M:%S')
        msg_content['ServerState'] = "Working"
        msg_content['code'] = 2 # 2 is server state
        #send_Notification(msg_content)




def get_price(url, selector):
    
    # set random user agent prevent banning
    try :
        #imported_proxy = random_proxy.random_proxies()
        #print("proxy used was")
        #print(imported_proxy)
        r = client.get(url, headers={
        'User-Agent':random_line('user-agents.txt')
            ,
        'Accept-Language':    'zh-tw',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Encoding':'gzip, deflate'
    })

        r.raise_for_status()
        #isbotalive()
        tree = html.fromstring(r.text)
	# find product name
        productName = ""
        productName_results = tree.xpath(selector['productname'])
        #print(proxies)
        if not productName_results:
        # raise Exception("Product Name does not exist")
            print('Didn\'t find the \'product-name\' element, trying again later...')
        else :
            productName = productName_results[0].text
            productName = productName.strip()
    except :
        print("BANNED")
        try :
        #imported_proxy = random_proxy.random_proxies()
        #print("proxy used was")
        #print(imported_proxy)
            r = client.get(url, headers={
        'User-Agent':random_line('user-agents.txt')
            ,
        'Accept-Language':    'zh-tw',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Encoding':'gzip, deflate'
            })

            r.raise_for_status()
            #isbotalive()
            tree = html.fromstring(r.text)
	# find product name
            productName = ""
            productName_results = tree.xpath(selector['productname'])
        #print(proxies)
            if not productName_results:
        # raise Exception("Product Name does not exist")
                print('Didn\'t find the \'product-name\' element, trying again later...')
            else :
                productName = productName_results[0].text
                productName = productName.strip()
        except :
            print("BANNED 2")
            try :
        #imported_proxy = random_proxy.random_proxies()
        #print("proxy used was")
        #print(imported_proxy)
                r = client.get(url, headers={
        'User-Agent':random_line('user-agents.txt')
            ,
        'Accept-Language':    'zh-tw',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Encoding':'gzip, deflate'
            })

                r.raise_for_status()
                #isbotalive()
                tree = html.fromstring(r.text)
	# find product name
                productName = ""
                productName_results = tree.xpath(selector['productname'])
        #print(proxies)
                if not productName_results:
        # raise Exception("Product Name does not exist")
                    print('Didn\'t find the \'product-name\' element, trying again later...')
                else :
                    productName = productName_results[0].text
                    productName = productName.strip()
            except :
        	    print("BANNED 3")



    # find Price
    try:
        # extract the price from the string
        print(productName)
        price_string = re.findall('\d+.\d+', tree.xpath(selector['price'])[0].text)[0]
        return float(price_string.replace(',', '')),productName
    
    except:
        print('Didn\'t find the \'price\' element, trying again later...')
        botToken = "1458960461:AAGNsxDSNl-begwUquQu1NgkilJ_hc5szA0"
        chatId = "-1001388198553"
        bot = telegram.Bot(botToken)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        bot.send_message(chat_id=chatId, text="I Am Tracking\n" + productName +'\n'+current_time)

        
        # be banned, send mail then shut down
        # send mail notifying server shutdown
        msg_content = {}
        msg_content['Subject'] = '[Amazon Price Alert] Server be banned !'
        msg_content['Content'] = 'Amazon Price Alert be banned at %s !' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        msg_content['Price'] = ""
        msg_content['Time'] = ""
        msg_content['ServerState'] = "Banned"
        msg_content['code'] = 3 # 3 is server shutdown
        #send_Notification(msg_content)
        return 0,productName




# read config json from path
def get_config(config):
    with open(config, 'r') as f:
        # handle '// ' to json string
        input_str = re.sub(r'// .*\n', '\n', f.read())
        return json.loads(input_str)

# add some arguments 
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        default='%s/config.json' % os.path.dirname(os.path.realpath(__file__)),
                        help='Add your config.json path')
    parser.add_argument('-t', '--poll-interval', type=int, default=780,
                        help='Time(second) between checking, default is 780 s.')

    return parser.parse_args()

def main():
    #set up arguments
    args = parse_args()
    intervalTimeBetweenCheck = args.poll_interval
    global dateIndex
    global emailinfo
    global IFTTT_Key,IFTTT_EventName,send_Mode
    global botToken, chatId
    global bot 

    
    dateIndex = datetime.now()

    # get config from path
    config = get_config(args.config)
    emailinfo = config['email']
    intervalTimeBetweenCheck = config['default-internal-time']
    send_Mode = config['send_Mode']
    IFTTT_Key = config['IFTTT']['key']
    IFTTT_EventName = config['IFTTT']['eventName']
    botToken = config['Telegram']['botToken']
    chatId = config['Telegram']['chatId']

    #initialize telegram bot
    if send_Mode == 3:
        bot = telegram.Bot(botToken)

    #get all items to parse
    items = config['item-to-parse']

    while True and len(items):
        nowtime = datetime.now()
        nowtime_Str = nowtime.strftime('%Y-%m-%d %H:%M:%S')
        print(('[%s] Start Checking' % (nowtime_Str)))

        # send mail notify system working everyday
        checkDayAndSendMail()

        itemIndex = 1
        for item in copy(items):
            # url to parse
            item_page_url = urllib.parse.urljoin(config['amazon-base_url'], item[0])
            print(('[#%02d] Checking price for %s (target price: %s)' % ( itemIndex, item[2], item[1])))

            # get price and product name
            productName = item[2]
            price,productName = get_price(item_page_url, config['xpath_selector'])
            
            
            # Check price lower then you expected
            if not price:
                continue
            elif price <= item[1]:
                print(('[#%02d] %s\'s price is %s!! Trying to send email.' % (itemIndex,productName,price)))
                msg_content = {}
                msg_content['Subject'] = '[Amazon] %s Price Alert - %s' % (productName,price)
                msg_content['Content'] = '[%s]\nThe price is currently %s !!\nURL to salepage: %s' % (nowtime_Str, price, item_page_url)
                msg_content['Price'] = price
                msg_content['URL'] = item_page_url
                msg_content['Product'] = productName
                msg_content['ServerState'] = ""
                msg_content['code'] = 1 # 2 is server state
                send_Notification(msg_content)
                #items.remove(item)
            else:
                print(('[#%02d] %s\'s price is %s. Ignoring...' % (itemIndex,productName,price)))
                botToken = "1458960461:AAGNsxDSNl-begwUquQu1NgkilJ_hc5szA0"
                chatId = "-1001497022075"
                bot = telegram.Bot(botToken)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                bot.send_message(chat_id=chatId, text="Price May have Increased\n" + productName + '\n' + str(price) + '\n'+current_time)
            itemIndex += 1


        if len(items):
            # time interval add some random number for preventing banning
            nowtime = datetime.now()
            thisIntervalTime = intervalTimeBetweenCheck + random.randint(0,30)

            #calculate next triggered time
            dt = datetime.now() + timedelta(seconds=thisIntervalTime)
            print(('Sleeping for %d seconds, next time start at %s\n' % (thisIntervalTime, dt.strftime('%Y-%m-%d %H:%M:%S'))))
            time.sleep(thisIntervalTime)
        else:
            break


if __name__ == '__main__':
    main()
