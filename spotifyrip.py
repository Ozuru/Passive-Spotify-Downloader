import pyaudio, wave, psutil, spotifyapi, time, sys, shutil, os, datetime, colorama
from colorama import Fore, Back, Style
from progressbar import *
SPOTIFY_RUNNING = "Spotify.exe" in [psutil.Process(i).name() for i in psutil.pids()]

playing_position = 0
song_length = 0
song_name = ""
song_album = ""
song_artist = ""

STORAGE_FOLDER = "E:\Dropbox\Dropbox\Music"

DATETIME = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

''' token generation '''
oauth_token = spotifyapi.get_oauth_token()
csrf_token = spotifyapi.get_csrf_token()

p = pyaudio.PyAudio()
colorama.init()

frames = []

print Fore.GREEN + "Successful OAuth Token: " + str(oauth_token is not None)
print "Successful CSRF Token: " + str(csrf_token is not None)
print "Is Spotify Running: " + str(SPOTIFY_RUNNING) + Style.RESET_ALL

def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c, '')
    return value

''' main loop '''
def record_song():
    global status, playing_position, song_artist, song_album, song_length, song_name, data
    status = spotifyapi.get_status(oauth_token, csrf_token, 1)
    if status is not None and status['playing'] is True: # if we had a successful connection and Spotify is playing
        playing_position = status['playing_position']
        song_length = status['track']['length']
        song_name = str(status['track']['track_resource']['name'])
        song_album = str(status['track']['album_resource']['name'])
        song_artist = str(status['track']['artist_resource']['name'])

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=input_device_index)
        startTime = time.time()
        endTime = (startTime + (song_length - playing_position)) + 0.7
        totalTime = endTime - startTime
        print Fore.WHITE + "Currently recording " + Back.RED + song_name + Back.RESET + " (" + song_album + ") " + "by " + song_artist + Fore.RESET
        print Fore.WHITE + "The recording will finish in " + Back.RED + str(round(endTime - time.time(), 2)) + Back.RESET + " seconds." + Fore.RESET
        try:
            widgets = ['Recording: ', Percentage(), ' ', Bar(marker=RotatingMarker(),left='[',right=']'), ' ', ETA(), ' '] #see docs for other options
            pbar = ProgressBar(widgets=widgets, maxval=totalTime)
            pbar.start()
            while time.time() < endTime:
                pbar.update(totalTime - (endTime - time.time()))
                data = stream.read(CHUNK) # read chunks of information from the stream
                frames.append(data) # append the data to the frames Array
            stream.stop_stream() # the song is over, stop reading and close it down boys
            stream.close()
            pbar.finish()

            if len(frames) > 50: # if there was a valid capture
                ''' save everything as a .wav file '''
                stripped_name = remove(song_artist + " - " + song_name, '\/:*?"<>|')
                wf = wave.open(stripped_name + ".wav", 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()

                if os.path.exists(STORAGE_FOLDER + "\\" + stripped_name + ".wav"):
                    mydir = os.path.join(STORAGE_FOLDER, str(DATETIME))
                    os.makedirs(mydir)
                    shutil.copy(stripped_name + ".wav", mydir)
                    print Fore.GREEN + "Copied " + stripped_name + ".wav to " + str(mydir) + Fore.RESET
                else:
                    shutil.copy(stripped_name + ".wav", STORAGE_FOLDER)
                    print Fore.GREEN + "Copied " + stripped_name + ".wav to " + STORAGE_FOLDER + Fore.RESET
                del frames[:] # clear out the frames array - keep this in
        except Exception as e: # occurs if data stream reader records null (?)
            print Fore.RED + "Exception with data stream reader.\n" + str(e) + Fore.RESET
            stream.stop_stream()
            stream.close()
    else: # can occur if Spotify is paused or connection issues between local API
        print Fore.YELLOW + "Spotify is paused or status is null." + Fore.RESET

def init():
    global p, input_device_index
    count = p.get_device_count()
    devices = []
    # iterates through the list of devices
    for i in range(count):
        devices.append(p.get_device_info_by_index(i))
    for i, dev in enumerate(devices):
        if "Virtual Audio Cable" in dev['name']:
            print Back.GREEN + "%d - %s" % (i, dev['name']) + Style.RESET_ALL
        else:
            print Back.RED + "%d - %s" % (i, dev['name']) + Style.RESET_ALL

    # set input_device_index to the input device of choice
    input_device_index = int(raw_input(Fore.YELLOW + 'Choose input device: ' + Fore.RESET))
try:
    init()
    while True:
        record_song()
except KeyboardInterrupt:
    p.terminate()
    print Fore.RED + "Keyboard interrupt, terminating!"
    sys.exit()