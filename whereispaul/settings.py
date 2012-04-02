# Copyright (c) Paul Tagliamonte

USER_AGENT     = "whereispaul/1.0"
##################################
ACCOUNTS       = 'https://accounts.google.com'
ACCOUNTS_OAUTH = 'o/oauth2'
ACCOUNTS_LOGIN = '%s/%s/device/code' % (
    ACCOUNTS,
    ACCOUNTS_OAUTH
)
ACCOUNTS_TOKEN = '%s/%s/token' % (
    ACCOUNTS,
    ACCOUNTS_OAUTH
)
##################################
APIS           = 'https://www.googleapis.com'
