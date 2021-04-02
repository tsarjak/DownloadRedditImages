import os
from typing import Dict

import requests

from utils import Utils
from os import path as osp


class WallpaperDownloader:
    """
    Core class to download images from Reddit.
    """

    def __init__(self,
                 subreddit: str = 'wallpaper',
                 sort_by: str = 'top',
                 sort_time: str = 'all'):
        """
        Initialize the preference and link to subreddit.
        :param subreddit: Name of the subreddit.
        :param sort_by: Sort by? Hot/Top/New/Controversial.
        :param sort_time: Sort time. day/week/month/year/all
        """
        self._url = 'https://www.reddit.com/r/{}/{}/.json?raw_json=1&t={}'.format(subreddit,
                                                                                  sort_by,
                                                                                  sort_time)
        self._preferences_file = 'wp_preferences.json'
        self._preferences = self._setup_preferences()

    @property
    def preferences(self) -> Dict:
        """
        Get the preferences.
        :return: Preferences Dict.
        """
        return Utils.load_preferences(self._preferences_file)

    def download(self, max_count: int = 50):
        """
        This is where all the downloading takes place.
        :param max_count: Maximum number of images to download.
        :return: num_downloaded: Number of downloaded images.
        """

        # Update URL to fetch entries based on max_count.
        self._url += '&limit={}'.format(
            max_count * 10)  # There are a lot of unwanted images, so setting it to high value.

        # Fetch the JSON file for subreddit here.
        subreddit_data = Utils.fetch_subreddit_data(subreddit_url=self._url)

        # If we can't get subreddit data even after 20 trials, we close the program. Try later.
        if subreddit_data is None:
            print('Unable to connect to reddit. Check internet connection. Or try later.')
            return

        count = 0
        saved_images = []

        for content in subreddit_data['data']['children']:

            if content['data'].get('post_hint', 'none') == 'image' and 'preview' in content['data']:
                # Get the information about the image.
                image_url = content['data']['preview']['images'][0]['source']['url']
                image_title = content['data']['title'][:15]
                image_id = content['data']['id']

                # Set image save name
                img_save_name = '{}_{}.jpg'.format(image_title, image_id)
                img_save_name = osp.join(self._preferences['wallpaper_dir'], img_save_name)

                # If we have already downloaded the image, we can skip.
                if osp.exists(img_save_name):
                    continue

                # Actually downloading the image.
                with requests.get(image_url, stream=True) as r:
                    r.raise_for_status()
                    with open('{}'.format(img_save_name), 'wb') as f:
                        for chunk in r.iter_content(chunk_size=26214400):
                            if chunk:
                                f.write(chunk)

                saved_images.append(img_save_name)

                # Update the preferences.
                self._preferences['urls'][image_id] = {'title': image_title,
                                                       'url': image_url}
                Utils.save_to_preferences(self._preferences, self._preferences_file)

                count += 1

            # Done downloading, so remove unwanted images and return the total number of saved images.
            if count >= max_count:
                count_removed = Utils.remove_unwanted_images(saved_images)
                return len(saved_images) - count_removed

    def _setup_preferences(self) -> Dict:
        """
        Setup the preferences for downloading. Find the machine type etc if its running for the first time.
        :return: preferences - Loaded preferences.
        """
        # Load the preferences file.
        preferences = Utils.load_preferences(self._preferences_file) if osp.exists(self._preferences_file) else {}

        # If it's empty (running for the first time), we set it up manually.
        if preferences == {}:
            os_type, wallpaper_dir = Utils.get_os()

            # If wallpapers directory is not there, we create it.
            if not osp.exists(wallpaper_dir):
                os.makedirs(wallpaper_dir)

            preferences['os_type'] = os_type
            preferences['wallpaper_dir'] = wallpaper_dir
            preferences['urls'] = dict()

        # Just save preferences back to file in case of update.
        Utils.save_to_preferences(preferences, self._preferences_file)

        return preferences
