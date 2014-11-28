#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import itertools
from voice_actor_api_wrapper import VoiceActorApiWrapper
from relevance_between_voice_actors import RelevanceBetweenVoiceActors

class VoiceActorCrawler(object):

    def __init__(self):
        self.vaaw = VoiceActorApiWrapper()
        self.rbva = RelevanceBetweenVoiceActors()

    def crawl(self):
        result = []
        vids = self.vaaw.get_id_list()['data']['vid_list']
        for vid1, vid2 in itertools.combinations(vids, 2):
            res = (vid1, self.vaaw.search(vid1)['data']['name'], vid2, self.vaaw.search(vid2)['data']['name'], self.rbva.calculate(vid1, vid2))
            print res
            result.append(res)
            time.sleep(1)
        result.sort(cmp=lambda x, y: cmp(y[4], x[4]))
        return result

if __name__ == '__main__':
    vac = VoiceActorCrawler()
    vac.crawl()
