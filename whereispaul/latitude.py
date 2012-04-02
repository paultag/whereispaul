# Copyright (c) Paul Tagliamonte

from whereispaul.googleservice import GoogleService

scope_host = "https://www.googleapis.com/auth"

scope = [
    #"latitude.current.best",
    #"latitude.current.city",
    "latitude.all.best"
]

class Latitude(GoogleService):
    def __init__(self, settings):
        self.set_settings(settings)
        sco = ""
        for s in scope:
            sco += "%s/%s " % (
                scope_host,
                s
            )
        self.scope = sco
        self.prime("latitude", "v1")
