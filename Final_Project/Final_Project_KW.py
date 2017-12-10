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

#import requests-facebook
from instagram.client import InstagramAPI
#access_token = "EAACEdEose0cBABP8nJHJQZCGUT5GLTtKz0T1ZAOZBS1VVPVkI8sfFZBHBpsRqbn7LeBrxUB13EBZAYwkUjwWbEah1Kt085RZAWWOexVVKBpBo14iZA12UH5SjWifZCVYtAQGcoyqzHyZCbe3lj4lo6Q87t0iAYtG8F0m5DtPtjPiSZBd2WqvIaqP84FWGnOE9mbyaUIFF3ldHlDwZDZD"
#if access_token is None:
#	access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

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
cur.execute('DROP TABLE IF EXISTS insta')

cur.execute('CREATE TABLE fb (post_id TEXT NOT NULL PRIMARY KEY, num_likes INTEGER, time_posted DATETIME)')
cur.execute('CREATE TABLE insta (post_id TEXT NOT NULL PRIMARY KEY, num_likes INTEGER, time_posted DATETIME)')

#insta
BASE_URL = 'https://api.instagram.com/v1/'
def get_user_insta():
	access_token = "189197666.3e5b08b.88c1b4c86c4940a086d79eab5ebed29d"

	client_secret = "29a444e5be5f4fe18cb7ff3af8c48da2"
	api = InstagramAPI(access_token=access_token, client_secret=client_secret)
	#my_usr = api.user('189197666')

	request_url = (BASE_URL + 'users/search?q=%a&access_token=%s') % ('pandakeyaria', access_token)
	print('GET request ue : %s' % (request_url))
	user_info = requests.get(request_url).json()

	if user_info['meta']['code'] == 200:
		if len(user_info['data']):
			print(user_info['data'][0]['id'])
		else:
			print('non')
	else:
		print('Status code other than 200 recieved')
		exit()

def get_posts():
	cur = conn.cursor()
	access_token = "189197666.3e5b08b.88c1b4c86c4940a086d79eab5ebed29d"

	request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') %('189197666', access_token)
	recent_post = requests.get(request_url).json()
	if(recent_post['meta']['code'] == 200):
		if len(recent_post['data']) > 0:
			image_name = recent_post['data'][0]['id'] + ".jpeg"
			image_url = recent_post['data'][0]['images']['standard_resolution']['url']

		else:
			print("There are no posts to show")
	else:
		print("Error: not 200")
	
	print(recent_post['data'][1]['likes']['count'])
	i = 0
	while i < 20:
		
		try:
			post_id = recent_post['data'][i]['id']
			count = recent_post['data'][i]['likes']['count']
			time_create = recent_post['data'][i]['created_time']
			print(recent_post['data'][i]['created_time'])
			i += 1
			cur.execute('INSERT INTO insta (post_id, num_likes, time_posted) VALUES (?, ?, ?)',  (post_id, count, time_create), )	

		except KeyError:
			break
	request1_url = (BASE_URL + 'media/%s/likes?access_token=%s') %(post_id, access_token)
	#print('like url %s' %(request1_url))
	#likes = requests.get(request1_url).json()
	#print(likes)
	#print('number of likes' + likes)
	# print('the post' + recent_post['data'][0]['id'])


	#recent_media, next_ = api.user_recent_media(user_id="189197666", count=10)
	#for media in recent_media:
   	#	print(media.caption.text)
	#api.user_media_feed()
	#recent_media, next_ = api.user_recent_media(my_usr, count)
	##print ('User id is', my_usr.username)
	#print(my_usr.media)

#Need to add Facebook

def insert_user_fb():
	access_token = "EAACEdEose0cBAKsmYNA7TZBmC4qgZCz32qU3ToYQmBMEiKH91mFl0M1kZCtdKaKtZCiKySKQni3pr3YzbdFcyD7kUwyScHxyrPK8DthxlzQXfwYEKVymsdhHbVTVKo5Kn69yJA1wwC5Ci6ZADujPy959B2GV7giBdtzhx2eIngN55ZBCKmX55qwyBK2X31lsqQ77RLBAZCwLAZDZD"

	cur = conn.cursor()

	
		#access_token = input("EAACEdEose0cBADZC65ZA2AchHZBulPTWcZB1bmZAOCq2F8yZAnz3XIPSvePuM86yDpkpqD9ntLma1lGV129depZAZBgRxQXqVDYjqswZBO1qNu7RC4scLMCZBGPF115OxGJfYZAFDz5nyp1hOtBud3BQs4MCeWAtovjYLGAQokxbqR7UwD0LO13Ygu01LZBcareHZAJAZD")
	graph = facebook.GraphAPI(access_token)
	fb_results = graph.get_connections('me', 'posts')
	#profile = graph.get_object('me', fields = 'name,location')
	#print(json.dumps(profile, indent = 4))
	query_string = 'posts?limit={0}'
