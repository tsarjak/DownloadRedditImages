import os
from typing import Any, Dict
from urllib.request import urlretrieve
import requests
from counter_and_status_bar import MultiProcessingCounterAndStatusBar

from utils import check_if_empty_and_delete_file, construct_local_filename, get_gfycat_redgif_url

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

class MediaDownloader:
    
    local_download_dir: str
    global_counter: MultiProcessingCounterAndStatusBar
    max_posts_download: int
    
    @classmethod
    def init(cls, 
             local_download_dir: str,
             global_counter: MultiProcessingCounterAndStatusBar,
             max_posts_download: int):
        """
        Setup the local download directory.
        :param local_download_dir: Path to the local download directory. All media files will be downloaded here.
        """
        cls.local_download_dir = local_download_dir
        cls.global_counter = global_counter
        cls.max_posts_download = max_posts_download
        os.makedirs(local_download_dir, exist_ok=True)
    
    @staticmethod
    def download_post(post_details: Dict[str, Any]):
        """
        Download the post from post details.
        """
        
        # If already downloaded max posts, then return.
        if MediaDownloader.global_counter.get_counter_value() >= MediaDownloader.max_posts_download:
            return
        
        domain = post_details.get('domain')
        media_url = post_details.get('url')
        post_title = post_details.get('title')
        
        # If domain or url is not available, return.
        if domain is None or media_url is None:
            return False
            
        media_download_helper = MediaDownloadHelper(media_url=media_url,
                                                    title=post_title,
                                                    local_download_dir=MediaDownloader.local_download_dir,
                                                    domain=domain,
                                                    post_details=post_details)
        download_successful = media_download_helper.download()
        MediaDownloader.global_counter.increment_counter(download_successful=download_successful)
        
    
    
class MediaDownloadHelper:
    
    def __init__(self, 
                 domain: str,
                 media_url: str,
                 title: str,
                 post_details: Dict[str, Any],
                 local_download_dir: str):
        """
        Initialize the said class with domain.
        Setup the correct call method to download.
        :param domain: Media domain from reddit post details.
        """
        self._local_download_dir = local_download_dir
        self._title = title
        self._media_url = media_url
        self._post_details = post_details
        self._domain = domain
        
    def download(self):
        """
        Download the media to disk.
        """
        domain_mappings = {
            'gfycat.com': self.gfycat,
            'i.imgur.com': self.imgur,
            'i.redd.it': self.ireddit,
            'redgifs.com': self.redgifs
        }
        local_filename = domain_mappings.get(self._domain, self.do_nothing)()
        download_successful = True if local_filename is not None else False
        
        # Try to download using correct media source.
        if download_successful:
            is_empty = check_if_empty_and_delete_file(file_path=local_filename)
            download_successful = False if is_empty else True
        
        # If unable to download from media source, download the preview from reddit page.
        if not download_successful:
            naive_local_filename = self._attempt_naive_preview_download()
            naive_download_successful = True if naive_local_filename is not None else False
            
            if naive_download_successful:
                naive_is_empty = check_if_empty_and_delete_file(file_path=naive_local_filename)
                naive_download_successful = False if naive_is_empty else True
                
        download_successful = download_successful or naive_download_successful
        return download_successful
    
    def do_nothing(self):
        """
        As the name suggests, do nothing. Return False as no download is happening.
        """
        return None
    
    def gfycat(self):
        """
        Download from source gfycat.com.
        """
        gfycat_url = get_gfycat_redgif_url(media_url=self._media_url, domain_type='gfycat')
        
        local_filename = None
        if gfycat_url is not None:
            local_filename = self._download_to_local_file(download_url=gfycat_url)
        
        return local_filename
    
    def imgur(self):
        """
        Download from source i.imgur.com.
        """
        if 'gifv' in self._media_url:
            self._media_url = self._media_url.replace('.gifv', '.mp4')
        
        local_filename = self._download_to_local_file(download_url=self._media_url)
        return local_filename
        
    def ireddit(self):
        """
        Download from source i.redd.it.
        """
        local_filename = self._download_to_local_file(download_url=self._media_url)
        return local_filename
    
    def redgifs(self):
        """
        Download from source redgifs.com.
        """
        redgif_url = get_gfycat_redgif_url(media_url=self._media_url, domain_type='redgif')
        
        local_filename = None
        if redgif_url is not None:
            local_filename = self._download_to_local_file(download_url=redgif_url)
            
        return local_filename
    
 
    
    def _download_to_local_file(self,
                                download_url: str):
        """
        Perform simple download from download url.
        :param download_url: Download URL.
        """
        local_filename = construct_local_filename(title=self._title,
                                                  download_url=download_url,
                                                  local_download_dir=self._local_download_dir)
        
        try:
            self._core_download(download_url=download_url, local_filename=local_filename)
            return local_filename
        except:
            return None
        
    def _attempt_naive_preview_download(self):
        """
        Attempt to naively download the post preview.
        """
        if 'preview' not in self._post_details:
            return None
        
        # Get the information about the image.
        preview_url = self._post_details['preview']['images'][0]['source']['url']
        local_filename = construct_local_filename(title=self._title,
                                                    file_suffix='.jpg',
                                                    local_download_dir=self._local_download_dir)
        
        self._core_download(download_url=preview_url, local_filename=local_filename)
        return local_filename
        
    def _core_download(self, download_url: str, local_filename: str):
        
        # If already exists locally, then just skip the download.
        if os.path.exists(local_filename):
            return
        
        # Actually downloading the media.
        with requests.get(download_url, stream=True) as r:
            with open('{}'.format(local_filename), 'wb') as f:
                for chunk in r.iter_content(chunk_size=26214400):
                    if chunk:
                        f.write(chunk)
