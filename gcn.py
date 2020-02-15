import urllib.request
import requests

f  = open('./url.txt')
lines = f.readlines()
for line in lines:

    url = 'http://xxx.itp.ac.cn/pdf/'+line.strip()+'.pdf'
    print(url)
    data = urllib.request.urlopen(url).read()
    f = open('./gcn/'+line.strip()+'.pdf', 'wb')
    f.write(data)
    f.close()






