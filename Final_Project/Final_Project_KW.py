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
import time
#from time import mktime
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
cur.execute('DROP TABLE IF EXISTS yelp')

cur.execute('CREATE TABLE fb (post_id TEXT NOT NULL PRIMARY KEY, num_likes INTEGER, time_posted DATETIME, day DATETIME)')
cur.execute('CREATE TABLE insta (post_id TEXT NOT NULL PRIMARY KEY, num_likes INTEGER, time_posted DATETIME, day DATETIME)')
cur.execute('CREATE TABLE gmail (post_id TEXT NOT NULL PRIMARY KEY, sender TEXT, time_recieved DATETIME)')
cur.execute('CREATE TABLE youtube (id TEXT NOT NULL, chanTitle TEXT, viewCount INTEGER, time_posted DATETIME, day DATETIME)')
cur.execute('CREATE TABLE yelp (id TEXT NOT NULL, lon INT, lan INT)')


#def time_retr(time):

	#Morning times
#	morS = datetime.time(6, 0, 1)
#	morE = datetime.time(11, 59, 0)

	#afternoon times
#	aftS = datetime.time(12, 0, 1)
#	aftE = datetime.time(17, 59, 0)

	#night times
#	nighS = datetime.time(18, 0, 1)
#	nighE = datetime.time(23, 59, 0)

	#early morning times
#	EmorS = datetime.time(0, 0, 1)
#	EmorE = datetime.time(5, 59, 0)

#	if (time > morS & time < morE) :
#		return("6:00am - 12:00pm")
#	return("not done")

#insta
BASE_URL = 'https://api.instagram.com/v1/'

#EFFECTS: Gathering the Insta information into a CACHE 
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

	
		if user_info['meta']['code'] == 200:
		
			if len(user_info['data']):
				print(user_info['data'][0]['id'])
			else:
				print('non')
		else:
		
			print('Status code other than 200 recieved')
			exit()

#EFFECTS: Grabbing the URLs and putting in the database 
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

	#Putting the infromation into the database
	while i < 20:
		
		try:
			post_id = recent_post['data'][i]['id']
			count = recent_post['data'][i]['likes']['count']
			time_create = recent_post['data'][i]['created_time']
			conv_time = datetime.utcfromtimestamp(int(time_create))

			#Converting the time stamp
			ct = conv_time.strftime('%H:%M:%S')

			theday = calendar.day_name[conv_time.weekday()]

			i += 1
			#time_period = time_retr(ct)
			#print(time_period)
			cur.execute('INSERT INTO insta (post_id, num_likes, time_posted, day) VALUES (?, ?, ?, ?)',  (post_id, count, ct, theday), )	


		except KeyError:
			break

	request1_url = (BASE_URL + 'media/%s/likes?access_token=%s') %(post_id, access_token)



#EFFECTS: Gathering the Facebook results and putting it in the database 
def insert_user_fb():
	access_token = "EAADotjbU44IBALC0DG78VtrdfJZBdRn6O7UrC0k2zfRiljj5x2gIdwqOZA6H0e7XPOoJAILqZAbzhfMslBOZBDZALe4LARurVgHc8LLmVzUgVaAFNosUwIKSwTkC9PY4O6WgfmJ5znZBWZArQg9wXrMNr5Qq3GCSkoZD"

	cur = conn.cursor()

	
	graph = facebook.GraphAPI(access_token)
	fb_results = graph.get_connections('me', 'posts')

	query_string = 'posts?limit={0}'

	offset = 0
	lst = list()
	

	while offset < 100:

		try:
		#	print(fb_results)
			for post in fb_results['data']:
					#print(fb_results['data'] )
				count = 0
				likes = graph.get_connections(post['id'], connection_name='likes')
				for like in likes['data']:
					count += 1

				tup6 = post['id']
				cur.execute('SELECT * FROM fb where post_id = ?', (tup6,))


				my_data = (dateparser.parse(post['created_time']))
				time_data= my_data.strftime('%H:%M:%S')
				#print(time_data)
				new_date= (datetime.strptime(time_data, "%H:%M:%S"))
				
				try:
					acct = cur.fetchone()[0]

				except:

					cur.execute('INSERT INTO fb (post_id, num_likes, time_posted, day) VALUES (?, ?, ?, ?)',  (post['id'], count, my_data.strftime("%I:%M:%S %p"), calendar.day_name[my_data.weekday()]), )	
				
			offset += 19
					
					
			fb_results = requests.get(fb_results['paging']['next']).json()

		except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
			break

