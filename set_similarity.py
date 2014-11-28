#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

class SetSimilarity(object):
    '''
    集合間の類似度を計算するクラス
    '''
    def __init__(self):
        pass

    @classmethod
    def jaccard_similarity(cls, a, b):
        '''
        2つの集合に対して，ジャカード係数を計算する
        '''
        if a | b == 0:
            return None
        else:
            return len(a & b) * 1.0 / len(a | b)

if __name__ == '__main__':
    print SetSimilarity.jaccard_similarity({'a', 'b', 'c'}, {'b', 'c', 'd', 'e'})
