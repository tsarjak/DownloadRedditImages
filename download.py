from multiprocessing import Pool
import os
import time
from counter_and_status_bar import MultiProcessingCounterAndStatusBar
from downloaders import MediaDownloader
import fire
from utils import check_max_simultaneous_downloads, get_default_download_dir

from web_handler import RedditStateHandler
    
    
def start_download(subreddit: str,
                   sort_time: str,
                   sort_by: str,
                   download_dir: str = None,
                   max_post_downloads: int = 10,
                   max_trials: int = 20,
                   max_simultaneous_downloads: int = 16,
                   ):
    """
    Initialize the said class.
    :param subreddit: Name of the subreddit.
    :param sort_time: Sort time - oneOf(all, year, month, week, day).
    :param sort_by: Sort by - oneOf(top, hot, rising, new).
    :param download_dir: Path to the download directory. All files will be downloaded here.
    :param max_post_downloads: Maximum number of posts to download. Default 10.
    :param max_trials: Maximum number of trials to fetch subreddit data. Default 20.
    :param max_simultaneous_downloads: Maximum number of simultaneous downloads. Default 16.
    """
    # If download directory is not specified, setup the default directory.
    download_dir = get_default_download_dir() if download_dir is None else download_dir
    
    # Set download dir to subreddit name inside provided download dir.
    download_dir = os.path.join(download_dir, subreddit)
    
    # Check max_simultaneous_downloads
    max_simultaneous_downloads = check_max_simultaneous_downloads(max_simultaneous_downloads)
    
    # Setup web handler for reddit.
    reddit_state_handler = RedditStateHandler(subreddit=subreddit,
                                              sort_by=sort_by,
                                              sort_time=sort_time,
                                              max_trials=max_trials)
    
    # Initialize the multiprocessing counter.
    MultiProcessingCounterAndStatusBar.init(total_count=max_post_downloads,
                                subreddit_name=subreddit,
                                sort_by=sort_by,
                                sort_time=sort_time,
                                local_download_dir=download_dir)
    
    # Loop till we reach max_post_downloads.
    while MultiProcessingCounterAndStatusBar.global_counter.value < max_post_downloads:
        # Get subreddit as json.
        subreddit_data = reddit_state_handler.webpage_as_json
        
        posts_info = subreddit_data.get('data', {}).get('children', None)
        if posts_info is None:
            print(f'Unable to find posts for {subreddit}. Please try again! :(')
            return
        
        # Initialize the media downloader.
        MediaDownloader.init(local_download_dir=download_dir,
                             global_counter=MultiProcessingCounterAndStatusBar,
                             max_posts_download=max_post_downloads)
        
        # Setup page post data and download using multiprocessing.
        posts_data = [content['data'] for content in subreddit_data['data']['children']]
        chunk_size = min(64, int(max_post_downloads/max_simultaneous_downloads))
        with Pool(max_simultaneous_downloads) as multi_processor:
            multi_processor.map(MediaDownloader.download_post, posts_data, chunksize=chunk_size)
        
        # Go to next page if all posts on current page are exhausted and we are still running.
        next_page_available = reddit_state_handler.try_to_goto_next_page()    
        if not next_page_available:
            break
    
    MultiProcessingCounterAndStatusBar.close_counter()
        
    
if __name__ == '__main__':
    fire.Fire(start_download)