##SI 206 2017
## Final Project
## Keyaria Walker
from __future__ import print_function
from datetime import datetime
import dateutil.parser as dateparser
import calendar
import unittest
import itertools
import collections
import requests
import json
import sqlite3
import facebook

import httplib2
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
#import requests-facebook
from instagram.client import InstagramAPI
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
#access_token = "EAACEdEose0cBABP8nJHJQZCGUT5GLTtKz0T1ZAOZBS1VVPVkI8sfFZBHBpsRqbn7LeBrxUB13EBZAYwkUjwWbEah1Kt085RZAWWOexVVKBpBo14iZA12UH5SjWifZCVYtAQGcoyqzHyZCbe3lj4lo6Q87t0iAYtG8F0m5DtPtjPiSZBd2WqvIaqP84FWGnOE9mbyaUIFF3ldHlDwZDZD"
#if access_token is None:
#	access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

#Cache setup
CLIENT_SECRETS_FILE = "client_secret.json"


SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


conn = sqlite3.connect('Final_Project.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS fb')
cur.execute('DROP TABLE IF EXISTS insta')
cur.execute('DROP TABLE IF EXISTS gmail')
cur.execute('DROP TABLE IF EXISTS youtube')

cur.execute('CREATE TABLE fb (post_id TEXT NOT NULL PRIMARY KEY, num_likes INTEGER, time_posted DATETIME, day DATETIME)')
cur.execute('CREATE TABLE insta (post_id TEXT NOT NULL PRIMARY KEY, num_likes INTEGER, time_posted DATETIME, day DATETIME)')
cur.execute('CREATE TABLE gmail (post_id TEXT NOT NULL PRIMARY KEY, sender TEXT, time_recieved DATETIME)')
cur.execute('CREATE TABLE youtube (id TEXT NOT NULL, chanTitle TEXT, viewCount INTEGER, time_posted DATETIME, day DATETIME)')

#insta
BASE_URL = 'https://api.instagram.com/v1/'
def get_user_insta():	
	cur = conn.cursor()
	access_token = "189197666.3e5b08b.88c1b4c86c4940a086d79eab5ebed29d"
	

	client_secret = "29a444e5be5f4fe18cb7ff3af8c48da2"
	api = InstagramAPI(access_token=access_token, client_secret=client_secret)
	CACHE_FNAME = "Final_Project_insta.json"


	try:
		cache_file = open(CACHE_FNAME, 'r')
		cache_contents = cache_file.read()
		cache_file.close()
		CACHE_DICTION = json.loads(cache_contents)

	except:
		CACHE_DICTION = {}
		

		
	user = '1647977160834807241_189197666'
	if user in CACHE_DICTION:
		print('using cached data')
		user_info = CACHE_DICTION[user]
	else:

		print('getting data from internet')
		request_url = (BASE_URL + 'users/search?q=%a&access_token=%s') % ('pandakeyaria', access_token)
		print('GET request ue : %s' % (request_url))
		user_info = requests.get(request_url).json()
		CACHE_DICTION[user] = user_info
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	#my_usr = api.user('189197666')



	
		if user_info['meta']['code'] == 200:
		
			if len(user_info['data']):
				print(user_info['data'][0]['id'])
			else:
				print('non')
		else:
		
			print('Status code other than 200 recieved')
			exit()

def get_posts():

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
			conv_time = datetime.utcfromtimestamp(int(time_create))
			#conv_time = datetime.strptime(conv_time, "%H:%M:%S")
			#new_date= (conv_time.strptime(conv_time, "%H:%M:%S"))
			#conv_time = datetime(conv_time)
			ct = conv_time.strftime('%I:%M:%S %p')
			#print(conv_time)
			#print(ct)
			theday = calendar.day_name[conv_time.weekday()]
			#print(calendar.day_name[conv_time.weekday()])

			#print(recent_post['data'][0]['created_time'])
			#print(dateparser.parse(recent_post['data'][0]['created_time'])	)
			#print(recent_post['data'][i]['created_time'])
			i += 1
			cur.execute('INSERT INTO insta (post_id, num_likes, time_posted, day) VALUES (?, ?, ?, ?)',  (post_id, count, conv_time, theday), )	

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
	access_token = "EAACEdEose0cBACL4RZBgLVr277vZBz4mbPL7pC2EfWN6JrKAYdtSdfYD4qhTl07s9ITAa4gY6rQ6sItou6H4z6Cv9pltMYhlQIIblBFpuZBRsC5CalJwUvZCZCUewE5gBBewIk1iDtCyeuvPTGI8k5gfM3XV0btbXbNPqoX1ZCyZAb6sRE6STwsW5hfVb8eSNZCtvHPFXfRpyQZDZD"

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
				#datetime(*strptime(s, "%Y-%m-%dT%H:%M:%S")[0:6])

				my_data = (dateparser.parse(post['created_time']))
				time_data= my_data.strftime('%H:%M:%S')
				#print(time_data)
				new_date= (datetime.strptime(time_data, "%H:%M:%S"))

				#print(new_date.strftime("%I:%M:%S %p"))
				#print(calendar.day_name[my_data.weekday()])
		 		#conn.commit()
		 		#Trying to see if it is unique is not dont do anything
				try:
				#	print('Made it here')
					acct = cur.fetchone()[0]

				except:
		 			#print("User Exists")
					cur.execute('INSERT INTO fb (post_id, num_likes, time_posted, day) VALUES (?, ?, ?, ?)',  (post['id'], count, my_data.strftime("%I:%M:%S %p"), calendar.day_name[my_data.weekday()]), )	
				
				#cur.execute('INSERT INTO fb (post_id, num_likes, time_posted) VALUES (?, ?, ?)',  (post['id'], count, post['created_time']), )	
			offset += 19
					
					
			fb_results = requests.get(fb_results['paging']['next']).json()

		except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
			break

