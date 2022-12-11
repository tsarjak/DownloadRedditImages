from multiprocessing import Value
import time

try:
    from tqdm import tqdm
    TQDM_IMPORTED = True
except ImportError:
    TQDM_IMPORTED = False


class MultiProcessingCounterAndStatusBar:
    """Class to handle Counter and Status/Progress bar for multiprocessing."""
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
        
        # Other params for status bar.
        cls.total_count = total_count
        cls.sort_by = sort_by
        cls.sort_time = sort_time
        cls.subreddit_name = subreddit_name
        cls.local_download_dir = local_download_dir
        cls.start_time = time.time()
        
        # Print initial information.
        print(f'\nDownloading {MultiProcessingCounterAndStatusBar.total_count} posts from /r/{MultiProcessingCounterAndStatusBar.subreddit_name} '
              f'sorted by {MultiProcessingCounterAndStatusBar.sort_by}|{MultiProcessingCounterAndStatusBar.sort_time} to {MultiProcessingCounterAndStatusBar.local_download_dir}/\n')
        
        # Initialize tqdm if imported.
        if TQDM_IMPORTED:
            cls.tqdm_progress_bar = tqdm(total=total_count, desc=f'{subreddit_name}|{sort_by}|{sort_time}|n={total_count}')
        else:
            cls.tqdm_progress_bar = None
                
    @staticmethod
    def increment_counter(download_successful: bool):
        """
        Increment the counter and progress bar.
        :param download_successful: bool containing whether download was successful.
        """
        if download_successful:
            with MultiProcessingCounterAndStatusBar.global_counter.get_lock():
                MultiProcessingCounterAndStatusBar.global_counter.value += 1
                
                if TQDM_IMPORTED:
                    MultiProcessingCounterAndStatusBar.tqdm_progress_bar.n = MultiProcessingCounterAndStatusBar.global_counter.value
                    MultiProcessingCounterAndStatusBar.tqdm_progress_bar.last_print_n = MultiProcessingCounterAndStatusBar.global_counter.value
                    MultiProcessingCounterAndStatusBar.tqdm_progress_bar.refresh()
                    
                else:
                    if MultiProcessingCounterAndStatusBar.global_counter.value % 5 == 0:
                        time_completed = time.time() - MultiProcessingCounterAndStatusBar.start_time
                        current_count_value = MultiProcessingCounterAndStatusBar.global_counter.value
                        total_count_value = MultiProcessingCounterAndStatusBar.total_count
                        total_expected_time = (total_count_value * time_completed) / current_count_value
                        print(f'Downloaded {current_count_value}/{total_count_value} posts '
                              f'in {time_completed:.2f} seconds. ETA {total_expected_time - time_completed:.2f} seconds.')
                        
    
    @staticmethod
    def get_counter_value():
        with MultiProcessingCounterAndStatusBar.global_counter.get_lock():
            counter_val = MultiProcessingCounterAndStatusBar.global_counter.value
        
        return counter_val
    
    
    @staticmethod
    def close_counter():
        """
        Close the tqdm_progress_bar, and print final status.
        """
        if TQDM_IMPORTED:
            MultiProcessingCounterAndStatusBar.tqdm_progress_bar.close()
        
        print(f'\nDownloaded {MultiProcessingCounterAndStatusBar.global_counter.value}/{MultiProcessingCounterAndStatusBar.total_count} posts '
                f'from /r/{MultiProcessingCounterAndStatusBar.subreddit_name} sorted by {MultiProcessingCounterAndStatusBar.sort_by}|{MultiProcessingCounterAndStatusBar.sort_time} to {MultiProcessingCounterAndStatusBar.local_download_dir}/ '
                f'in {(time.time() - MultiProcessingCounterAndStatusBar.start_time):.2f} seconds')
