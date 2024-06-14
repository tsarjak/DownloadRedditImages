from multiprocessing import Pool
import os
import fire
from downloaders import download_post
from utils import check_max_simultaneous_downloads, get_default_download_dir, print_progress_bar
from web_handler import RedditStateHandler

try:
    from tqdm import tqdm
    tqdm_installed = True
except ImportError:
    tqdm_installed = False



def start_download(subreddit: str,
                   sort_time: str,
                   sort_by: str,
                   download_dir: str = None,
                   max_post_downloads: int = 10,
                   max_trials: int = 20,
                   max_simultaneous_downloads: int = 16,
                   ):
    """
    Start downloading images from a specified subreddit.
    :param subreddit: The name of the subreddit to download images from.
    :param sort_time: The time period to sort posts by (e.g., 'day', 'week', 'month', 'year', 'all').
    :param sort_by: The criterion to sort posts by (e.g., 'top', 'new', 'hot').
    :param download_dir: The directory where images will be downloaded. Defaults to None, which means the default download directory will be used.
    :param max_post_downloads: The maximum number of posts to download images from. Defaults to 10.
    :param max_trials: The maximum number of trials to attempt downloading before stopping. Defaults to 20.
    :param max_simultaneous_downloads: The maximum number of simultaneous downloads. Defaults to 16.
    """
    download_dir = get_default_download_dir() if download_dir is None else download_dir
    download_dir = os.path.join(download_dir, subreddit)
    max_simultaneous_downloads = check_max_simultaneous_downloads(max_simultaneous_downloads)
    os.makedirs(download_dir, exist_ok=True)
    
    reddit_state_handler = RedditStateHandler(subreddit=subreddit,
                                              sort_by=sort_by,
                                              sort_time=sort_time,
                                              max_trials=max_trials)

    if tqdm_installed:
        pbar = tqdm(total=max_post_downloads, desc=f'Downloading posts from /r/{subreddit}')
    
    downloaded_posts = 0
    if not tqdm_installed:
        print_progress_bar(downloaded_posts, max_post_downloads, prefix='Progress:', suffix='Complete', length=50)

    while downloaded_posts < max_post_downloads:
        subreddit_data = reddit_state_handler.webpage_as_json
        posts_data = [content['data'] for content in subreddit_data['data']['children']]
        if not posts_data:
            print(f'Unable to find posts for {subreddit}. Please try again! :(')
            return
        
        with Pool(max_simultaneous_downloads) as pool:
            results = pool.map(download_post, [(post, download_dir) for post in posts_data])
            new_downloads = sum(results)
            downloaded_posts += new_downloads
            if tqdm_installed:
                pbar.update(new_downloads)
            else:
                print_progress_bar(downloaded_posts, max_post_downloads, prefix='Progress:', suffix='Complete', length=50)
            if downloaded_posts >= max_post_downloads:
                break
        
        if not reddit_state_handler.try_to_goto_next_page():
            break
    
    if tqdm_installed:
        pbar.close()
    
    print(f'Downloaded {downloaded_posts} posts from /r/{subreddit}')

if __name__ == '__main__':
    fire.Fire(start_download)
