import enum
from urllib import response
from numpy import extract
import requests #to make http requests
from bs4 import BeautifulSoup #for web scraping
import smtplib #send the email

from email.mime.multipart import MIMEMultipart #for email body
from email.mime.text import MIMEText #for email body
import datetime #system date and time manipulation
now = datetime.datetime.now() #to extract the current datatime i.e system datetime

content = "" #content placeholder

def extract_news(url):
    print("Extracting hacker news story...")
    cnt = ""
    cnt += ('<b>HN Top Stories:</b>\n'+'<br>'+50*'-'+'<br>')
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag  in enumerate(soup.find_all('td',attrs={'class':'title', 'valign':''})):
        cnt += ((str(i+1)+" :: "+tag.text+"\n"+"<br>") if tag.text!="More" else "")
    return(cnt)

cnt = extract_news("https://news.ycombinator.com/")
content += cnt
content += ('<br>--------<br>')
content += ('<br><br>End of Message')


# let's send the email

print("Composing email ...")

#update our email details
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = '************'
TO = '************'
PASS = '*************'

msg = MIMEMultipart()

msg['Subject'] = "Top News Stories [AUTOMATED EMAIL]" + ' ' + str(now.day) + "-" + str(now.date)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initializing Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print("Email Sent...")

server.quit()