def get_user_fb():
	CACHE_FNAME = "Final_Project_cache.json"


	try:
		cache_file = open(CACHE_FNAME, 'r')
		cache_contents = cache_file.read()
		cache_file.close()
		CACHE_DICTION = json.loads(cache_contents)

	except:
		CACHE_DICTION = {}

	access_token = "EAACEdEose0cBACL4RZBgLVr277vZBz4mbPL7pC2EfWN6JrKAYdtSdfYD4qhTl07s9ITAa4gY6rQ6sItou6H4z6Cv9pltMYhlQIIblBFpuZBRsC5CalJwUvZCZCUewE5gBBewIk1iDtCyeuvPTGI8k5gfM3XV0btbXbNPqoX1ZCyZAb6sRE6STwsW5hfVb8eSNZCtvHPFXfRpyQZDZD"
	if access_token is None:
		access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")
	user = 'me'
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
def retrieve_data():
	from operator import itemgetter, attrgetter
	cur = conn.cursor()
	cur.execute('SELECT day FROM fb')
	counts = dict()
	lis = list()
	for row in cur:
		lis.append(str(row))
	
	for day in lis:
		counts[day] = counts.get(day, 0) + 1
	sort_ver = sorted(counts.items(), key=itemgetter(1), reverse = True)
	print('Days most active')
	print(sort_ver)
	

def get_gmail():
	CACHE_FNAME = "Final_Project_gmail.json"


	try:
		cache_file = open(CACHE_FNAME, 'r')
		cache_contents = cache_file.read()
		cache_file.close()
		CACHE_DICTION = json.loads(cache_contents)

	except:
  		CACHE_DICTION = {}



	cur = conn.cursor()


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
	SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
	CLIENT_SECRET_FILE = 'client_id.json'
	APPLICATION_NAME = 'apitime'
	#GetMessage()

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    
def GetMessage():
	CACHE_FNAME = "Final_Project_gmail.json"


	try:
		cache_file = open(CACHE_FNAME, 'r')
		cache_contents = cache_file.read()
		cache_file.close()
		CACHE_DICTION = json.loads(cache_contents)

	except:
  		CACHE_DICTION = {}



	cur = conn.cursor()


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
	SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
	CLIENT_SECRET_FILE = 'client_id.json'
	APPLICATION_NAME = 'apitime'
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)
	date = 0
	sender = ''
	user = '16032b49493fdc35'
	if user in CACHE_DICTION:
		print('using cached data')
		msgs = CACHE_DICTION[user]
	else:
		print('getting data from internet')
  
   # try:
   #   message = service.users().messages().get(userId='me', id='16038100b2b13aa4').execute()
   #   payload = message['payload'] 
  #    header = payload['headers']
   #   for item in header:
    #    if item['name'] == 'Date':
         # date = item['value']
     # print('Message snippet: %s' % message['snippet'])
      #print('Message Date: %s' % message['internalDate'])
      #print(date)

      
    #except errors.HttpError:
    #  print ('An error occurred: %s' % error)
	with open('Final_Project_gmail.json', 'a' ) as f:
		msgs = service.users().messages().list(userId='me', maxResults=100).execute()
		for msg in msgs['messages']:
			CACHE_DICTION[user] = service.users().messages().get(userId='me', id=msg['id']).execute()
			f.write(json.dumps(CACHE_DICTION) + "\n")
			m_id = msg['id'] # get id of individual message
			message = service.users().messages().get(userId='me', id=m_id).execute()
			payload = message['payload'] 
			header = payload['headers']
      #print(header)
			for item in header:
				if item['name'] == 'Date':
					date = item['value']
				if item['name'] == 'From':
					sender = item['value']

			cur.execute('INSERT INTO gmail (post_id, sender, time_recieved) VALUES (?, ?, ?)',  (m_id,sender, date), )
	f.close()
      #print(m_id + '' + date + '' + sender)


	#from oauth2client.client import OAuth2WebServerFlow

	#flow = OAuth2WebServerFlow(client_id='60246787954-01thr1e518mr3l7upgse73798inf4439.apps.googleusercontent.com',
	#						client_secret='MdZH07Gp4atU8OVrE3Jed13h',
	##						scope='https://www.googleapis.com/auth/gmail',
	#						redirect_uri='https://google.com')
	#auth_uri = flow.step1_get_authorize_url()
