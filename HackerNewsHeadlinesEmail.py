from email.mime.nonmultipart import MIMENonMultipart
import requests                 #http requests
from bs4 import BeautifulSoup   #web scraping

#Send he mail
import smtplib

#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#system data and time manipulation
import datetime
now = datetime.datetime.now()   #email subject line with appropriate date, when it was sent

#email content placeholder
content = ''   

#Extracting Hacker News stories
def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content      #Different object from the global content on line 16
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')
        #print(tag.prettify)    #find all('span', attrs={'class':'sitestr'}))
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content +=('<br><br>End of Message')

#Let's send the email
print('Composing Email...')

#Update your email details
SERVER = 'smtp.gmail.com'           #"your smtp server"
PORT = 587                          #Your port number
FROM = ''   #"Your from/sending email id"
TO = ''        #"Your recieving/to email ids"    #Can be a list
PASS = ''         #"Your from/sending email id's password"


#fp = open(file_name, 'rb')
#Create a text/plain message
#msg = MIMEText('')
msg = MIMEMultipart()

#msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
#fp.close()

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()









































