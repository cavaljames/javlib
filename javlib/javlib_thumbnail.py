#!/usr/bin/python 
#-*- coding: utf-8 -*-
'''
Created on 2016年12月22日
@author: sugar
@see: a simple crawler for javlib to download pic-code.
'''
import urllib2,urllib,os,sys
from bs4 import BeautifulSoup
from Config import Config

def do_get(url): 
    get_headers = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    } 
    req = urllib2.Request(url,headers=get_headers)  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    try:
        d = opener.open(req ,timeout=50).read()
    except:
        return None
    return d

def get_prepic(kw='aaa',next_page=1,total_page=0):
    # deal with url
    base_url = 'http://www.javlibrary.com/cn/vl_searchbyid.php?&keyword=%s&page=%d'%(kw,next_page)
    # get datas
    data_dict_list = []
    page = do_get(base_url)
    root_soup = BeautifulSoup(page,'lxml')
    list_soup = root_soup.select('div.videothumblist div.videos div.video')
    for soup in list_soup:
        vid = soup.select_one('div.id').get_text()
        img_url = soup.select_one('img')['src']
        if vid and img_url:
            data_dict = dict()
            data_dict['vid'] = vid
            data_dict['img_url'] = img_url
            data_dict_list.append(data_dict)
    # deal with total_page and next_page
    if total_page == 0:
        total_page = int(root_soup.select_one('div.page_selector a.page.last')['href'].split('page=')[-1])
    next_page += 1
    if next_page > total_page:
        next_page = 0
    return data_dict_list,next_page,total_page
    
def download_pic_list(download_path, key_word, current_page, vid_imgurl_list):
    rdp = '%s/%s'%(download_path,key_word)
    if not os.path.isdir(rdp):
        os.makedirs(rdp)
    for vid_imgurl in vid_imgurl_list:
        vid = vid_imgurl['vid']
        img_url = vid_imgurl['img_url']
        suffix = img_url.split('.')[-1]
        d_path = '%s/%d_%s.%s' % (rdp,current_page,vid,suffix)
        if not os.path.exists(d_path):
            print 'downloading %s ...'%vid
            urllib.urlretrieve(img_url, d_path)
        
if __name__ == '__main__':
    # 定位当前路径
    cwd = os.path.dirname(sys.argv[0])
    os.chdir(cwd)
    crawl_configs = Config('./roster.ini')
    crawl_config_sections = crawl_configs.sections()
    for crawl_config_section in crawl_config_sections:
        cfg = crawl_configs.get(crawl_config_section)
        if cfg['mode'] == 'search':
            next_page = cfg['start']
            total_page = cfg['end']
            dir_path = cfg['dir']
            key_word = cfg['keyword']
            if isinstance(next_page, (str,unicode)):
                next_page = int(next_page) if next_page else 1
                total_page = int(total_page) if total_page else 0
                while next_page:
                    current_page = next_page
                    d_dict_list,next_page,total_page = get_prepic(kw=key_word,next_page=next_page,total_page=total_page)
                    download_pic_list(dir_path,key_word,current_page,d_dict_list)
            elif isinstance(next_page, list):
                for p in next_page:
                    p = int(p) if p else 1
                    current_page = p
                    d_dict_list,_,__ = get_prepic(kw=key_word,next_page=p,total_page=(p+1))
                    download_pic_list(dir_path,key_word,current_page,d_dict_list)
            else:
                print '[error: incorrect page properties!]'
    print 'finish!'
    while True:
        finish_input = raw_input('please input anything to exit: ')
        if finish_input or finish_input=='':
            sys.exit()
        
    

    
    