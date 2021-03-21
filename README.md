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

# Python Programm

## Downloader und Converter

### Usage:

```bash
main.py <pl_url/song_url> [-o <output_folder> -i <offline_index_file>]
main.py <pl_url/song_url> [-o <output_folder> -i <offline_index_file]
```

Argumente: 

- Playlist/Song
- (-o Output)
- (-i Offline-Index File)

