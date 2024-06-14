import os
from typing import Any, Dict, Tuple
import requests

from utils import check_if_empty_and_delete_file, construct_local_filename, get_gfycat_redgif_url, get_media_download_url

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

def download_post(args: Tuple[dict, str]) -> bool:
    post_details, download_dir = args
    domain = post_details.get('domain')
    media_url = post_details.get('url')
    post_title = post_details.get('title')

    if domain is None or media_url is None:
        return False

    media_url = get_media_download_url(media_url, domain)
    if not media_url:
        return False

    local_filename = construct_local_filename(title=post_title, download_url=media_url, local_download_dir=download_dir)
    if os.path.exists(local_filename):
        return False

    try:
        with requests.get(media_url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=26214400):
                    if chunk:
                        f.write(chunk)
        if check_if_empty_and_delete_file(local_filename):
            return False
        return True
    except Exception as e:
        print(f'Error downloading {media_url}: {e}')
        return False