import scrapy,requests,urllib
from bs4 import BeautifulSoup
from lxml import html
from urllib import request,response
import time
import shelve
headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

#res=requests.get('https://cricbuzz.com/live-cricket-scores/22458/',allow_redirects=False) #cricbuzz is rejecting anonymous requests without headers and redirecting it to home page
#src=res.content
#htmlElem=html.document_fromstring(src)
#temp=htmlElem.cssselect("[class=cb-ovr-flo]")
#for i in temp:
    #print(i.text_content())

#print(src)
#print("end")
def bs():
    url='https://www.cricbuzz.com/live-cricket-scores/22460/'
    req = urllib.request.Request(url=url, headers=headers)
    html=urllib.request.urlopen(req)
    soup=BeautifulSoup(html,'html.parser')
    #print(soup.prettify())

    #class ="cb-col cb-col-67 cb-nws-lft-col cb-comm-pg"
    root=soup.find('div',{'class':'cb-col cb-col-100 cb-font-12 cb-text-gray cb-min-rcnt'})
    temp=soup.find('div',{'class':"cb-mat-mnu-wrp cb-ovr-num"})
    print("temp",list(temp))
    if '.6' in list(temp)[0]:
        print('_____________Over complete_______')
    #print('test: ',root)
    try:
        print("1:", list(root.span.next_sibling))
        data = list(root.span.next_sibling)[0].strip().replace("|", "").split(" ")
        print(len(data))
        print(data)
        print(data[len(data) - 2], data[len(data) - 1])
        print("Match complete!")
    #main=soup.find('div',{'ng-show':'!isCommentaryRendered'})
    #comm=main.find('div',{'class':'"cb-col cb-col-100"'})
    #comm=main.div
    #l=list(comm)
    #print(main)
    #print('--------------------------------')
    #print(comm)
    #print(l)
        if '6' in data[len(data)-1]:
            print(True)
        else:
            print(False)
    except Exception:
        print("Match Complete!")

bs()
# start=time.time()
# while True:
#     bs()

class Sw6(scrapy.Spider):
    name = "Swiggy6Notifier"
    urls=['https://cricbuzz.com/live-cricket-scores/22458']