#EFFECTS: Gathering the information into a CACHE
#RETURN: All the results gathered
def get_user_fb():
	CACHE_FNAME = "Final_Project_cache.json"


	try:
		cache_file = open(CACHE_FNAME, 'r')
		cache_contents = cache_file.read()
		cache_file.close()
		CACHE_DICTION = json.loads(cache_contents)

	except:
		CACHE_DICTION = {}

	access_token = "EAADotjbU44IBALC0DG78VtrdfJZBdRn6O7UrC0k2zfRiljj5x2gIdwqOZA6H0e7XPOoJAILqZAbzhfMslBOZBDZALe4LARurVgHc8LLmVzUgVaAFNosUwIKSwTkC9PY4O6WgfmJ5znZBWZArQg9wXrMNr5Qq3GCSkoZD"
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

		#Dealing with pagination 
		while offset < 100:
			try:

				with open('Final_Project_cache.json', 'a' ) as f:

					
					for post in fb_results['data']:

						#r = json.dumps(post)
						CACHE_DICTION[user] = post
						f.write(json.dumps(CACHE_DICTION) + "\n")
						
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

#EFFECTS: Retrieves the data from the different API so they can be outputted on screen
def retrieve_data():
	from operator import itemgetter, attrgetter
	cur = conn.cursor()

	#Faceboo Output
	cur.execute('SELECT day FROM fb')
	counts = dict()
	lis = list()
	for row in cur:
		lis.append(str(row))
	
	for day in lis:
		counts[day] = counts.get(day, 0) + 1
	sort_ver = sorted(counts.items(), key=itemgetter(1), reverse = True)
	print('Days most active on Facebook')
	print(sort_ver)
	cur.execute('SELECT day FROM Insta')
	counts = dict()
	lis = list()
	for row in cur:
		lis.append(str(row))
	
	#Instagram Output
	for day in lis:
		counts[day] = counts.get(day, 0) + 1
	sort_ver = sorted(counts.items(), key=itemgetter(1), reverse = True)
	print('Days most active on Insta')
	print(sort_ver)



	
#EFFECTS: Gathering the information into a CACHE for Gmail
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

	SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
	CLIENT_SECRET_FILE = 'client_id.json'
	APPLICATION_NAME = 'apitime'
	#GetMessage()

#Gathering the authentication for Youtube
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

#EFFECTS: Putting the gmail information into the database   
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

	#Putting the scope
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
  
      
	#Getting the individual results
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
					#print(sender)




			cur.execute('INSERT INTO gmail (post_id, sender, time_recieved) VALUES (?, ?, ?)',  (m_id,sender, date), )

		f.close()

#Youtube authentication
def get_authenticated_service():
	flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
	credentials = flow.run_console()
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


# Build a resource based on a list of properties given as key-value pairs.
def build_resource(properties):
	resource = {}
	for p in properties:

		prop_array = p.split('.')
		ref = resource
	for pa in range(0, len(prop_array)):
		is_array = False
		key = prop_array[pa]


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

			ref[key] = {}
			ref = ref[key]
		else:

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

##EFFECTS: Gathering the most popular videos
def videos_list_most_popular(client, **kwargs):
 

	kwargs = remove_empty_kwargs(**kwargs)

	response = client.videos().list(
	**kwargs
	).execute()


	for res in response.get('items', []):


		my_data = (dateparser.parse(res['snippet']['publishedAt']))
		time_data= my_data.strftime('%H:%M:%S')
      # print(time_data)
      #new_date= (datetime.strptime(time_data, "%H:%M:%S"))
		tup = res['id'], res['snippet']['channelTitle'], res['statistics']['viewCount'],my_data.strftime("%I:%M:%S %p"),calendar.day_name[my_data.weekday()]
		cur.execute('INSERT INTO youtube (id, chanTitle, viewCount, time_posted, day) VALUES (?, ?, ?, ?, ?)',  tup, )

  #return print_response(response)

