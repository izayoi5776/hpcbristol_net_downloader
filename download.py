# coding: UTF-8
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import time
import json
import os
from multiprocessing import Pool

# get full url from soup tag a
def a2url(a, url):
  return urllib.request.urljoin(url, a.get('href'))

# read url parse to soup
def url2soup(url):
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")
  return soup

# download level2 html as dict
def getlevel2dict(id, url):
  ret = {'z_id':id, 'z_baseurl':url}
  soup = url2soup(url)
  # tags
  for tag in soup.select('div.field__label'):
    tagname = tag.get_text()
    tagtext = list(map(lambda x: x.get_text(), tag.parent.select('div.field__item')))
    ret.update({tagname:tagtext})
  # get title
  for tag in soup.select('h1.page-title span.text'):
    ret.update({'title':tag.get_text()})
  # download link
  for tag in soup.select('div.field__download li a'):
    ret.update({'z_download_url':a2url(tag,url)})
  return ret

# check if level2 json, jpg exists
def chkfiles(fjson, fjpg):
  return os.path.isfile(fjson) and os.path.exists(fjpg)

# return id, json filename, jpg filename, create folder if need
def getFileNames(url):
  path1 = "json"
  path2 = "jpg"
  createDirSafe(path1)
  createDirSafe(path2)
  id= url.split('/')[-1]
  fjson = path1 + "/" + id + ".json"
  fjpg  = path2 + "/" + id + ".jpg"
  return [id, fjson, fjpg]

# create folder if need
def createDirSafe(path):
  if not os.path.isdir(path):
    os.makedirs(path)

# level 2 main
def level2(url):
  url = url.replace('\n', '')
  [id, fjson, fjpg] = getFileNames(url)
  if(chkfiles(fjson, fjpg)):
    print("skip " + url)
  else:
    print("downloading " + url)
    d = getlevel2dict(id, url)
    # save json
    with open(fjson, mode='w') as f:
      json.dump(d, f, indent=2)
    # download jpg only if not exists
    if(not os.path.exists(fjpg)):
      urllib.request.urlretrieve(d['z_download_url'], fjpg)

# ------------------- MAIN -----------------
url2 = "https://www.hpcbristol.net/visual/jc-s014"
url3 = "https://www.hpcbristol.net/visual/yo-s19"
url4 = "https://www.hpcbristol.net/download/image/28574"
url5 = "https://www.hpcbristol.net/visual/bo01-077" # caption on mount
url6 = "https://www.hpcbristol.net/visual/hv23-001" # no captions

path = './urls.txt'
with open(path, mode='r') as f:
  urls = f.readlines()

with Pool(5) as p:
  p.map(level2, urls)

