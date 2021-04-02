import json
import os
import platform
import pwd
import time
from typing import List, Dict
from os import path as osp

try:
    import urllib.request as urllib2  # For Python 3.x
except ImportError:
    import urllib2  # For Python 2.x


class Utils:
    """
    Bunch of utils used for the Reddit Downloader.
    """

    @staticmethod
    def save_to_preferences(preferences: Dict[str, Dict], preferences_file: str):
        """
        Save the preferences to a JSON file.
        :param preferences: Dict containing preferences to save to file.
        :param preferences_file: Location of the file where you want to save.
        """
        with open(preferences_file, 'w') as f:
            json.dump(preferences, f)

    @staticmethod
    def load_preferences(preferences_file: str) -> Dict[str, Dict]:
        """
        Load the preferences from JSON file and return as Dict.
        :param preferences_file: Location of the file containing the preferences.
        :return: preferences - Dict containing preferences to save to file.
        """
        with open(preferences_file, 'r') as f:
            preferences = json.load(f)

        return preferences

    @staticmethod
    def get_os():
        """
        Get the OS type (Linux or Macbook), and set the wallpaper folder accordingly.
        :return:
            os_type: Type of OS (Linux for Linux, Darwin for Mac).
            wallpapers_directory: Directory where the wallpapers will be saved.
        """
        os_type = platform.system()
        assert os_type in {'Darwin', 'Linux'}

        # Get the username
        username = pwd.getpwuid(os.getuid()).pw_name

        # Set the directory to download images.
        wallpapers_directory = '/Users/{}/Pictures/Wallpapers/'.format(username) if os_type == 'Darwin' \
            else '/home/{}/Wallpapers/'.format(username)

        return platform.system(), wallpapers_directory

    @staticmethod
    def remove_unwanted_images(images: List[str]):
        """
        Remove unwanted images. Since this is a naive approach, we might end up downloading some unwanted images, so we
        delete them.
        :param images: List of image file locations to filter and remove unwanted images from.
        """
        count_removed = 0
        for image in images:
            # These are some random html pages that might have been downloaded.
            # This is a fairly quick and naive approach to downloading images from reddit.
            if osp.getsize(image) < 102400:
                os.remove(image)
                count_removed += 1
        return count_removed

    @staticmethod
    def fetch_subreddit_data(subreddit_url: str, max_trials: int = 20) -> Dict:
        """
        Fetch the subreddit JSON page based on the URL.
        :param subreddit_url: URL created based on user inputs (subreddit, sort_type, sort_time, max_download_count).
        :param max_trials: Maximum number of trial to use for fetching the subreddit JSON data.
        :return: subreddit_data - Nested Dict containing Subreddit data for query.
        """

        subreddit_data = None
        for _ in range(max_trials):
            try:
                subreddit_page = urllib2.urlopen(subreddit_url)
                subreddit_data = json.load(subreddit_page)
                break
            except:
                time.sleep(2)  # If we cannot access the reddit page, we wait for 2 seconds and retry.

        return subreddit_data
