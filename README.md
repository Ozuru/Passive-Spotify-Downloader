# Passive Spotify Downloader by [Ozuru](http://www.malware.cat/)

## What is Passive Spotify Downloader?

Passive Spotify Downloader (PSD) passively downloads songs streamed through Spotify. It is intended to be ran in the background while listening to Spotify. PSD detects when a song is being played and records it as it's being listened to.

I started this project because I was annoyed how how Spotify's mobile app has thousands of ads compared to the few I come across on the computer. When Spotify is playing, the program downloads the file. Optimally, the output file is synced with mobile to allow cross-platform playing. If a file has been recorded already, it creates a copy of it in a file with the timestamp.

## What do I need to run Passive Spotify Downloader?

1. [Virtual Audio Cable](http://software.muzychenko.net/eng/vac.htm)
2. [Audio Router](https://www.reddit.com/user/audiorouterdev) (if this is removed, I will upload a mirror)
3. [Python 2.7.x](https://www.python.org)
 
## Setup Guide

This guide assumes you have everything installed and the program's files extracted somewhere.

1. Download and extract the files somewhere. It doesn't matter where.
2. Open Audio Router and Virtual Audio Cable's Control Panel and Audio Repeater.
3. In Audio Router, make Spotify output to Virtual Audio Cable's Line 1.
4. In Virtual Audio Cable's Audio Repeater, set your wave in to "Line 1 (Virtual Audio Cable)" and wave out to whatever your speakers/headphones are set to.
5. Ensure the sample rate (in Audio Repeater) is set to 44100. This is what Spotify plays at.
6. Set the total buffer to 500 and buffers to 12. Increase this if you have issues with the audio quality.

You're done! What we effectively did is route Spotify's output to a seperate audio cable line and then route that audio to your speakers. This is so you can listen to Spotify while it is recording and isolated. Enjoy the music.

## Usage Guide

```python
STORAGE_FOLDER = "E:\Dropbox\Dropbox\Music"
```

###### STORAGE_FOLDER
This value is the path to where the storage folder is located. No trailing slashes.

## Credits

[spotifyapi.py](https://github.com/cgbystrom/spotify-local-http-api)