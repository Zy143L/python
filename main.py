import os
import json
import qrcode
import time
import pyperclip
import requests
import threading
requests.packages.urllib3.disable_warnings()
os.environ['no_proxy'] = '*'

jd_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 SP-engine/2.14.0 main/1.0 baiduboxapp/11.18.0.16 (Baidu; P2 13.3.1) NABar/0.0 TM/{0}'


def token_get():
    t = round(time.time())
    headers = {
        'User-Agent': jd_ua.format(t),
        'referer': 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    }
    t = round(time.time())
    url = 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    res = s.get(url=url, headers=headers, verify=False)
    res_json = json.loads(res.text)
    s_token = res_json['s_token']
    token_post(s_token)
    # return s_token


def token_post(s_token):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': jd_ua.format(t),
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?s_token={0}&v={1}&remember=true'.format(s_token, t)
    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
        }
    # print(jd_ua.format(t))
    res = s.post(url=url, headers=headers, data=data, verify=False)
    # print(res.text)
    res_json = json.loads(res.text)
    token = res_json['token']
    # print("token:", token)
    c = s.cookies.get_dict()
    okl_token = c['okl_token']
    # print("okl_token:", okl_token)
    t1 = threading.Thread(target=image_print, args=(token,))
    t2 = threading.Thread(target=check_token, args=(token, okl_token))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def check_token(token, okl_token):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': jd_ua.format(t),
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?&token={0}&ou_state=0&okl_token={1}'.format(token, okl_token)
    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action'.format(t),
        'source': 'wq_passport',
    }
    res = s.post(url=url, headers=headers, data=data, verify=False)
    check = json.loads(res.text)
    code = check['errcode']
    message = check['message']
    while code == 0:
        print("扫码成功")
        jd_ck = s.cookies.get_dict()
        pt_key = 'pt_key=' + jd_ck['pt_key']
        pt_pin = 'pt_pin=' + jd_ck['pt_pin']
        ck = str(pt_key) + ';' + str(pt_pin) + ';'
        print(ck)
        pyperclip.copy(ck)
        print("已复制到剪切板")
        break
    else:
<<<<<<< HEAD
        print(message)
        time.sleep(1)
        check_token(token, okl_token)
=======
        i = i + 1
        # print(i)
        if i < 120:
            print(message)
            time.sleep(1)
            check_token(token, okl_token)
        else:
            exit(0)
>>>>>>> 0c15127ae266524f4e52d518679d0bd93e3f9c32


def image_print(token):
    qrurl = 'https://plogin.m.jd.com/cgi-bin/m/tmauth?client_type=m&appid=300&token={0}'.format(token)
    print("如果系统未弹出二维码图片, 请手动生成二维码")
    print("URL地址已复制到剪切板, 请使用在线二维码生成")
    print()
    print(qrurl)
    print()
    pyperclip.copy(qrurl)
    try:
        img = qrcode.make(qrurl)
        img.show()
    except:
        print('二维码生成失败, 请手动在线生成')
        print(qrurl)


if __name__ == '__main__':
    os.system('chcp 65001')
    print("Ver: 1.3.1 By: limoe")
    print("https://github.com/Zy143L/jd_cookie")
    print("JD扫码获取Cookie")
    print("回车生成二维码")
    input()
    s = requests.session()
    token_get()
    os.system('pause')
