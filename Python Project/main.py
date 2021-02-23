# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import json
import youtube_dl
import os
import sys, getopt

# Public variable
index_file_name = "index.json"
default_song_folder = "downloadedSongs"

# Helper
# hook for Progress-viewing. Not used at the moment
def my_hook(d):
    if d['status'] == 'finished':
        print('Finished step')

# Just create Console-Output
def output(metadata):
    if metadata.get("_type", None) == "playlist":
        # Some console output
        for info in metadata['entries']:
            video_url = info.get("url", None)
            video_id = info.get("id", None)
            video_title = info.get("title", None)
            print(f"Title: {video_title}, URL: {video_url}, id: {video_id}")
            print(info)
    else:
        video_url = metadata.get("url", None)
        video_id = metadata.get("id", None)
        video_title = metadata.get("title", None)
        print(f"Title: {video_title}, URL: {video_url}, id: {video_id}")

# Creates json to output
def create_json(metadata):
    # playlist-tags
    data = {'pl_title': metadata.get("title", None),
            'pl_id': metadata.get("id", None),
            'pl_url': metadata.get("webpage_url", None),
            'songs': []}
    # song-tags for each song
    for song in metadata['entries']:
        data['songs'].append({
            'title': song.get("title", None),
            'file': f'{song.get("title", None)}.{song.get("ext", None)}',
            'id': song.get("id", None),
            'url': song.get("webpage_url", None)
        })

    return data
# End Helper


# Method: get all items of Playlist as Object (not downloaded) or get Song-Info
def get_song_or_playlist(param_playlist):
    ydl_opts = {
        'format': 'bestaudio/best',
    }
    # Getting Playlists, but only parse items / nod downloading
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:  # ToDo try catch if Playlist ist private / not existent
        return ydl.extract_info(param_playlist, download=False)

# Actually download array of songs into folder
def download_songs(urls, output_folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'progress_hooks': [my_hook],
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url_list=urls)

# Delete array of songs
def delete_songs(songs_to_delete, output_folder):
    for song_to_delete in songs_to_delete:
        os.remove(f'{output_folder}/{song_to_delete["file"]}')

# Compare download-List with Metadata; returns: songs_to_download: array of direct URLS to songs, songs_to_delete: array of song_of_index
def compare_with_index(metadata, index_file):
    # Create empty songs_to_download and songs_to_delete array
    songs_to_download = []
    songs_to_delete = []
    # If exists, parse json and find out songs_to_download to parse and write new content in file
    # Open index-file
    with open(index_file) as json_file:
        index_object = json.load(json_file)
        # Check for each song in metadata if it exists
        for song_of_metadata in metadata['entries']:
            if next((song_of_index for song_of_index in index_object['songs'] if song_of_index['id'] == song_of_metadata.get('id', None)), None) \
                    is None:
                # And add it to songs_to_download
                songs_to_download.append(song_of_metadata.get('webpage_url', None))
        # Check for each song in index-file if it exists in metadata
        for songs_of_index in index_object['songs']:
            if next((songs_of_metadata for songs_of_metadata in metadata['entries'] if songs_of_metadata.get('id', None) == songs_of_index['id']), None) \
                    is None:
                # And add it to songs_to_download
                songs_to_delete.append(songs_of_index)


    print(f'Songs to download: {songs_to_download}, Songs to delete: {songs_to_delete}')
    return songs_to_download, songs_to_delete

# do main functions
def compare_and_download(url:str, p_output_dir:str=None, p_index_file_path:str=None):
    # get song or playlist
    meta = get_song_or_playlist(param_playlist=url)
    # do some console-output
    output(metadata=meta)
    # Create empty arrays to store values in it
    songs_to_download = []
    songs_to_delete = []

    # check which type is given
    if meta.get("_type", None) == "playlist":

        # normalise path only of output-dir is set
        if p_output_dir:
            p_output_dir = os.path.normpath(p_output_dir)
            folder_name = f'{p_output_dir}/{meta.get("title", None)}'
        else:
            folder_name = meta.get("title", None)
        # Add playlist to songs_to_download and songs_to_delete if needed


        # Check if p_index_file_path is given, else set it to default
        index_file_path=os.path.normpath(p_index_file_path) if p_index_file_path else f'{folder_name}/{index_file_name}'

        # Find out if index-file exists
        if os.path.exists(index_file_path):
            songs = compare_with_index(metadata=meta, index_file=index_file_path)
            songs_to_download = songs[0]
            songs_to_delete = songs[1]
        else:
            # If not exists...
            # Generate JSON

            # Check if parent-directory exists
            if not os.path.exists(folder_name):
                # Create it if not
                os.makedirs(folder_name)
            # then download all
            for song in meta['entries']:
                songs_to_download.append(song.get("webpage_url", None))

        # Rewrite index-file
        index_object = create_json(metadata=meta)
        print(f'JSON: {index_object}')
        with open(index_file_path, 'w') as outfile:
            json.dump(index_object, outfile)

    else:
        # Add single song to songs_to_download
        folder_name = default_song_folder
        songs_to_download.append(meta.get("webpage_url", None))

    download_songs(urls=songs_to_download, output_folder=folder_name)
    delete_songs(songs_to_delete=songs_to_delete, output_folder=folder_name)

# main and get arguments
def main(argv):
   # special handling for first argument (URL), but show help if is first argument
   if argv[0] == "-h":
       print('autoYoutubeUpdater.py <pl_url/song_url> [-o <output_folder> -i <index_file]')
       sys.exit()
   if not argv[0] or argv[0].startswith('-'):
       sys.exit('Missing URL. Usage: autoYoutubeUpdater.py <pl_url/song_url> [-o <output_folder> -i <index_file]')

   # setting empty values
   offline_index_file = None
   output_folder = None

   # setting URL
   song_or_playlist_url = argv[0]

   # try getting other arguments
   try:
      opts, args = getopt.getopt(argv[1:],"hi:o:",["index_file=","output_folder="])
   except getopt.GetoptError:
      print('autoYoutubeUpdater.py <pl_url/song_url> [-o <output_folder> -i <index_file]')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('autoYoutubeUpdater.py <pl_url/song_url> [-o <output_folder> -i <index_file]')
         sys.exit()
      elif opt in ("-i", "--index_file"):
         offline_index_file = arg
      elif opt in ("-o", "--output_folder"):
         output_folder = arg
   print('Index file is "', offline_index_file)
   print('Output folder is "', output_folder)
   print('Song  folder is "', song_or_playlist_url)
   compare_and_download(url=song_or_playlist_url, p_output_dir=output_folder, p_index_file_path=offline_index_file)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])