import datetime
import pyglet.media as media
import threading
import vlc

# global var for fast forwarding/reverse speed
jump_distance = 10


# MediaPlayer -- a class that stores several functions to manipulate a song file
class MediaPlayer:
    def __init__(self, song_time, song_duration, volume):
        self.path = ''
        # volume is a float from 0 (mute) to 1 (normal volume)
        self.volume = volume
        self.songtime = song_time
        self.songduration = song_duration
        self.player = media.Player()    # the pyglet media player
        self.time_thread()              # time updating thread

        # to keep the private fields and media player in sync
        # self.path.trace('w', self.play_song)
        # self.volume.trace('w', self.volume_)

    # jump to a different time on the track
    def jump(self, jump_time):
        try:
            self.player.seek(jump_time)
            return
        except:
            print('Error -- jump is not possible')
            return

    # return the current time on the track
    def now(self):
        currtime = self.player.time
        return currtime

    # pause the track
    def pause(self):
        print('pausing...')
        self.player.pause()
        print('...')
        return

    # play/continue the track
    def play(self, event=None):
        print('playing song...')
        self.player.play()
        print('...')
        return

    # play multiple tracks
    def play_multi(self):
        print('playing multiple songs')
        print(self.player.source.duration)
        self.songduration = self.player.source.duration
        self.player.play()
        return

    # reset the player
    def stop(self):
        print('stopping...')
        self.reset_player()
        print('...')
        return

    # return the current time, but as a string converted to "0:00:00" format
    def now_(self):
        currtime = int(self.now())
        k = datetime.timedelta(seconds=currtime)
        k = str(k)
        return k

    # TODO -- delete this class and see if the app still runs
    def volume_(self, *args, **kwargs):
        try:
            volume = self.volume.get()
            self.player.volume = volume
        except:
            pass
        return

    # to keep time consistent
    def time_thread(self):
        threading.Thread(target=self.update_time).start()
        return

    # to update the time on the track
    def update_time(self):
        while True:
            now = self.now_()
            try:
                self.songtime = now
                pass
            except Exception as e:
                print(e)
                pass

    # stop the track and reset the media player
    def reset_player(self):
        self.player.pause()
        self.player.delete()
        return

    # return the duration of the current source
    def duration(self):
        try:
            storeobj = self.player.source.duration
            return storeobj
        except:
            return '0'

    def duration_(self):
        time = self.duration() + 10.0
        k = datetime.timedelta(seconds=time)
        k = k.__str__()
        return k

    # fast forward current source according to the jump distance
    def fast_forward(self):
        time = self.player.time + jump_distance
        try:
            if self.duration() > time:
                self.player.seek(time)
            else:
                self.player.seek(self.duration())
        except AttributeError:
            pass

    # rewind current source according to the jump distance
    def rewind(self):
        time = self.player.time - jump_distance
        print('rewinding...')
        try:
            self.player.seek(time)
        except:
            self.player.seek(0)

    # reset the play and queue up a source
    def play_media(self, *args, **kwargs):
        try:
            self.reset_player()
            try:
                src = media.load(self.path)
                # use vlc module to play videos
                if src.video_format is not None:
                    instance = vlc.Instance()
                    vlc_player = instance.media_player_new()
                    vlc_media = instance.media_new(self.path)
                    vlc_media.get_mrl()
                    vlc_player.set_media(vlc_media)
                    vlc_player.play()
                self.player.queue(src)
                self.songduration = src.duration  # Updating duration Time
                return
            except Exception as e:
                print("Something wrong when playing song -- ", e)
                return
        except Exception as e:
            print('Please Check Your File Path; ', self.path)
            print('Error: Problem On Playing:\n ', e)
            return

    # update volume from volume slider
    def set_vol(self, nvol):
        self.player.volume = nvol / 100.0
        return

    # update current source path
    def set_path(self, npath):
        self.path = npath
        return
