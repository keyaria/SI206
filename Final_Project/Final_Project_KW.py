##SI 206 2017
## Final Project
## Keyaria Walker

import unittest
import itertools
import collections

import json
import sqlite3
from instagram.client import InstagramAPI
access_token = "189197666.3e5b08b.88c1b4c86c4940a086d79eab5ebed29d"

client_secret = "29a444e5be5f4fe18cb7ff3af8c48da2"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
usr = api.user("pandakeyaria")
my_usr = usr[0]
print ('User id is', my_usr.id, 'and name is ', my_usr.username)