#	posts = graph.get_connections('me', 'posts')
	#fdffddffad
	offset = 0
	lst = list()
	
	#data = json.load(open('Final_Project_cache.json'))
	#print(json.dumps(data, indent=4))
	#print(fb_results)
	while offset < 100:
		#print(fb_results['data'])
		try:
		#	print(fb_results)
			for post in fb_results['data']:
					#print(fb_results['data'] )
				count = 0
				likes = graph.get_connections(post['id'], connection_name='likes')
				for like in likes['data']:
					count += 1
				#print(post)
				#tup = post['id'],count, count, post['created_time']
				tup6 = post['id']
				cur.execute('SELECT * FROM fb where post_id = ?', (tup6,))
		 		#conn.commit()
		 		#Trying to see if it is unique is not dont do anything
				try:
				#	print('Made it here')
					acct = cur.fetchone()[0]

				except:
		 			#print("User Exists")
					cur.execute('INSERT INTO fb (post_id, num_likes, time_posted) VALUES (?, ?, ?)',  (post['id'], count, post['created_time']), )	
				
				#cur.execute('INSERT INTO fb (post_id, num_likes, time_posted) VALUES (?, ?, ?)',  (post['id'], count, post['created_time']), )	
			offset += 19
					
					
			fb_results = requests.get(fb_results['paging']['next']).json()

		except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
			break

def get_user_fb(user):
	access_token = "EAACEdEose0cBAKsmYNA7TZBmC4qgZCz32qU3ToYQmBMEiKH91mFl0M1kZCtdKaKtZCiKySKQni3pr3YzbdFcyD7kUwyScHxyrPK8DthxlzQXfwYEKVymsdhHbVTVKo5Kn69yJA1wwC5Ci6ZADujPy959B2GV7giBdtzhx2eIngN55ZBCKmX55qwyBK2X31lsqQ77RLBAZCwLAZDZD"
	if access_token is None:
		access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

	if user in CACHE_DICTION:
		print('using cached data')
		fb_results = CACHE_DICTION[user]
	else:
		print('getting data from internet')
		graph = facebook.GraphAPI(access_token)
		fb_results = graph.get_connections('me', 'posts')
		count = 0
		offset = 0
		lr = dict()
		while offset < 100:
			try:

			#count = count + len (likes['data'])
        # Perform some action on each post in the collection we receive from
        # Facebook.
				with open('Final_Project_cache.json', 'a' ) as f:

					#lst.append(count)
					for post in fb_results['data']:

						#r = json.dumps(post)
						CACHE_DICTION[user] = post
						f.write(json.dumps(CACHE_DICTION) + "\n")
						

					#	lr = json.loads(r)
						#print(count)
						#tup = ps['id'],lr['story'],count, lr['created_time']
						#print(tup)
						#tup2 = lr['id'],lr['story'],count, lr['created_time']
						#print(tup2)
						#print(lr['id'])
					#	type(lr)
						#print(post["messages"])
						#print(lr)
				#f.close()
					#print(lst)	
				
				#print(tup)
				#print(lr)
			#	tup = lr		
				offset += 19
					
					
				fb_results = requests.get(fb_results['paging']['next']).json()

			except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
				break
		f.close()
	insert_user_fb()
	return fb_results
def get_gmail():
	request_url = "https://www.googleapis.com/gmail/v1/users/me/profile&key=ya29.GlseBdlphjF3BDFns897kg5Wbzz2umVpQGru-v7VjK_png07kIOKH4JDPvb64ZBIjyYSmEikZD4I2Z9DkY-8NLffmpE_KaXXfpLYsFiQsm7rzKL8SOMzd7qMLdrD"
	print('GET request ue : %s' % (request_url))

	access_token= "ya29.GlseBdlphjF3BDFns897kg5Wbzz2umVpQGru-v7VjK_png07kIOKH4JDPvb64ZBIjyYSmEikZD4I2Z9DkY-8NLffmpE_KaXXfpLYsFiQsm7rzKL8SOMzd7qMLdrD",
	user_info = requests.get(request_url).json()

	print(user_info)

	#from oauth2client.client import OAuth2WebServerFlow

	#flow = OAuth2WebServerFlow(client_id='60246787954-01thr1e518mr3l7upgse73798inf4439.apps.googleusercontent.com',
	#						client_secret='MdZH07Gp4atU8OVrE3Jed13h',
	##						scope='https://www.googleapis.com/auth/gmail',
	#						redirect_uri='https://google.com')
	#auth_uri = flow.step1_get_authorize_url()
#service = build('gmail', 'v4', developerKey=ya29.GlseBdlphjF3BDFns897kg5Wbzz2umVpQGru-v7VjK_png07kIOKH4JDPvb64ZBIjyYSmEikZD4I2Z9DkY-8NLffmpE_KaXXfpLYsFiQsm7rzKL8SOMzd7qMLdrD)

#def what(url,headers):
#get_user_insta()
#get_posts()
#faceb = get_user_fb("me")
get_gmail()
#insert_user_fb()
#d = json.loads(open('my_posts.json'))
conn.commit()
cur.close()

#Github

#some type of google api

#Youtube addin something

#COmments