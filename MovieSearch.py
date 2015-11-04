#!/usr/bin/env python
#coding=utf-8

from MovieEngines import GaoqingMp4, Dytt

movieEngines = [GaoqingMp4, Dytt, ]

def movieSearch(keyword):
    searchResult = []
    for engine in movieEngines:
        engine = engine()
        engine.search(keyword)
        searchResult.append(engine)
    return searchResult
