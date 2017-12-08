##SI 206 2017
## Final Project
## Keyaria Walker
import datetime
import unittest
import itertools
import collections
import requests
import json
import sqlite3
import facebook
from instagram.client import InstagramAPI

#Cache setup
CACHE_FNAME = "Final_Project_cache.json"


try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)

except:
	CACHE_DICTION = {}

conn = sqlite3.connect('Final_Project.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS fb')

cur.execute('CREATE TABLE fb (post_id TEXT NOT NULL PRIMARY KEY UNIQUE, post_mes TEXT, num_likes INTEGER, time_posted DATETIME)')
#insta
def get_user_insta():
	access_token = "189197666.3e5b08b.88c1b4c86c4940a086d79eab5ebed29d"

	client_secret = "29a444e5be5f4fe18cb7ff3af8c48da2"
	api = InstagramAPI(access_token=access_token, client_secret=client_secret)
	usr = api.user("pandakeyaria")
	my_usr = usr[0]
	print ('User id is', my_usr.id, 'and name is ', my_usr.username)

#Need to add Facebook

def insert_user_fb():
	cur = conn.cursor()

	offset = 0
	access_token = "EAACEdEose0cBAKZA9tAKIac7OIw4NgXYSEkUQKvCxusivcgIiA1QbLQ2IXZBP7BGN8gxBza7G4Ko14T48ug5yV1kRv5m9PLEGVS2SV9ZA0cjXGGozsomP0lANb7Pel32ktuH6Q2lmuixSbSnZBXPZBPU53O4ZBWOVwQdAhBWj7CxvGaKKNZBMZBjkNu5ZC0yaAlfZBZBz9JYKxYvQZDZD"
	if access_token is None:
		 access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")
		#access_token = input("EAACEdEose0cBADZC65ZA2AchHZBulPTWcZB1bmZAOCq2F8yZAnz3XIPSvePuM86yDpkpqD9ntLma1lGV129depZAZBgRxQXqVDYjqswZBO1qNu7RC4scLMCZBGPF115OxGJfYZAFDz5nyp1hOtBud3BQs4MCeWAtovjYLGAQokxbqR7UwD0LO13Ygu01LZBcareHZAJAZD")
	graph = facebook.GraphAPI(access_token)
	#profile = graph.get_object('me', fields = 'name,location')
	#print(json.dumps(profile, indent = 4))
	query_string = 'posts?limit={0}'
	posts = graph.get_connections('me', 'posts', limit=100)
	
	lst = list()
	
	#numofposts = 0
	while offset < 100:
		try:

			#count = count + len (likes['data'])
        # Perform some action on each post in the collection we receive from
        # Facebook.
			with open('my_posts.json', 'a' ) as f:
				for post in posts['data']:
					likes = graph.get_connections(post['id'], connection_name='likes')
					count = 0
					for like in likes['data']:
						count += 1
					lst.append(count)
					f.write(json.dumps(post)+"\n")
					#print(lst)	
					#print(post['id']['data']
					#tup = post['id'],post['message'],count, post['created_time']
					#cur.execute('INSERT INTO fb (post_id, post_mes, num_likes, time_posted) VALUES (?, ?, ?, ?)''',  tup,)	
					#conn.commit()


					#print(tup)
				#print(posts['data']['id'])
				#tup = posts['id']['data'],post['message']['data'],count, post['created_time']['data']
				#cur.execute('INSERT INTO fb (post_id, post_mes, num_likes, time_posted) VALUES (?, ?, ?, ?)''',  tup,)						
					
	#print(likes)
				offset += 50
					
					#print(post['likes'])
				#conn.close()

        # Attempt to make a request to the next page of data, if it exists.
			
				posts = requests.get(posts['paging']['next']).json()
			
				#for n in post['likes']['data']:
				#	print(n + "\n")
					
				#print(posts)
		except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
			break
	
#def get_user_fb():

#	if user in CACHE_DICTION:
#		print('using cached data')
#		fb_results = CACHE_DICTION[user]
#	else:
#		print('getting data from internet')

#		fb_results = graph.get_object('me', fields = 'name,location')
#		CACHE_DICTION[user] = fb_results
#		f.write(json.dumps(CACHE_DICTION))
#		f.close()
#	insert_user_fb(fb_results)
#	return fb_results
insert_user_fb()
conn.commit()
#conn.close()
cur.close()
#Github

#some type of google api

#Youtube addin something

#COmments