from multiprocessing import Value
import time

try:
    from tqdm import tqdm
    TQDM_IMPORTED = True
except ImportError:
    TQDM_IMPORTED = False


class MultiProcessingCounter:
    
    global_counter = None
    tqdm_progress_bar = None
    total_count = None
    subreddit_name = None
    sort_by = None
    sort_time = None
    local_download_dir = None
    start_time = None
    
    @classmethod
    def init(cls, 
             total_count: int,
             subreddit_name: str,
             sort_by: str,
             sort_time: str,
             local_download_dir: str):
        """
        Initialize the said class. Setup tqdm and multiprocessing counter.
        """
        
        # MultiProcessing Counter
        cls.global_counter = Value('i', 0)
        cls.total_count = total_count
        cls.sort_by = sort_by
        cls.sort_time = sort_time
        cls.subreddit_name = subreddit_name
        cls.local_download_dir = local_download_dir
        cls.start_time = time.time()
        
        
        print(f'\nDownloading {MultiProcessingCounter.total_count} posts from /r/{MultiProcessingCounter.subreddit_name} '
              f'sorted by {MultiProcessingCounter.sort_by}|{MultiProcessingCounter.sort_time} to {MultiProcessingCounter.local_download_dir}/\n')
        
        if TQDM_IMPORTED:
            cls.tqdm_progress_bar = tqdm(total=total_count, desc=f'{subreddit_name}|{sort_by}|{sort_time}|n={total_count}')
        else:
            cls.tqdm_progress_bar = None
                
    @staticmethod
    def increment_counter(download_successful: bool):
        """
        Increment the counter and progress bar.
        """
        
        if download_successful:
            with MultiProcessingCounter.global_counter.get_lock():
                MultiProcessingCounter.global_counter.value += 1
                
                if TQDM_IMPORTED:
                    MultiProcessingCounter.tqdm_progress_bar.n = MultiProcessingCounter.global_counter.value
                    MultiProcessingCounter.tqdm_progress_bar.last_print_n = MultiProcessingCounter.global_counter.value
                    MultiProcessingCounter.tqdm_progress_bar.refresh()
                    
                else:
                    if MultiProcessingCounter.global_counter.value % 5 == 0:
                        print(f'Downloaded {MultiProcessingCounter.global_counter.value}/{MultiProcessingCounter.total_count} posts...')
                        
    
    @staticmethod
    def get_counter_value():
        with MultiProcessingCounter.global_counter.get_lock():
            counter_val = MultiProcessingCounter.global_counter.value
        
        return counter_val
    
    
    @staticmethod
    def close_counter():
        """
        Close the tqdm_progress_bar, and print final status.
        """
        if TQDM_IMPORTED:
            MultiProcessingCounter.tqdm_progress_bar.close()
        
        print(f'\nDownloaded {MultiProcessingCounter.global_counter.value}/{MultiProcessingCounter.total_count} posts '
                f'from /r/{MultiProcessingCounter.subreddit_name} sorted by {MultiProcessingCounter.sort_by}|{MultiProcessingCounter.sort_time} to {MultiProcessingCounter.local_download_dir}/ '
                f'in {(time.time() - MultiProcessingCounter.start_time):.2f} seconds')
