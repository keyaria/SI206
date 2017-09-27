import os
import filecmp
import csv 
import sys

def getData(file):
#Input: file name
#Ouput: return a list of dictionary objects where 
#the keys will come from the first row in the data.

#Note: The column headings will not change from the 
#test cases below, but the the data itself will 
#change (contents and size) in the different test 
#cases.
	fname = open(file)
	reader = csv.reader(fname)
	next(reader)
	lst = list()
	
	for i in reader:
		mydict = {}
	
		mydict['First'] = i[0]
		mydict['Last'] = i[1]
		mydict['Email'] = i[2]
		mydict['Class'] = i[3]
		mydict['DOB'] = i[4]
		lst.append(mydict)

	#print(lst)



	return lst	

#Sort based on key/column
def mySort(data,col):
#Input: list of dictionaries
#Output: Return a string of the form firstName lastName

	#Your code here: sort by key first then sort by first name

	 from operator import itemgetter, attrgetter
	 s = sorted(data, key=itemgetter(col))

	 str1 = s[0]



	 #print(s)
	 return str1['First'] + " " + str1['Last']

	
#Create a histogram
def classSizes(data):
# Input: list of dictionaries
# Output: Return a list of tuples ordered by
# ClassName and Class size, e.g 
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]

	#Your code here:
	from collections import Counter
	


	tup = Counter()			#Initialize my Counter
	#Add things to it
	for i in data:
		tup[i['Class']] += 1

	from operator import itemgetter, attrgetter
	netup = sorted(tup.items(), key=itemgetter(1), reverse = True)
	return list(netup)



# Find the most common day of the year to be born
def findDay(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB
	
	daycount = dict()
	#Your code here:
	for i in a:
		dob = i['DOB']
		spil = dob.split('/')
		day = spil[1]
		if day in daycount :
			daycount[day] += 1
		else:
			daycount[day] = 1

	#from collections import Counter
	#counter = collections.Counter(daycount)
	#tup = counter.most_common(1)
	#counter = [i for i, j in Counter(daycount).most_common(1)]
	lst = list()
	for i in daycount.keys():
		tup = (i, daycount[i])
		lst.append(tup)

	lssort =sorted(lst, reverse = True, key = lambda k: k[1])

	common = sorted(daycount, key = daycount.get, reverse = True)
	return int(lssort[0][0])
	
		


# Find the average age (rounded) of the Students
def findAge(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB

	from datetime import date, timedelta
	today = date.today()
	age = list()
	add = 0
	
	for i in a:
		dob = i['DOB']
		spil = dob.split('/')
		needyear = spil[2]
		
		age.append(today.year - int(needyear))

	
	for i in age:
		add += i

	
	return (round(add / (len(age))))

	
	

#Similar to mySort, but instead of returning single
#Student, all of the sorted data is saved to a csv file.
def mySortPrint(a,col,fileName):
#Input: list of dictionaries, key to sort by and output file name
#Output: None
	from operator import itemgetter, attrgetter
	s = sorted(a, key=itemgetter(col))
	
	#with open('fileName', 'wb') as csvfile:
	#keys = s[0].keys()

	headers = ['First', 'Last', 'Email']
	file = open(fileName,"w", newline="\n")
	dict_writer = csv.DictWriter(file, headers,extrasaction='ignore', lineterminator='\n')
	dict_writer.writerows(s)
	#str1 = s[]
	#file.write(str1['First'] + "," + str1['Last'] + "," +str1['Email'])


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ",end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),40)
	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',15)
	total += test(mySort(data2,'First'),'Adam Rocha',15)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',15)
	total += test(mySort(data2,'Last'),'Elijah Adams',15)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',15)
	total += test(mySort(data2,'Email'),'Orli Humphrey',15)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],10)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],10)

	print("\nThe most common day of the year to be born is:")
	total += test(findDay(data),13,10)
	total += test(findDay(data2),26,10)
	
	print("\nThe average age is:")
	total += test(findAge(data),39,10)
	total += test(findAge(data2),41,10)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,10)


	print("Your final score is: ",total)
# Standard boilerplate to call the main() function that tests all your code.
if __name__ == '__main__':
    main()

