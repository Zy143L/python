import os
import json
import qrcode
import time
import pyperclip
import requests
requests.packages.urllib3.disable_warnings()
os.environ['no_proxy'] = '*'


def token_get():
    t = round(time.time())
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'referer': 'https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?s_token={0}&v={1}&remember=true'.format(s_token, t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?s_token={0}&v={1}&remember=true'.format(s_token, t)
    data = 'lang=chs&appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    res = s.post(url=url, headers=headers, data=data, verify=False)
    # print(res.text)
    res_json = json.loads(res.text)
    token = res_json['token']
    # print("token:", token)
    image_print(token)
    c = s.cookies.get_dict()
    okl_token = c['okl_token']
    # print("okl_token:", okl_token)
    while True:
        zt = check_token(token, okl_token)
        time.sleep(1)
        if zt == 0:
            break

def check_token(token, okl_token):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'referer': 'https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?&token={0}&ou_state=0&okl_token={1}'.format(token, okl_token),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?&token={0}&ou_state=0&okl_token={1}'.format(token, okl_token)
    data = 'lang=chs&appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    res = s.post(url=url, headers=headers, data=data, verify=False)
    check = json.loads(res.text)
    code = check['errcode']
    message = check['message']
    if code == 0:
        print("扫码成功")
        jd_ck = s.cookies.get_dict()
        pt_key = 'pt_key=' + jd_ck['pt_key']
        pt_pin = 'pt_pin=' + jd_ck['pt_pin']
        ck = str(pt_key) + ';' + str(pt_pin) + ';'
        print("JDCookie: ", ck)
        pyperclip.copy(ck)
        print("已复制到剪切板")
        return 0
    else:
        print(message)
        return 1


def image_print(token):
    qrurl = 'https://plogin.m.jd.com/cgi-bin/m/tmauth?client_type=m&appid=300&token={0}'.format(token)
    print("如果系统未弹出二维码图片, 请手动生成二维码")
    print("URL地址已复制到剪切板, 请使用在线二维码生成")
    print(qrurl)
    pyperclip.copy(qrurl)
    img = qrcode.make(qrurl)
    img.show()


if __name__ == '__main__':
    print("Ver: 0.2 By: limoe")
    print("https://github.com/Zy143L/jd_cookie")
    print("JD扫码获取Cookie本地版")
    print("手机与电脑请在同一网络下!")
    print("回车生成二维码")
    input()
    s = requests.session()
    token_get()
    input()