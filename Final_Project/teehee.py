from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import sqlite3
import json
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

CACHE_FNAME = "Final_Project_gmail.json"


try:
  cache_file = open(CACHE_FNAME, 'r')
  cache_contents = cache_file.read()
  cache_file.close()
  CACHE_DICTION = json.loads(cache_contents)

except:
  CACHE_DICTION = {}
conn = sqlite3.connect('Final_Project.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS gmail')

cur.execute('CREATE TABLE gmail (post_id TEXT NOT NULL PRIMARY KEY, sender TEXT, time_recieved DATETIME)')


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'apitime'
    

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
      
def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])


    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])

    try:
      response = service.users().messages().list(userId='me',
                                               q=100).execute()
    
      messages = []
      if 'messages' in response:
        messages.extend(response['messages'])

      while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me', q=100,
                                         pageToken=page_token).execute()
        messages.extend(response['messages'])

      print(messages)
    except errors.HttpError:
      print ('An error occurred: %s' % error)
    GetMessage()
    conn.commit()
    cur.close()

if __name__ == '__main__':
    main()