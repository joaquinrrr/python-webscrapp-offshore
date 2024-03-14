from requests_html import HTMLSession
from bs4 import BeautifulSoup

s = HTMLSession()
url = 'https://offshoreleaks.icij.org/search?q=china&c=&j=&d='

def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

print(getdata(url))