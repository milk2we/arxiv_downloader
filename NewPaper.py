# encoding: utf-8
# Author    : damionfan@163.com
# Datetime  : 2020/2/15 20:50
# User      : Damion Fan
# Product   : PyCharm
# Project   : arxiv
# File      : NewPaper.py
# explain   : 参考代码地 http://gwang-cv.github.io/2016/04/01/Python%E7%88%AC%E5%8F%96arxiv%E7%9A%84paper/

from urllib import request
from translate import Translator

import http.client
import hashlib
import urllib
import random
import json

from  bs4 import BeautifulSoup
from lxml import etree
import time
import re
from multiprocessing.dummy import Pool

def getHtml(url):
    content = request.urlopen(url).read()
    return content.decode('utf-8')

def getContent(content):
    soup = BeautifulSoup(content, 'lxml')
    urls = soup.find_all(name='span', attrs={'class': 'list-identifier'})
    links = []
    for url in urls:
        link = url.find_all(name='a', href=True)
        links.append(link[0]['href'])

    return links



'''
appKey = '0caaa17749afe877'
secretKey = 'E8RlvPAy8P3EUPM0sycgTYssKzCvfB9l'


def youdaoTranslate(q):
    httpClient = None
    myurl = '/api'
    fromLang = 'EN'
    toLang = 'zh-CHS'
    salt = random.randint(1, 65536)
    sign = appKey + q + str(salt) + secretKey
    m1 = hashlib.new('md5')
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl + '?appKey=' + appKey + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('openapi.youdao.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        s = eval(response.read().decode("utf-8"))['translation']
        #print(s)
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
    return s
'''


appid = '20200216000384575'  # 填写你的appid
secretKey = 'Oy5hM_wZHyS4fDpY3SRw'  # 填写你的密钥
def Baidutranslation(text):
    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'auto'   #原文语种
    toLang = 'zh'   #译文语种
    salt = random.randint(32768, 65536)
    # q= 'Knowledge distillation introduced in the deep learning context is a method to transfer knowledge from one architecture to another. In particular, when the architectures are identical, this is called self-distillation. The idea is to feed in predictions of the trained model as new target values for retraining (and iterate this loop possibly a few times). It has been empirically observed that the self-distilled model often achieves higher accuracy on held out data. Why this happens, however, has been a mystery: the self-distillation dynamics does not receive any new information about the task and solely evolves by looping over training. To the best of our knowledge, there is no rigorous understanding of why this happens. This work provides the first theoretical analysis of self-distillation. We focus on fitting a nonlinear function to training data, where the model space is Hilbert space and fitting is subject to L2 regularization in this function space. We show that self-distillation iterations modify regularization by progressively limiting the number of basis functions that can be used to represent the solution. This implies (as we also verify empirically) that while a few rounds of self-distillation may reduce over-fitting, further rounds may lead to under-fitting and thus worse performance'
    q = text
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        res = result['trans_result'][0]['dst']

    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()
    return res

def translation(text):
    '''
   lines = text.split('. ')
    res = ""
    for line in lines:
        result = translation(line)
        res += result

    '''
    res = Baidutranslation(text)
    return res

def getInformation(base_url, href):
    content = getHtml(base_url+href)
    soup = BeautifulSoup(content, 'lxml')
    title = soup.find_all(name='h1',attrs={'class':'title mathjax'})
    title = title[0].get_text().split('\n')[1]
    zh_title = translation(title)

    authors = soup.find_all(name='div', attrs={'class': 'authors'})
    authors = authors[0].get_text().split('\n')
    string = ""
    for author in range(1,len(authors)):
        string += authors[author]
    authors = string

    abstract = soup.find_all(name='blockquote', attrs={'class': 'abstract mathjax'})
    abstract = abstract[0].get_text().replace('\n',' ')

    #print(abstract)
    #print(translation(abstract))
    zh_abstract = translation(abstract)

    meta = soup.find_all(name='td', attrs={'class': 'tablecell comments'})
    comment = ''
    if len(meta) > 0:
        comment = meta[0].get_text()


    # print(title,authors,abstract,comment,zh_title,zh_abstract)
    return title,authors,abstract,comment,zh_title,zh_abstract


def getTotal(url):
    #url = 'http://xxx.itp.ac.cn/list/cs.LG/pastweek'
    #u = 'http://xxx.itp.ac.cn/list/cs.LG/pastweek?show=618'
    #print(url)
    content = getHtml(url)
    soup = BeautifulSoup(content, 'lxml')
    h3 = soup.find_all(name='h3')
    #print(h3)
    #print(h3[0].get_text())

    all = h3[0].get_text()
    total = all.split(' ')[8]
    #print(total)
    return total

def process_html(base_url, flag):
    total = getTotal(base_url + '/list/' + flag + '/pastweek')
    page = getHtml(base_url + '/list/' + flag + '/pastweek?show=' + total)
    links = getContent(page)

    for link in links:
        title,authors,abstract,comment,zh_title,zh_abstract = getInformation(base_url, link)
        print(title)
        print(authors)
        print(abstract)
        print(comment)
        print(zh_title)
        print(zh_abstract)
        arxiv_id = re.sub(r'(/)|([a-zA-Z])','',link)
        download_url = base_url+'/pdf/'+arxiv_id
        print(arxiv_id)
        print(download_url)


if __name__ == '__main__':
    base_url = 'http://xxx.itp.ac.cn/'

    keyword = ['cs','cs.lg','cs.cv','cs.dc','cs.lg','cs.cl']

    process_html(base_url,keyword[1])

