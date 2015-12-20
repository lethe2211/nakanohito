#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import fetchurl

class LainCrawler(object):
    
    def __init__(self):
        self.base_url = 'http://lain.gr.jp/voicedb/'

    def crawl(self):
        for i in xrange(1, 4192):
            filename = self.base_url + 'profile/' + str(vid) + '.html'
            page_content = self.getProfilePage(i)
            self.writeToFile(filename, page_content)
    
    def getProfilePage(vid):
        url = self.base_url + 'profile/' + str(vid)
        f = fetchurl.FetchUrl()
        response = f.get(url, sleep_time=1)
        return response.content

    def writeToFile(filename, content):
        with open(filename, 'w') as f:
            f.write(content)

if __name__ == '__main__':
    m = LainCrawler()
    m.crawl()
