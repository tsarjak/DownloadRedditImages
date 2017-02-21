import glob
import urllib2
import json
import os
import getpass
import time

#URL of the EarthPorn JSON
url = 'http://www.reddit.com/r/earthporn.json' 
WallpaperCount=0


#Returns a list of wallpapers from the folder
def returnwallpaper():
	username = getpass.getuser()
	listWallpaper = glob.glob("/home/"+username+"/twallpapers/*.jpg")
	print("Wallpapers Returned : ",listWallpaper)	
	return listWallpaper
	
#Gets the list of wallpaper and sets a new wallpaper based on count
def setwallpaper(listwallpaper, count):
	filepath = "gsettings set org.gnome.desktop.background picture-uri file:" + listwallpaper[count]
	os.system(filepath)


def download(dCount):

	#open the URL of earthporn JSON and store the JSON data in umm... data
	obj = urllib2.urlopen(url)
	data = json.load(obj)

	#Directory to save the downloaded images
	username = getpass.getuser() #Gets current user to save files accordingly
	directory = "/home/"+username+"/Wallpapers/"

	#Check if Directory alredy exists, If doesn't exist, create new directory
	if not os.path.exists(directory):
		os.makedirs(directory)
		print("New directory Made!")
  
	for i in data["data"]["children"]:

	  imurl = i["data"]["url"]
	  checkUrl = str(imurl)

	  #Checking if the link extracted is actually an image
	  if "jpg" in checkUrl:
	  	print(checkUrl)
	  	try:

		    print imurl
	    
		    req = urllib2.Request(imurl+".jpg")
		    if req:
	    		print('Request done.')
		    #Get the Data in the URL
		    imgdata = urllib2.urlopen(req).read()
		    
		    #Create a new image file and write to it
		    fp = open((directory + "%s"+".jpg") %(dCount) ,"wb")
		    
		    fp.write(imgdata)

		    fp.close()

		    dCount = dCount + 1
	    
		except:
		    pass
	    
  
  	print dCount
  	return dCount


#Time Countdown function to check wallpaper change time or download time
def countdownDownload(timerDownload, timerupdate,count):

	stu = timerupdate
	
	listwallpaper = returnwallpaper()
	WallpaperCount = len(listwallpaper)
	
	#24 hour loop
	while timerDownload:
		#1 Minute Loop
	    while timerupdate:
	        time.sleep(1)
	        timerupdate -= 1
	    print("End of 30 Minutes, Wallpaper to be changed!")
	    
	    if(count>=WallpaperCount):
	    	count = 0

	    setwallpaper(listwallpaper,count)	
	    count += 1	

	    timerupdate = stu	
	    timerDownload = timerDownload - stu

	dCount = download()
	return dCount



#Function to fetch preferences from file
def fetchPreferences():
	Preferences = list()
	pref = open("WpPreferences.txt","r")
	for word in pref.read().split():
		Preferences.append(int(word))
	return Preferences

#Function to the Index of Latest downloaded Wallpaper
def saveToPreferences(Preferences):
	for i in range(0,5):
		Preferences[i] = str(Preferences[i])
		Preferences[i] = Preferences[i] + "\n"
	with open('WpPreferences.txt', 'w') as file:
		file.writelines(Preferences)

#To download wallpapers automatically on first run
def firstTimeDownload(Preferences):
	if Preferences[3] == 0:
		print("Downloading for the first time!")
		dCount = download()
		Preferences[3] = 1
		Preferences[4] = dCount
	saveToPreferences(Preferences)
	return Preferences



Preferences = fetchPreferences()
Preferences = firstTimeDownload(Preferences)
Preferences = fetchPreferences()

timerDownload = Preferences[2] * 60 * 60
timerupdate = Preferences[1] * 60


while(1):
	count=0
	dCount = countdownDownload(timerDownload, timerupdate,count)
	Preferences[4] = dCount
	saveToPreferences(Preferences)