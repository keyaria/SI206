from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')
html = urlopen(url, context=ctx).read()
counter = 0
sum_lst = 0
# html.parser is the HTML parser included in the standard Python 3 library.
# information on other HTML parsers is here:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the anchor tags
tags = soup('span')
for tag in tags:
    # Look at the parts of a tag
   # print('TAG:', tag)
   # print('URL:', tag.get('href', None))
   # print('Contents:', tag.contents[0])
   # print('Attrs:', tag.attrs)
   # tag = tag.rstrip()
	counter += 1
	sum_lst += int(tag.contents[0])



	

print("Count", counter)
print("Sum", sum_lst)
