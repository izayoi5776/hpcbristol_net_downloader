# coding: UTF-8
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import time

# top level
def level0(url):
  print("level0 url=" + url)
  soup = url2soup(url)
  urls = []
  for tag in soup.select('li[aria-level="1"] a'):
    urls.append(a2url(tag, url))
  return urls

# parse level1 page and all next pages, return urls
def level1(url):
  print("lvel1 url=" + url)
  soup = url2soup(url)
  urls = []
  for tag in soup.select('h3.node__h1 a'):
    urls.append(a2url(tag, url))
  for tag in soup.select('li.pager-next a'):
    urls.extend(level1(a2url(tag, url)))
  return urls

# get full url from soup tag a
def a2url(a, url):
  return urllib.request.urljoin(url, a.get('href'))

# read url parse to soup
def url2soup(url):
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")
  return soup

# ------------------- MAIN -----------------
# top URL
url = "https://www.hpcbristol.net/collections"
url1 = "https://www.hpcbristol.net/collections/carstairs-jamie"
url2 = "https://www.hpcbristol.net/visual/jc-s014"

lst = level0(url)

path = './urls.txt'
with open(path, mode='w') as f:
  n = len(lst)
  for i in range(n):
    u = lst[i]
    print(str(i) + "/" + str(n) + " " + u)
    lst1 = level1(u)
    f.writelines('\n'.join(lst1))
    f.write('\n')
    f.flush()
    #time.sleep(1)
