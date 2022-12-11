import os
import platform
import pwd
from typing import Any, Dict
import requests

VALID_SORT_TIME_OPTIONS = ['all', 'year', 'month', 'week', 'day']
VALID_SORT_BY_OPTIONS = ['hot' , 'new', 'rising', 'top']
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

def verify_sort_options(sort_time: str, sort_by: str) -> None:
    """
    Verify the sort options provided by user.
    :param sort_time: sort_time param provided by user.
    :param sort_by: sort_by param provided by user.
    """
    assert sort_by in VALID_SORT_BY_OPTIONS, f'Incorrect sort_time {sort_by}. Valid options: {VALID_SORT_BY_OPTIONS}'
    assert sort_time in VALID_SORT_TIME_OPTIONS, f'Incorrect sort_time {sort_time}. Valid options: {VALID_SORT_TIME_OPTIONS}'
    
    
def check_if_empty_and_delete_file(file_path, allowed_size: int = 10240) -> bool:
    
    is_empty_file = os.path.getsize(file_path) < allowed_size
    
    if is_empty_file:
        os.remove(file_path)
        
    return is_empty_file
    
    
def get_gfycat_redgif_url(media_url: str,
                          domain_type: str):
    """
    Get URL for gfycat mp4 from gfycat name.
    :param media_url: Media URL.
    :param domain_type: oneOf(gfycat, redgif).
    """
    media_name = media_url.split('/')[-1]
    data = None
    
    if domain_type == 'gfycat':
        data = requests.get(f'https://gfycat.com/cajax/get/{media_name}', 
                            headers=HEADERS)
    
    elif domain_type == 'redgif':
        data = requests.get(f'https://api.redgifs.com/v1/gfycats/{media_name}',
                            headers=HEADERS)
    
    if data is not None and data.status_code == 200:
        json_data = data.json()
        return json_data['gfyItem']['mp4Url']
    else:
        return None
    

def construct_local_filename(title: str, 
                             local_download_dir: str,
                             download_url: str = None,
                             file_suffix: str = None):
    """
    Construct the local filename.
    """
    assert file_suffix is not None or download_url is not None
    
    # Replace '/' in title to avoid issues with file system.
    title = title.replace('/', '-')
    
    # Ensure title isn't too long, to avoid OSError: File name too long.
    title = title[:150]
    
    if file_suffix is None:
        file_suffix = os.path.splitext(download_url)[1]
        
    return os.path.join(local_download_dir, f'{title}.{file_suffix}')


def check_max_simultaneous_downloads(max_simultaneous_downloads: int):
    """
    Check if max_simultaneous_downloads are greater than CPU count on machine. 
    If so, correct it and return the correct value.
    """
    if max_simultaneous_downloads >= os.cpu_count() - 2:
        print(f'max_simultaneous_downloads too high: {max_simultaneous_downloads}. '
              f'Max CPU count available: {os.cpu_count()}. '
              f'Setting max_simultaneous_downloads to {os.cpu_count() - 2}')
        max_simultaneous_downloads = os.cpu_count() - 2
        
    return max_simultaneous_downloads
    

def get_default_download_dir():
    """
    Get default download directory for linux/mac.
    """
    os_type = platform.system()
    assert os_type in {'Darwin', 'Linux'}, "If you are using windows, please provide download_dir." \
                                           "Automatic setup to home directory is supported on Linux and Mac only."
    
    username = pwd.getpwuid(os.getuid()).pw_name
    default_dir = f'/Users/{username}/Pictures/RedditMedia/' if os_type == 'Darwin' else f'/home/{username}/RedditMedia/'

    return default_dir