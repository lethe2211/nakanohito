#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import fetchurl
import filecache
from bs4 import BeautifulSoup, NavigableString
import codecs

class VoiceActorApiWrapper(object):
    
    def __init__(self):
        self.base_url = 'http://lain.gr.jp/voicedb/'

    def search(self, vid, mode='detail'):
        cache_client = filecache.Client(dir='cache/voicedb/search/')
        cache = cache_client.get(str(vid))
        if cache is not None:
            html = cache
        else:
            url = self.base_url + 'profile/' + str(vid)
            f = fetchurl.FetchUrl()
            response = f.get(url, sleep_time=1)
            html = response.content
        cache_client.set(str(vid), html)
        json = {'status': u'NG', 'type': unicode(mode), 'data': {'vid': unicode(vid)}} 
        if mode == 'detail':            
            # print response.encoding
            soup = BeautifulSoup(html, 'html.parser')
            # print soup.find('p', {'class': 'outline'}).contents
            json['data']['outline'] = soup.find('p', {'class': 'outline'}).get_text()
            for db in soup.find_all('div', {'id': 'db'}):
                dl = db.dl
                for e in dl.find_all('dt'):
                    dt = e.get_text().strip()
                    dd_tag = e.next_sibling
                    # FIXME: なぜか年齢と所属が取得できない
                    # 要素がNavigableStringの時だけ文字が消えるみたい
                    if dd_tag.__class__ == NavigableString:
                        dd = unicode(dd_tag.string)
                        # print repr(dd)
                    else:
                        dd = dd_tag.get_text().strip()
                    # TODO: 実際にレスポンスに入れたい情報を後で考える
                    if dt == u'名前':
                        json['data']['name'] = dd
                    elif dt == u'よみ':
                        json['data']['yomi'] = dd
                    elif dt == u'ローマ字':
                        json['data']['roman'] = dd
                    elif dt == u'年齢':
                        json['data']['age'] = dd
            json['status'] = 'OK'
            return json
        elif mode == 'cast':
            soup = BeautifulSoup(html, 'html.parser')
            json['data']['cast'] = []
            ul = soup.find('ul', {'class': 'cast-list'})
            if ul is None:
                json['status'] = 'OK'
                return json
            for li in ul.find_all('li'):
                # TODO: 作品のカテゴリ分類を後でやる
                logo_filename = li.h3.img['src'].split('/')[-1]
                if logo_filename == 'cate_1.png':
                    worktype = u'tv_anime'
                elif logo_filename == 'cate_2.png':
                    worktype = u'ova_anime'
                elif logo_filename == 'cate_3.png':
                    worktype = u'movie'
                else:
                    worktype = 'None'
                elem = {'wid': int(li.h3.a['href'].split('/')[-1]), 'workname': li.h3.a.string, 'role': li.div.string, 'worktype': worktype}
                json['data']['cast'].append(elem)
            json['status'] = 'OK'
            return json

    def name_to_id(self, name):
        url = self.base_url + 'search'
        params = {'q': name}
        f = fetchurl.FetchUrl()
        response = f.get(url, params=params, sleep_time=1)
        vid = int(response.url.split('/')[-1])
        return vid

    def get_id_list(self):
        json = {'status': u'NG', 'type': u'vid_list', 'data': {}}
        cache_client = filecache.Client(dir='cache/voicedb/vid_list/')
        cache = cache_client.get('vid_list')
        vids = []
        if cache is not None:
            vids = cache
        else:
            for i in range(1, 11):
                url = self.base_url + 'profile/list/cid/' + str(i)
                f = fetchurl.FetchUrl()
                response = f.get(url, sleep_time=1)
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')
                for ul in soup.find_all('ul', {'class': 'listItems'}):
                    for li in ul.find_all('li'):
                        vid = int(li.a['href'].split('/')[-1])
                        vids.append(vid)
            cache_client.set('vid_list', vids)
        json['data']['vid_list'] = sorted(vids)
        json['status'] = 'OK'
        return json

if __name__ == '__main__':
    # sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    vaw = VoiceActorApiWrapper()
    # print vaw.search_by_name(u'新谷良子')
    # print vaw.search(vaw.name_to_id(u'阿澄佳奈'), mode='cast')
    print vaw.get_id_list()
