#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import filecache
from voice_actor_api_wrapper import VoiceActorApiWrapper
from set_similarity import SetSimilarity

class RelevanceBetweenVoiceActors(object):

    def __init__(self):
        pass

    @classmethod
    def calculate(self, vid1, vid2):
        vaaw = VoiceActorApiWrapper()
        cache_client = filecache.Client(dir='cache/voicedb/search/works/')
        works_va1 = []
        works_va2 = []
        cache1 = cache_client.get(str(vid1))
        if cache1 is not None:
            works_va1 = cache1
        else:
            vaaw_va1 = vaaw.search(vid1, mode='cast')
            works_va1 = [int(e['wid']) for e in vaaw_va1['data']['cast']]
            cache_client.set(str(vid1), works_va1)
        cache2 = cache_client.get(str(vid2))
        if cache2 is not None:
            works_va2 = cache2
        else:
            vaaw_va2 = vaaw.search(vid2, mode='cast')
            works_va2 = [int(e['wid']) for e in vaaw_va2['data']['cast']]
            cache_client.set(str(vid2), works_va2)
        return SetSimilarity.jaccard_similarity(set(works_va1), set(works_va2))

if __name__ == '__main__':
    rbva = RelevanceBetweenVoiceActors()
    print rbva.calculate(1040, 2193)
    