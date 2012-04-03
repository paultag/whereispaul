# Copyright (c) Paul Tagliamonte

import sys
import json
import urllib
import urllib2

from whereispaul.db import Database
from whereispaul.util import get, post

import whereispaul.settings as settings
import whereispaul.errors

class GoogleService:
    def prime(self, service_name, api_version):
        self.service_name = service_name
        self.api_version  = api_version
        self.db           = Database("cache.%s.json" % ( service_name ))
        try:
            self.ensure()
        except urllib2.HTTPError as e:
            errors = e.read()
            print "Error during ensure.:"
            print "  %s" % errors

    def ensure(self):
        if "device_token" not in self.db.get():
            self._get_authcode()
        if "token" not in self.db.get():
            self._new_refresh_token()

    def set_settings(self, settings):
        self.settings = settings

    def _url(self, resource):
        return "%s/%s/%s/%s" % (
            settings.APIS,
            self.service_name,
            self.api_version,
            resource
        )

    def _get_authcode(self):
        print "Oh man. Please auth me a token."
        query = self.post(settings.ACCOUNTS_LOGIN, {
            "client_id" : self.settings['client_id'],
            "scope"     : self.scope
        })
        self.db.get()['device_token'] = query
        self.db.write()
        print "Please visit %s and enter %s" % (
            query['verification_url'],
            query['user_code']
        )
        print "You've got %d minutes. Make it quick, shlub." % (
            (query['expires_in'] / 60)
        )
        sys.stdin.readline()

    def _new_refresh_token(self):
        refresh = self.post(settings.ACCOUNTS_TOKEN, {
            "client_id"     : self.settings['client_id'],
            "client_secret" : self.settings['client_secret'],
            "code"          : self.db.get()['device_token']['device_code'],
            "grant_type"    : "http://oauth.net/grant_type/device/1.0"
        })
        self.db.get()['token'] = refresh
        self.db.get()['refresh_token'] = refresh['refresh_token']
        self.db.write()

    def _refresh_token(self):
        refresh = self.post(settings.ACCOUNTS_TOKEN, {
            "client_id"     : self.settings['client_id'],
            "client_secret" : self.settings['client_secret'],
            "refresh_token" : self.db.get()['refresh_token'],
            "grant_type"    : "refresh_token"
        })
        self.db.get()['token'] = refresh
        self.db.write()

    def get(self, url, data):
        payload = json.load(get(url, data))
        return payload

    def post(self, url, data):
        payload = json.load(post(url, data))
        return payload

    def query(self, resource, **kwargs):
        token = self.db.get()['token']

        data = kwargs
        data["access_token"] = token['access_token']

        try:
            return self.get(self._url(resource), data)
        except urllib2.HTTPError as e:
            errors = e.read()
            #print "Error:"
            #print "  %s" % errors
            if e.getcode() == 401:
                #print "Forcing a token refresh."
                self._refresh_token()
                return self.query(resource, **kwargs)
            raise
