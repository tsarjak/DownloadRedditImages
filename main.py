import argparse
import os
import random
import glob
from os import path as osp

from core import WallpaperDownloader


def main():

    args = parse_args()
    downloader = WallpaperDownloader(subreddit=args.subreddit,
                                     sort_time=args.sort_time,
                                     sort_by=args.sort_by)

    total_downloaded = downloader.download(max_count=args.max_download_count)

    print('Downloaded {} images from /r/{} sorted by {} for sort time {}'.format(total_downloaded,
                                                                                 args.subreddit,
                                                                                 args.sort_by,
                                                                                 args.sort_time))

    if args.download_only:
        return

    # Now setup wallpaper randomly from the wallpaper folder.
    preferences = downloader.preferences
    wallpapers = glob.glob(osp.join(preferences['wallpaper_dir'], '*.jpg'))
    random.shuffle(wallpapers)

    total_iters = int((args.run_for * 60) / args.update_every)

    assert total_iters >= 1, "See help for run_for and update_every"

    if total_iters >= len(wallpapers):
        to_extend = int(total_iters/len(wallpapers)) + 1
        wallpapers_copy = []
        for _ in range(to_extend):
            wallpapers_copy.extend(wallpapers.copy())
        wallpapers = wallpapers_copy

    for i in range(total_iters):
        if preferences['os_type'] == 'Linux':
            filepath = "gsettings set org.gnome.desktop.background picture-uri file:" + wallpapers[i]
        elif preferences['os_type'] == 'Darwin':
            filepath = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + \
                       wallpapers[i] + "\"'"
        else:
            raise NotImplementedError('Implemented only for Linux and Mac. ')

        os.system(filepath)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download images and set wallpaper from your choice of subreddit!')
    parser.add_argument('--subreddit', type=str, default='wallpaper',
                        help='Your choice of subreddit to download Images. Default is "wallpaper".')
    parser.add_argument('--sort_by', type=str, default='hot',
                        help='Select sort-by option. Default is "hot". Options: hot|new|rising|top')
    parser.add_argument('--sort_time', type=str, default='day',
                        help='Sort time for subreddit. Default is "day". Options: all|year|month|week|day')
    parser.add_argument('--max_download_count', type=int, default=20,
                        help='Maximum number of images to download. Default is 20.')
    parser.add_argument('--download_only', action='store_true', default=False,
                        help='Only download the photos. Skip setting up wallpaper.')
    parser.add_argument('--update_every', type=int, default=30,
                        help='Update the wallpaper after how many mins? Default is 30 mins.')
    parser.add_argument('--run_for', type=int, default=24,
                        help='How long you want to keep updating the wallpaper? Default ius 24 hours.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
