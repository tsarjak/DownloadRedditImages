# Download Images/Media from your choice of Subreddit!

Using this script:
* **No Setup Needed!**
* **Download any number of images** from **Any Subreddit!**
* Select your sort type **(Top, Hot, New, Controversial)**
* Select your sort time **(All, Year, Month, Week, Day)**
* Extremely **Reliable Downloading.** With **progress bar showing ETA.**
* Download using **ParallelProcessing**
* Specify your **custom save location**
* Major reddit media servers supported **(i.redd.it, imgur, gfycat, redgif)**
* **If media server is unsupported, Download raw previews**
* (Optional) Install tqdm to see tqdm progress and time estimates. Without tqdm, native progress bar is printed to terminal output.


#### PS: Automatic wallpaper setting from downloaded images and support for python v2.x has been removed in latest update. Feature will be added back soon(~1 week). Please use the old version if you absolutely need that feature.

### No Dependencies! Just Download and Run!
Just download the files and run the file - no need to setup anything at all!

To download via Terminal:
```shell
git clone https://github.com/tsarjak/WallpapersFromReddit.git

# Next step is Fully Optional - to use tqdm progress bar. Without this, native progress bar will show up with exact same features, just a little less pretty.
pip install tqdm
```

### To run the code

In terminal:
```shell
# In the Home Directory or the Directory in which you cloned/downloaded the script
cd ~/DownloadRedditImages
python download.py 
  --subreddit <your choice of subreddit> 
  --sort_type <hot|new|rising|top> 
  --sort_time <all|year|month|week|day>
  --download_dir <Directory where you want to store the images. For Max/Linux, the script can identify home directory and sets a RedditMedia folder there. For Windows, a path MUST be provided>
  --max_post_downloads <Maximum number of posts media to download. Default=10>
  --max_simultaneous_downloads <Maximum number of simultaneous downloads to run using multiple CPU cores. Default=16.>
  --max_trials <Maximum number of trials to fetch subreddit data. Sometimes the response is slow and multiple attempts are needed. Default=20.>
```

## Example: 
```shell
python download.py --subreddit pics -sort_type top --sort_time all --max_post_downloads 40 --download_dir /Users/user_me/Pictures/RedditMedia/
# This will download top 50 posts of all time from earthporn subreddit to /Users/user_me/Pictures/RedditMedia folder.
```
Without tqdm installed:
<img width="741" alt="Screen Shot 2022-12-11 at 2 31 50 AM" src="https://user-images.githubusercontent.com/9898343/206898666-d9f95e4f-3bd1-4f37-9372-32f4009a434c.png">

With tqdm installed (optional):
<img width="944" alt="Screen Shot 2022-12-11 at 2 20 41 AM" src="https://user-images.githubusercontent.com/9898343/206898223-3872e046-a8d3-4199-b4da-00ed9a429005.png">

```

### Changelog: v2.1.0 vs v2.0.0:
* Added support for mp4 and gif downloads.
* Added support to download directly from media servers (imgur, i.redd.it, gfycat, redgifs) instead of reddit post previews.
* For other media servers, fallback to reddit post preview download.
* Added native progress bar. As well as tqdm progress bar for those who already have it installed on their systems.
* Removed support for automatic wallpaper changing for Linux and Mac. Support will be added back in v2.1.1.
* Removed support for python v2.x. Some requests/url libraries are difficult to maintain for python v2.x now.

#### Grab the previous release here! For wallpaper and python v2.x support.
DownloadRedditImages v2.0.0 - https://github.com/tsarjak/WallpapersFromReddit/releases/tag/v2.0.0
