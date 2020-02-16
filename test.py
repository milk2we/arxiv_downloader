import requests
import time
import random
import json


class Client(object):
    def __init__(self, api_key, api_secret, redirect_uri, token=None,
                 username=None, password=None):
        # const define
        self.site = 'https://api.weibo.com/'
        self.authorization_url = self.site + 'oauth2/authorize'
        self.token_url = self.site + 'oauth2/access_token'
        self.api_url = self.site + '2/'

        # init basic info
        self.client_id = api_key
        self.client_secret = api_secret
        self.redirect_uri = redirect_uri

        self.session = requests.session()
        if username and password:
            self.session.auth = username, password

        # activate client directly if given token
        if token:
            self.set_token(token)

    @property
    def authorize_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        return "{0}?{1}".format(self.authorization_url, urlencode(params))

    @property
    def alive(self):
        if self.expires_at:
            return self.expires_at > time.time()
        else:
            return False

    def set_code(self, authorization_code):
        """
        Activate client by authorization_code.
        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri
        }
        res = requests.post(self.token_url, data=params)
        token = json.loads(res.text)
        self._assert_error(token)

        token[u'expires_at'] = int(time.time()) + int(token.pop(u'expires_in'))
        self.set_token(token)

    def set_token(self, token):
        """Directly activate client by access_token.
        """
        self.token = token

        self.uid = token['uid']
        self.access_token = token['access_token']
        self.expires_at = token['expires_at']

        self.session.params = {'access_token': self.access_token}

    def _assert_error(self, d):
        """Assert if json response is error.
        """
        if 'error_code' in d and 'error' in d:
            raise RuntimeError("{0} {1}".format(
                d.get("error_code", ""), d.get("error", "")))

    def get(self, uri, **kwargs):
        """Request resource by get method.
        """
        url = "{0}{1}.json".format(self.api_url, uri)

        # for username/password client auth
        if self.session.auth:
            kwargs['source'] = self.client_id

        res = json.loads(self.session.get(url, params=kwargs).text)
        self._assert_error(res)
        return res

    def post(self, uri, **kwargs):
        """Request resource by post method.
        """
        url = "{0}{1}.json".format(self.api_url, uri)

        # for username/password client auth
        if self.session.auth:
            kwargs['source'] = self.client_id

        if "pic" not in kwargs:
            res = json.loads(self.session.post(url, data=kwargs).text)
        else:
            files = {"pic": kwargs.pop("pic")}
            res = json.loads(self.session.post(url,
                                               data=kwargs,
                                               files=files).text)
        self._assert_error(res)
        return res


if __name__ == '__main__':



    this_time = time.localtime()
    API_KEY = '31978875'    #第二步得到的API_KEY
    API_SECRET = '1a4e0cd3d4569ba5be3e9d391f1e153a' #第二步得到的API_SECRET
    REDIRECT_URI = 'https://api.weibo.com/oauth2/default.html'
    weibo_zhanghao = '18340097805'  #开发者页面绑定的微博账号
    secret = 'fsy199708'  # 绑定的微博密码
    domain = '\nhttps://www.weibo.com/6115313139/' # 安全域名

    # 发送一条纯文字微博
    #WeiBo_Client = Client(API_KEY, API_SECRET, REDIRECT_URI, username=weibo_zhanghao, password=secret)
    #weibotext = 'This is a test for auto-robot'
    #weibocontent = weibotext + domain
    #WeiBo_Client.post('statuses/share', status=weibocontent)

     # 发送一条带图片微博
    WeiBo_Client = Client(API_KEY, API_SECRET, REDIRECT_URI, username=weibo_zhanghao, password=secret)
    weibotext = 'ok?'
    weibocontent = weibotext + domain
    picname = './ml.png' # 发送的图片文件名
    fp = open(picname, 'rb')
    WeiBo_Client.post('statuses/share', status=weibocontent, f=fp)
    fp.close() #关闭打开的图片

