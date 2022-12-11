import json
import time
import urllib.request as request
from typing import Dict

from utils import verify_sort_options


class RedditStateHandler:
    
    def __init__(self, 
                 subreddit: str,
                 sort_time: str,
                 sort_by: str,
                 max_trials: int = 20):
        """
        Initialize the said class.
        :param subreddit: Name of the subreddit.
        :param sort_time: Sort time.
        :param sort_by: Sort by.
        :param max_trials: Maximum number of trials to fetch subreddit data.
        """
        
        verify_sort_options(sort_time=sort_time, sort_by=sort_by)
        
        self._subreddit = subreddit
        self._sort_time = sort_time
        self._sort_by = sort_by
        self._max_trials = max_trials
        
        self._core_url = f'https://www.reddit.com/r/{self._subreddit}/{self._sort_by}.json?raw_json=1&t={self._sort_time}'
        self._current_url = self._core_url
        
    @property
    def webpage_as_json(self) -> Dict:
        """
        Return the current reddit webpage as JSON dict.
        """
        subreddit_data = {'data': {'children': None}}        
        for _ in range(self._max_trials):
            try:
                subreddit_page = request.urlopen(self.current_url)
                subreddit_data = json.load(subreddit_page)
                break
            except:
                time.sleep(2)  # If we cannot access the reddit page, we wait for 2 seconds and retry.

        return subreddit_data
    
    @property
    def current_url(self) -> str:
        """Return the current reddit URL."""
        return self._current_url
    
    def try_to_goto_next_page(self) -> bool:
        """Go to the next page. Return True if next page was reached, else False."""
        web_data = self.webpage_as_json
        
        next_page_info = web_data.get('data').get('after')
        if next_page_info is not None:
            self._current_url = f'{self._core_url}&after={next_page_info}'
            return True
        else:
            return False