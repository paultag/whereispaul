# Copyright (c) Paul Tagliamonte

import urllib
import urllib2

import whereispaul.settings

def get_opener():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', whereispaul.settings.USER_AGENT)]
    return opener

opener = get_opener()

def post(url, data={}):
    data = urllib.urlencode(data)
    return opener.open(url, data)

def get(url, data=None):
    data = urllib.urlencode(data)
    url += "?" + data
    return opener.open(url)
