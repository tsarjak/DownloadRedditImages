import os
import platform
import pwd
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
    """
    Check if the given file is empty (smaller than allowed size of 10kb), then delete it, and return flag.
    """
    try:
        is_empty_file = os.path.getsize(file_path) < allowed_size
        
        if is_empty_file:
            os.remove(file_path)
            
    except:
        is_empty_file = True
    
    return is_empty_file
    
    
    
def get_gfycat_redgif_url(media_url: str,
                          domain_type: str) -> str:
    """
    Get URL for gfycat mp4 from gfycat name.
    :param media_url: Media URL.
    :param domain_type: oneOf(gfycat, redgif).
    :return: URL for the final download link for gfycat or redgifs.
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
    if max_simultaneous_downloads >= 4 * os.cpu_count():
        print(f'max_simultaneous_downloads too high: {max_simultaneous_downloads}. '
              f'Max CPU count available: {os.cpu_count()}. '
              f'Setting max_simultaneous_downloads to {(4 * os.cpu_count()) - 2}')
        max_simultaneous_downloads = (4 * os.cpu_count()) - 2
        
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


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()
        

def get_media_download_url(media_url: str, domain: str) -> str:
    try:
        if domain == 'gfycat.com':
            return get_gfycat_redgif_url(media_url, 'gfycat')
        elif domain == 'redgifs.com':
            return get_gfycat_redgif_url(media_url, 'redgif')
        elif domain == 'i.redd.it' or domain == 'i.imgur.com':
            return media_url
        return None
    except:
        print('Error fetching media url')
        return None