##EFFECTS: Calling and setting scopes for videos_list functions
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

#EFFECTS: Gathering the information into a CACHE, getting all the results and putting it in a database
def get_yelp():
	CACHE_FNAME = "Final_Project_yelp.json"

	cur = conn.cursor()
	app_id = 'HLFMMIEGVil6OfM8RfgS5Q'
	api_key = 'inCVmJm19AV8DNjDDaozhCMeQ9p7-CHlLVUbpvZIIfk3nUcNL_FoEa_awqToRZ1474JDl6XGfQpC40MTEhQ3SFwpog_NxPEj6z_TWYvF0k_IitUUTQT0_IHeFv4tWnYx'
	url = "https://api.yelp.com/v3/businesses/search"
	headers = {'Authorization': 'Bearer %s' %api_key}
	try:
		cache_file = open(CACHE_FNAME, 'r')
		cache_contents = cache_file.read()

		cache_file.close()
		
		CACHE_DICTION = json.loads(cache_contents)

	except:
  		CACHE_DICTION = {}

	user = 'McDonald'
	#print(CACHE_DICTION)
	if user in CACHE_DICTION:
		print('using cached data')
		search_US = CACHE_DICTION[user]
		for i in search_US['businesses']:
			if i['name'] == "McDonald's":
					#print(i['name'])
					#print(i['location'])
				tup = i['id'],i['coordinates']['longitude'],i['coordinates']['latitude']

				cur.execute('INSERT INTO yelp (id, lon, lan) VALUES (?, ?, ?)',  tup, )
		
	else:
		print('getting data from internet')



		offset = 0

		#To deal with pagination
		while offset < 100:
			param = {'term': 'McDonald',
					 'location': 'MI',
					 'sort_by': 'best_match',
					 'limit': 50,
					 'offset': offset

			}
			param2 = {'term': 'McDonald',
					 'location': 'OH',
					 'sort_by': 'best_match',
					 'limit': 6,
					 #'offset': offset

			}
			search_US = requests.get(url=url,params=param, headers=headers)
			search_OH = requests.get(url=url,params=param2, headers=headers)
			#data = [search_US.json(), search_OH.json()]
			#print(data)
			CACHE_DICTION[user] = search_US.json()
			

			f = open(CACHE_FNAME, "w")
			f.write(json.dumps(CACHE_DICTION) +"\n")
			CACHE_DICTION[user] = search_OH.json()
			f.write(json.dumps(CACHE_DICTION) )
			f.close()

			try:

				search_US = search_US.json()
				search_OH = search_OH.json()
			except:
				print('didnt work')
				pass
			
			offset +=50
		#print(search['businesses'])

			for i in search_US['businesses']:
				if i['name'] == "McDonald's":
					#print(i['name'])
					#print(i['location'])
					tup = i['id'],i['coordinates']['longitude'],i['coordinates']['latitude']

					cur.execute('INSERT INTO yelp (id, lon, lan) VALUES (?, ?, ?)',  tup, )
			for i in search_OH['businesses']:
				if i['name'] == "McDonald's":
					#print(i['name'])

					tup = i['id'],i['coordinates']['longitude'],i['coordinates']['latitude']

					cur.execute('INSERT INTO yelp (id, lon, lan) VALUES (?, ?, ?)',  tup, )





if __name__ == '__main__':
	get_user_insta()

	get_posts()
	faceb = get_user_fb()
	
	get_gmail()
	GetMessage()
	retrieve_data()
	get_youtube()
	get_yelp()
#get_gmail()
#insert_user_fb()
#d = json.loads(open('my_posts.json'))
	conn.commit()
	cur.close()


