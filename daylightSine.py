import json
import requests
import urllib.parse
import matplotlib.pyplot as plt
import numpy as np

def getDaylightLengthInMinutes(lat, lng, date, formatted=1):
	# get the length of daylight for a given location
	url = "https://api.sunrise-sunset.org/json"
	# add latitude, longitude and date to URL

	lat = str(lat)
	lng = str(lng)

	url = url + "?"
	url = url + "lat=" + lat
	url = url + "&lng=" + lng
	url = url + "&date=" + date
	req = requests.get(url)
	obj = req.json()
	dayLen = obj["results"]["day_length"]

	dLen_split = dayLen.split(":") # split into hours, mins, seconds
	d_hours = dLen_split[0]
	d_minutes = dLen_split[1]
	d_seconds = dLen_split[2]

	dLenMinutes = (int(d_hours) * 60) + (int(d_minutes)) + (int(d_seconds) / 60)
	print(dLenMinutes)
	return dLenMinutes

def getDayList():
	# get a list of ISO formatted dates to give to the API
	dayList = []

	daysToCheck = [7, 21]

	for i in range(1,13):
		# do this for every month
		for j in daysToCheck: # repeat for the no.
		# of days in this month
			dayStr = ""
			dayStr = dayStr + "2020" # add the year (2021 currently)
			dayStr = dayStr + "-" + str(i) # add the current month
			dayStr = dayStr + "-" + str(j) # add the current day
			dayList.append(dayStr)
	for i in range(1,13):
		# do this for every month
		for j in daysToCheck: # repeat for the no.
		# of days in this month
			dayStr = ""
			dayStr = dayStr + "2021" # add the year (2021 currently)
			dayStr = dayStr + "-" + str(i) # add the current month
			dayStr = dayStr + "-" + str(j) # add the current day
			dayList.append(dayStr)


	return dayList


def getListofDayLen():
	# get an array filled with the length (in minutes) of each day
	dList = getDayList() # array of ISO formatted dates
	dLenList = []
	for i in range(1,len(dList)):
		# for every date in the list
		dLen = getDaylightLengthInMinutes(52, -0.5, dList[i])
		dLenList.append(dLen)
	return dLenList

def translateRange(leftMin, leftMax, rightMin, rightMax, inArray):

	leftDif = float(leftMax - leftMin)
	rightDif = float(rightMax - rightMin)

	scaleFactor = rightDif/leftDif

	outArray = []
	# get the scale of each range
	for x in inArray:
		# translate all values in range
		trX = x*scaleFactor
		if (abs(trX) > 1):
			outArray.append(1*int(trX))
		else:
			outArray.append(trX)
	return outArray


def plotDayLen():
	# create a sine wave on the plot
	# plot length of day as well


	# first plot - sine wave

	x1 = np.arange(0,2*np.pi,0.1) # get a range of values from 0 to 2pi radians
	y1 = np.sin(x1*2)

	plt.plot(x1, y1)

	# now to do the length of the day in comparison

	dayLengthNP = np.array(getListofDayLen()) # create a numpy style array out of the standard list

	maxDLen = np.amax(dayLengthNP) # longest day
	minDLen = np.amin(dayLengthNP) # shortest day
	avg = (maxDLen + minDLen) / 2 # get the average day length

	dLenNormalised = []
	for x in dayLengthNP:
		dLenNormalised.append( ( (int(x) - avg) / avg ) )
	print(dLenNormalised)

	maxDLenNorm = np.amax(dLenNormalised)
	minDLenNorm = np.amin(dLenNormalised)

	translatedArr = translateRange(minDLenNorm, maxDLenNorm, -1, 1, dLenNormalised)
	print(translatedArr)

	radianTranslate = []
	#for z in translatedArr:
	for i in range(0, len(translatedArr)):
		z = translatedArr[i]
		rt = float( (i / len(translatedArr))-(40/365)) * 2*np.pi
		print(rt, "is the radian position, ", translatedArr.index(z), " is the index in db\n" )
		radianTranslate.append(rt)
	print(radianTranslate)

	


	# second plot - length of the day

	x2 = radianTranslate
	y2 = translatedArr
	plt.plot(x2, y2)

	plt.show()

plotDayLen()
