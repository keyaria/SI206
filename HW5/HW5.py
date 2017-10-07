import re

def reg(file):
	lst=[]
	fh= open(file, "r")
	for line in fh:
		line = line.rstrip()
		
		stuff = re.findall('[0-9]+', line)
		
		if stuff != [] : 
			lst.extend(stuff)


	sum_lst = 0
	for a in lst:
		sum_lst += int(a)
	return (sum_lst)



#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verfiy_mode = ssl.CERT_NONE

#url = input('Enter -')
#html = urlopen(url, context=ctx).read()

print(reg("regex_sum_42.txt"))
print(reg("regex_sum_31934.txt"))
