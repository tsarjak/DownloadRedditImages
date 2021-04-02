# Download Images and Set Wallpapers from your choice of Subreddit!

Using this script:
* **No Setup Needed!**
* **Download any number of images** from **Any Subreddit!**
* Select your sort type **(Top, Hot, New, Controversial)**
* Select your sort time **(All, Year, Month, Week, Day)**
* Extremely **Reliable Downloading.**
* **Automatically set and switch Wallpaper** from the downloaded images
* **Store the links** to all the downloaded images (in case you want to access later?)

This Script will download all the Images (First page of hot section) from /r/Wallpaper subreddit to a local folder every 24 hours.
It will also automate a Slideshow change of Wallpapers from that local storage. Wallpaper will change every 30 Minutes.
This works only on Gnome Based Desktops.

## No Dependencies! Just Download and Run!
Just download the files and run the file - no need to setup anything at all!

To download via Terminal:
```shell
git clone https://github.com/tsarjak/WallpapersFromReddit.git
```


### To run the code

In terminal:
```shell
# In the Home Directory or the Directory in which you cloned/downloaded the script
cd ~/WallpapersFromReddit
python main.py 
  --subreddit <your choice of subreddit> 
  --sort_type <hot|new|rising|top> 
  --sort_time <all|year|month|week|day>
  --update_every <Number of minutes after which you want to change the wallpapers>
  --run_for <Total number of hours you want to run the script for>
  --download_only <Toggle this to either only download the images, or to also keep cycling throught the wallpapers>
```

Example: 
```shell
python wallpaper.py --subreddit earthporn -sort_type top --sort_time all --download_only
```


### After First run, you might want to run the app in background (This is possible even on first run!)

```shell
nohup python main.py &
```
nohup command is used to keep the script running in background, even when the terminal is closed

### Add the script to run it as startup application

Goto "Startup Applications"
Click "Add" -> Click "Custom Command" -> Enter command as "nohup python ~/wallpaper.py &", enter name and other details and save
