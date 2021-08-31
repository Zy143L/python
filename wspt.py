import requests
import json
import os
import pyperclip

requests.packages.urllib3.disable_warnings()
os.environ['no_proxy'] = '*'


def getToken(ws):
    headers = {
        'cookie': ws,
        'User-Agent': 'okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1440x3007;os/11;network/wifi;',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'charset': 'UTF-8',
        'accept-encoding': 'br,gzip,deflate'
    }
    params = {
        'functionId': 'genToken',
        'clientVersion': '10.1.2',
        'client': 'android',
        'lang': 'zh_CN',
        'uuid': '09d53a5653402b1f',
        'st': '1630392618706',
        'sign': '53904736db53eebc01ca70036e7187d6',
        'sv': '120'
    }
    # url = 'https://api.m.jd.com/client.action?functionId=genToken&clientVersion=10.1.2&client=android&lang=zh_CN&uuid=09d53a5653402b1f&st=1630392618706&sign=53904736db53eebc01ca70036e7187d6&sv=120'
    url = 'https://api.m.jd.com/client.action'
    data = 'body=%7B%22action%22%3A%22to%22%2C%22to%22%3A%22https%253A%252F%252Fplogin.m.jd.com%252Fcgi-bin%252Fm%252Fthirdapp_auth_page%253Ftoken%253DAAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg%2526client_type%253Dandroid%2526appid%253D879%2526appup_type%253D1%22%7D&'
    res = requests.post(url=url, params=params, headers=headers, data=data, verify=False)
    # print(res.text)
    res_json = json.loads(res.text)
    totokenKey = res_json['tokenKey']
    # print("Token:", totokenKey)
    appjmp(totokenKey)


def appjmp(token):
    headers = {
        'User-Agent': 'jdapp;android;10.1.2;11;0393465333165363-5333430323261366;network/wifi;model/M2102K1C;addressid/938507929;aid/09d53a5653402b1f;oaid/2acbcab5bb3f0e68;osVer/30;appBuild/89743;partner/lc023;eufv/1;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045714 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    }
    params = {
        'tokenKey': token,
        'to': 'https://plogin.m.jd.com/cgi-bin/m/thirdapp_auth_page?token=AAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg',
        'client_type': 'android',
        'appid': 879,
        'appup_type': 1,
    }
    # url = 'https://un.m.jd.com/cgi-bin/app/appjmp?tokenKey={0}&to=https%3A%2F%2Fplogin.m.jd.com%2Fcgi-bin%2Fm%2Fthirdapp_auth_page%3Ftoken%3DAAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg%26client_type%3Dandroid%26appid%3D879%26appup_type%3D1'.format(token)
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp'
    # print(url)
    # res = requests.get(url=url, headers=headers, verify=False, allow_redirects=False)
    res = requests.get(url=url, headers=headers, params=params, verify=False, allow_redirects=False)
    # print(res.headers)
    # print(res.status_code)
    res_set = res.cookies.get_dict()
    pt_key = 'pt_key=' + res_set['pt_key']
    pt_pin = 'pt_pin=' + res_set['pt_pin']
    ck = str(pt_key) + ';' + str(pt_pin) + ';'
    print(ck)
    pyperclip.copy(ck)
    print("已复制到剪切板")
    # print(res.text)


if __name__ == '__main__':
    os.system('chcp 65001')
    print("Ver: 0.1")
    print("limoe")
    print("请输入格式为pin=xxx;wskey=xxx;")
    ws = input()
    getToken(ws)
    os.system('pause')
