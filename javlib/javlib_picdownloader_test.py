#!/usr/bin/python 
#-*- coding: utf-8 -*-
'''
Created on 2016年12月22日
@author: sugar
@see: a simple crawler for javlib to download pic-code.
'''
import urllib2,os,sys
from bs4 import BeautifulSoup
from Config import Config
import clipboard

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
    if total_page == 0:
        soup = list_soup[0]
        vid = soup.select_one('div.id').get_text()
        keyword = vid.split('-')[0]
        vid_url = 'http://www.javlibrary.com/cn/?v=%s'%soup['id'].replace('vid_','')
        vid_page = do_get(vid_url)
        vid_soup = BeautifulSoup(vid_page,'lxml')
        img_url = vid_soup.select_one('div#video_jacket img#video_jacket_img')['src']
        print img_url
        total_page = int(root_soup.select_one('div.page_selector a.page.last')['href'].split('page=')[-1])
        next_page = total_page
    else:
        list_soup.reverse()
        for soup in list_soup:
            vid = soup.select_one('div.id').get_text()
            keyword = vid.split('-')[0]
            if keyword.lower() == kw.lower():
                vid_url = 'http://www.javlibrary.com/cn/?v=%s'%soup['id'].replace('vid_','')
                vid_page = do_get(vid_url)
                vid_soup = BeautifulSoup(vid_page,'lxml')
                img_url = vid_soup.select_one('div#video_jacket img#video_jacket_img')['src']
                print img_url
                while True:
                    finish_input = raw_input('url-test finished, please input anything to exit and copy the url :-) ')
                    if finish_input or finish_input=='':
                        clipboard.copy(img_url)
                        osCommandString = 'D:/Notepad++/notepad++.exe roster.ini'
                        os.system(osCommandString)
                        sys.exit()
        next_page -= 1
    return data_dict_list,next_page,total_page
        
if __name__ == '__main__':
    # 定位当前路径
    cwd = os.path.dirname(sys.argv[0])
    os.chdir(cwd)
    crawl_configs = Config('./roster.ini')
    crawl_config_sections = crawl_configs.sections()
    for crawl_config_section in crawl_config_sections:
        cfg = crawl_configs.get(crawl_config_section)
        if cfg['mode'] == 'test':
            next_page = cfg['start']
            total_page = cfg['end']
            dir_path = cfg['dir']
            key_word = cfg['keyword']
            if isinstance(next_page, (str,unicode)):
                next_page = int(next_page) if next_page else 1
                total_page = int(total_page) if total_page else 0
                while next_page:
                    d_dict_list,next_page,total_page = get_prepic(kw=key_word,next_page=next_page,total_page=total_page)
            else:
                print '[error: incorrect page properties!]'
    print 'finish!'
        
    

    
    