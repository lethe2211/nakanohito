#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from voice_actor_api_wrapper import VoiceActorApiWrapper
from set_similarity import SetSimilarity

class RelevanceBetweenVoiceActors(object):

    def __init__(self):
        pass

    @classmethod
    def calculate(self, vid1, vid2):
        vaaw = VoiceActorApiWrapper()
        vaaw_va1 = vaaw.search(vid1, mode='cast')
        vaaw_va2 = vaaw.search(vid2, mode='cast')
        # print vaw_va1
        # print vaw_va2
        works_va1 = [int(e['wid']) for e in vaaw_va1['data']['cast']]
        works_va2 = [int(e['wid']) for e in vaaw_va2['data']['cast']]
        return SetSimilarity.jaccard_similarity(set(works_va1), set(works_va2))

if __name__ == '__main__':
    rbva = RelevanceBetweenVoiceActors()
    print rbva.calculate(1040, 2193)
    