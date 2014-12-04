#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import csv
import itertools
from multiprocessing import Process
from voice_actor_api_wrapper import VoiceActorApiWrapper
from relevance_between_voice_actors import RelevanceBetweenVoiceActors

class VoiceActorCrawler(object):

    def __init__(self):
        self.vaaw = VoiceActorApiWrapper()
        self.rbva = RelevanceBetweenVoiceActors()

    def crawl(self):
        vids = self.vaaw.get_id_list()['data']['vid_list']
        
        min_relevance = float('inf')
        result = {}

        for vid1, vid2 in list(itertools.combinations(vids, 2)):
            row = self.get_relevance(vid1, vid2)
            if len(result) < 100:
                result[(vid1, vid2)] = row
                if min_relevance > row[2]:
                    min_relevance = row[2]
                # min_relevance = min(e[2] for e in result.values())
            else:
                if min_relevance < row[2]:
                    result[(vid1, vid2)] = row
                    for (v1, v2), (name1, name2, relevance) in result.items():
                        if relevance == min_relevance:
                            print 'Poped', result[(v1, v2)][0], result[(v1, v2)][1], result[(v1, v2)][2]
                            result.pop((v1, v2))
                            break
                    else:
                        print 'okashii'
                    min_relevance = min(e[2] for e in result.values())
            if (vid1, vid2) in result:
                print 'Added', result[(vid1, vid2)][0], result[(vid1, vid2)][1], result[(vid1, vid2)][2]
            else:
                print 'Not added', row[0], row[1], row[2]
        result = sorted(result.items(), cmp=lambda x, y: cmp(y[1][2], x[1][2]))
        print result
        with open('relevance.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for elem in result:
                row = [elem[0][0], elem[0][1], elem[1][0].encode('utf-8'), elem[1][1].encode('utf-8'), elem[1][2]]
                writer.writerow(row)



        # vids_combination = list(itertools.combinations(vids, 2))
        # vids_combination_divided = [vids_combination[i:i+len(vids_combination)/4] for i in range(0, len(vids_combination), len(vids_combination)/4)]
        # jobs = [Process(target=self.get_relevances, args=(vcd,)) for vcd in vids_combination_divided]
        # for j in jobs:
        #     j.start()
        # for j in jobs:
        #     j.join()
        # self.result = sorted(self.result.items(), cmp=lambda x, y: cmp(y[1][2], x[1][2]))
        # return self.result
        # for vid1, vid2 in it:
        #     jobs = []
        #     if len(jobs) == 5:
        #         for j in jobs:
        #             j.start()
        #         jobs = []
        #     else:
        #         jobs.append()


        # jobs = [Process(target=self.get_relevance, args=(vid1, vid2,)) for vid1, vid2 in itertools.combinations(vids, 2)]
        # print jobs
        # for j in jobs:
        #     j.start()
        # for j in jobs:
        #     j.join()
        #     # time.sleep(1)
        # self.result = sorted(self.result.items(), cmp=lambda x, y: cmp(y[1][2], x[1][2]))
        # return self.result

    # def get_relevances(self, comb):
    #     for vid1, vid2 in comb:
    #         self.get_relevance(vid1, vid2)

    def get_relevance(self, vid1, vid2):
        return [self.vaaw.search(vid1)['data']['name'], self.vaaw.search(vid2)['data']['name'], self.rbva.calculate(vid1, vid2)]
        # print self.vaaw.search(vid1)['data']['name'], self.vaaw.search(vid2)['data']['name'], self.rbva.calculate(vid1, vid2)
        # self.result[(vid1, vid2)] = (self.vaaw.search(vid1)['data']['name'], self.vaaw.search(vid2)['data']['name'], self.rbva.calculate(vid1, vid2))


if __name__ == '__main__':
    vac = VoiceActorCrawler()
    vac.crawl()
