#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
from voice_actor_api_wrapper import VoiceActorApiWrapper

class RankRelevanceBetweenVoiceActors(object):
    
    def __init__(self):
        self.vaw = VoiceActorApiWrapper()

    def rank(self):
        data = np.load('jaccard_reduce_at_50_works_series.npy')
        d = data.flatten()      # 1次元配列に変換(必要？)
        rank = d.argsort()[::-1][:100] # データを降順に並べた際の上位100件のデータのインデックス
        for r in rank:
            vid1 = r / data.shape[0]
            vid2 = r % data.shape[1]
            name1 = self.vaw.search(vid1)['data']['name']
            name2 = self.vaw.search(vid2)['data']['name']
            cast1 = self.vaw.search(vid1, mode='cast')['data']['cast']
            cast2 = self.vaw.search(vid2, mode='cast')['data']['cast']
            cast_overlap = set(e['wid'] for e in cast1) & set(e['wid'] for e in cast2)
            workname_overlap = [e['workname'] for e in cast1 if e['wid'] in cast_overlap]
            
            print vid1, name1, vid2, name2, ', '.join(workname_overlap)
        
        return None

if __name__ == '__main__':
    rrbva = RankRelevanceBetweenVoiceActors()
    rrbva.rank()