#service = build('gmail', 'v4', developerKey=ya29.GlseBdlphjF3BDFns897kg5Wbzz2umVpQGru-v7VjK_png07kIOKH4JDPvb64ZBIjyYSmEikZD4I2Z9DkY-8NLffmpE_KaXXfpLYsFiQsm7rzKL8SOMzd7qMLdrD)
def get_authenticated_service():
	flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
	credentials = flow.run_console()
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
	resource = {}
	for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
		prop_array = p.split('.')
		ref = resource
	for pa in range(0, len(prop_array)):
		is_array = False
		key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
		if key[-2:] == '[]':
			key = key[0:len(key)-2:]
			is_array = True

		if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
			if properties[p]:
				if is_array:
					ref[key] = properties[p].split(',')
			else:
				ref[key] = properties[p]
		elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
			ref[key] = {}
			ref = ref[key]
		else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
			ref = ref[key]
	return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
	good_kwargs = {}
	if kwargs is not None:
		for key, value in kwargs.items():
			if value:
				good_kwargs[key] = value
	return good_kwargs

def videos_list_most_popular(client, **kwargs):
  # See full sample for function

	kwargs = remove_empty_kwargs(**kwargs)

	response = client.videos().list(
	**kwargs
	).execute()



	for res in response.get('items', []):
  #  print(res['id'])
   # print(res['snippet']['publishedAt'] +' ' +res['snippet']['channelTitle'])
  #  print(res['statistics']['viewCount'] + ' ' + res['statistics']['likeCount'])

		my_data = (dateparser.parse(res['snippet']['publishedAt']))
		time_data= my_data.strftime('%H:%M:%S')
      # print(time_data)
      #new_date= (datetime.strptime(time_data, "%H:%M:%S"))
		tup = res['id'], res['snippet']['channelTitle'], res['statistics']['viewCount'],my_data.strftime("%I:%M:%S %p"),calendar.day_name[my_data.weekday()]
		cur.execute('INSERT INTO youtube (id, chanTitle, viewCount, time_posted, day) VALUES (?, ?, ?, ?, ?)',  tup, )

  #return print_response(response)

def get_youtube():
	CLIENT_SECRETS_FILE = "client_secret.json"


	SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
	API_SERVICE_NAME = 'youtube'
	API_VERSION = 'v3'
	client = get_authenticated_service()
  
	videos_list_most_popular(client,
		part='snippet,contentDetails,statistics',
		chart='mostPopular',
		maxResults=50,
		regionCode='US',
		videoCategoryId='')
	videos_list_most_popular(client,
		part='snippet,contentDetails,statistics',
		chart='mostPopular',
		maxResults=50,
		regionCode='CA',
		videoCategoryId='')

def get_yelp():
	app_id = 'HLFMMIEGVil6OfM8RfgS5Q'
	api_key = 'inCVmJm19AV8DNjDDaozhCMeQ9p7-CHlLVUbpvZIIfk3nUcNL_FoEa_awqToRZ1474JDl6XGfQpC40MTEhQ3SFwpog_NxPEj6z_TWYvF0k_IitUUTQT0_IHeFv4tWnYx'
	url = "https://api.yelp.com/v3/businesses/search"
	headers = {'Authorization': '	Bearer %s' % api_key}
	uniqlo = list()
	offset = 0

	while offset < 100:
		param = {'location': 'USA',
				 'term': 'Uniqlo',
				 'sort_by': 'best_match',
				 'limit': 50,
				 'offset': offset

		}
	print(requests.get(url=url,params=param, headers=headers))
	search = requests.get(url=url,params=param, headers=headers)
	print('here')
	try:

		search = search.json()
	except:
		print('didnt work')
		pass
		
	offset +=50
	for i in search['businesses']:
		if i['name'] == "Uniqlo":
			uniqlo[i['location']['city']].append(i['name'])
		else:
			break
	print(uniqlo)


#CHECK ALL CACHES THEY DONT REALLY WORK!!!!!!!!!!
#def what(url,headers):
if __name__ == '__main__':
	#get_user_insta()

	#get_posts()
	#faceb = get_user_fb()
	#retrieve_data()
	#get_gmail()
	#GetMessage()
	#get_youtube()
	get_yelp()
#get_gmail()
#insert_user_fb()
#d = json.loads(open('my_posts.json'))
	conn.commit()
	cur.close()


#Github

#some type of google api

#Youtube addin something

#COmments