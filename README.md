# YouTube Auto Download

[TOC]

# Youtube-DL

1. Youtube-DL installieren:

```powershell
pip install youtube-dl
```

2. Playlist / Video downloaden

```
yotube-dl <link to Playlist>
```

Nützliche Argumente:

- `--flat-playlist ` Do not extract the videos of a playlist, only list them.

- `-x / --extract-audio ` Convert video files to audio-only files (requires ffmpeg/avconv and ffprobe/avprobe)

- `--audio-format FORMAT ` Specify audio format: "best", "aac", "flac", "mp3", "m4a", "opus", "vorbis",or "wav"; "best" by default; No effect without -x

- `--audio-quality QUALITY`  Specify ffmpeg/avconv audio quality, insert a value between 0 (better) and 9 (worse) for VBR or a specific bitrate like 128K (default 5)

- `--embed-thumbnail` Embed thumbnail in the audio as cover art

- `--add-metadata` Write metadata to the video file

- `--metadata-from-title FORMAT` Parse additional metadata like song title / artist from the video title. The format syntax is the same as --output. Regular expression with named capture groups may also be used. The parsed parameters replace existing values. Example: `--metadata-from-title "%(artist)s - %(title)s"` matches a title like "Coldplay - Paradise". Example (regex): `--metadata-from-title "(?P<artist>.+?) - (?P<title>.+)"`

- `--exec CMD` Execute a command on the file after downloading and post-processing, similar to find's -exec syntax. Example: --exec 'adb push {} /sdcard/Music/ && rm {}'

- `--convert-subs FORMAT` Convert the subtitles to other format (currently supported: srt|ass|vtt|lrc)

- `--match-filter FILTER` Generic video filter. Specify any key (see the "OUTPUT TEMPLATE" for a list of available keys) to match if the key is present, !key to check if the key is not present, key > NUMBER (like "comment_count > 12", also works with  >=, <, <=, !=, =) to compare against a number, key = 'LITERAL' (like "uploader = 'Mike Smith'", also works with !=) to match against a string literal and & to require multiple matches. Values which are not known are excluded unless you put a question mark (?) after the operator. For example, to only match videos that have been liked more than 100 times and disliked less than 50 times (or the dislike functionality is not available at the given service), but who also have a description, use `--match-filter "like_count > 100 & dislike_count <? 50 & description"`

- `--match-title REGEX` Download only matching titles (regex or caseless sub-string)
- `--reject-title REGEX` Skip download for matching titles (regex or caseless sub-string)

More on the official [GitHub - ytdl-org/youtube-dl: Command-line program to download videos from YouTube.com and other video sites](https://github.com/ytdl-org/youtube-dl) -page



### Eine Liste der Lieder in einer Playlist:

```
youtube-dl -j --flat-playlist 'https://www.youtube.com/playlist?list=<pl>' >> output.json
```

## Konvertieren

YoutubeDL konvertiert mit ffpmpeg, was wir direkt unter Windows angeben können ([Download FFmpeg](https://www.ffmpeg.org/download.html#build-windows)): 

```powershell
youtube-dl -f bestaudio LinkToVideoOrPlaylistHere -o /Download/%(title)s.%(ext)s --ffmpeg-location %CD%\ffmpeg\bin
```

oder unter linux installieren können:

```bash
sudo apt-get install ffmpeg
```

## Playlists abgleichen

1. Offline alles löschen, was online nicht existiert
2. Online alles Löschen, was Offline existiert
3. Index Updaten
4. Rest Downloaden

### Beispiel

![Beispiel](C:\Users\Benedikt\Projekte\YoutubeAPI2\Beispiel.svg)

Song 3 Löschen, Song 5 Runterladen und Online zu neuem Offline-Index machen.

entries
id
title
uploader
uploader_id
uploader_url
extractor
webpage_url
webpage_url_basename
extractor_key

# Python Programm

## Downloader und Converter (mit Picard?)

### Usage:

```bash
<<<<<<< HEAD
autoYoutubeUpdater.py <pl_url/song_url> [-o <output_folder> -i <offline_index_file>]
=======
autoYoutubeUpdater.py <pl_url/song_url> [-o <output_folder> -i <offline_index_file]
>>>>>>> 19f165b (Initial commit)
```

Argumente: 

- Playlist/Song
- (-o Output)
- -i Offline-Index File

## NC Uploader

