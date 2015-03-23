#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import numpy as np
# import itertools
# from multiprocessing import Process
from voice_actor_api_wrapper import VoiceActorApiWrapper
from relevance_between_voice_actors import RelevanceBetweenVoiceActors

class VoiceActorCrawler(object):

    def __init__(self):
        self.vaaw = VoiceActorApiWrapper()
        self.rbva = RelevanceBetweenVoiceActors()

    def crawl(self):
        vids = set(self.vaaw.get_id_list()['data']['vid_list'])

        a = np.array([[-1.0 for j in xrange(4200)] for i in xrange(4200)])

        for i in xrange(4200):
            for j in xrange(4200):
                if i in vids and j in vids and i < j:
                    a[i][j] = self.get_relevance(i, j)
                    print i, j, a[i][j]
        np.save('jaccard_reduce_at_50_works_series', a)

    def get_relevance(self, vid1, vid2):
        return self.rbva.calculate(vid1, vid2)
        # print self.vaaw.search(vid1)['data']['name'], self.vaaw.search(vid2)['data']['name'], self.rbva.calculate(vid1, vid2)
        # self.result[(vid1, vid2)] = (self.vaaw.search(vid1)['data']['name'], self.vaaw.search(vid2)['data']['name'], self.rbva.calculate(vid1, vid2))


if __name__ == '__main__':
    vac = VoiceActorCrawler()
    vac.crawl()
