# Wallpapers from /r/EarthPorn

This Script will download all the Images (First page of hot section) from /r/EarthPorn subreddit to a local folder every 24 hours.
It will also automate a Slideshow change of Wallpapers from that local storage. Wallpaper will change every 30 Minutes.
This works only on Gnome Based Desktops.

### Libraries Required:
glob, urllib2, json, getpass
```python
sudo pip install glob urllib2 json getpass
```

### To run the code
In terminal:
```python
nohup python wallpaper.py &
```
##### nohup command is used to keep the script running in background, even when the terminal is closed

### Add the script to run it as startup application

##### Goto "Startup Applications"
##### Click "Add" -> Click "Custom Command" -> Enter command as "nohup python ~/wallpaper.py &", enter name and other details and save


##### Custom Preferences and more Subreddits comming soon!
