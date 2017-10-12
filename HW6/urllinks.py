# To run this, you can install BeautifulSoup
# https://pypi.python.org/pypi/beautifulsoup4

# Or download the file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')

count = int(input("Enter count: "))
position = int(input("Enter position: "))
othercount = 0

#for tag in tags:
lst = [] 


#findall
for i in range(count):

	html = urllib.request.urlopen(url, context=ctx).read()
	soup = BeautifulSoup(html, 'html.parser')
	tags = soup('a')
	print (tags[position-1].get('href', None))
	# if othercount == position:
	# 	#url = urllib.request.urlopen(tag[position - 1], context=ctx).read()
	url = tags[position-1].get('href', None)
	# 	tags.contents[position-1]
	# 	print(tags)
	# #lst.append(tag.get('href', None))

