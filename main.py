import scrapy
from bs4 import BeautifulSoup
from urllib import request
import shelve
#using shelve, we store load id into a variable and override the value of id on disk (with 1 increment) only once in the whole run and

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

