import datetime
import pyglet
import pyglet.media as media
import threading
import winsound as ws
import wx
import wx.lib.buttons as buttons

# jump_distance = 30


# MediaPlayer -- the class that stores several functions to manipulate a song file
class MediaPlayer:
    def __init__(self, path, song_time, song_duration, volume):
        self.path = path
        self.volume = volume
        self.songtime = song_time
        self.songduration = song_duration
        self.player = media.Player()    # the pyglet media player
        self.player.volume = 1.5
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
    def play(self):
        print('playing song...')
        self.player.play()
        print('...')
        return

    # reset the player
    def stop(self):
        print('stopping...')
        self.reset_player()
        print('...')
        return

    def now_(self):
        currtime = int(self.now())
        k = datetime.timedelta(seconds=currtime)
        k = str(k)
        return k

    def volume_(self, *args, **kwargs):
        try:
            volume = self.volume.get()
            self.player.volume = volume
        except:
            pass
        return

    # [fill this in]
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

    def play_song(self, *args, **kwargs):
        try:
            self.reset_player()
            try:
                src = media.load(self.path)
                self.player.queue(src)

                self.songduration = self.duration_()  # Updating duration Time
                return
            except Exception as e:
                print("[+] Something wrong when playing song", e)
                return
        except Exception as e:
            print(' [+] Please Check Your File Path', self.path.get())
            print(' [+] Error: Problem On Playing \n ', e)
            return
        return
