import os
import pyglet.media as media
import tkinter as tk
import tkinter.filedialog as fd
import time
import sys
from tkinter import ttk
# personal imports
import backend


class Main(tk.Tk):
    def __init__(self, root):
        player = backend.MediaPlayer(0, 100, 1.5)

        # -------------------------------------------------------------------
        # setting up GUI...
        self.root = root
        root.geometry('260x230+30+30')
        root.title('Avideom')
        s = ttk.Style()
        s.configure('TScale', background='white', sliderlength=10)

        # some standard media player functionalities
        play = tk.PhotoImage(file='bitmaps/player_play.png')
        w2 = tk.Button(root, image=play, command=player.play, borderwidth=0).place(x=10, y=150)
        pause = tk.PhotoImage(file='bitmaps/player_pause.png')
        w3 = tk.Button(root, image=pause, command=player.pause, borderwidth=0).place(x=60, y=150)
        next = tk.PhotoImage(file='bitmaps/player_next.png')
        w4 = tk.Button(root, image=next, command=player.player.next_source, borderwidth=0).place(x=110, y=150)
        ff = tk.PhotoImage(file='bitmaps/player_ff.png')
        w5 = tk.Button(root, image=ff, command=player.fast_forward, borderwidth=0).place(x=160, y=150)
        rev = tk.PhotoImage(file='bitmaps/player_rev.png')
        w6 = tk.Button(root, image=rev, command=player.rewind, borderwidth=0).place(x=210, y=150)

        vol = tk.DoubleVar()
        # volume slider -- using lambda here so I can pass in parameters
        volume_slider = ttk.Scale(root, from_=0, to=100, variable=vol, orient='vertical', command=lambda x: player.set_vol(vol.get())).place(x=10, y=30)

        # time slider
        vtime = tk.IntVar()
        # TODO -- dragging slider changes player's songtime and updates song duration, but doesn't display curr time
        time_slider = ttk.Scale(root, from_=0, to=player.songduration, orient='horizontal', length=240,
                                variable=vtime,
                                command=lambda x: player.player.seek(vtime.get()))
        time_slider.place(x=10, y=190)

        # creating the menu
        menu = tk.Menu(root)
        root.config(menu=menu)
        media_tab = tk.Menu(menu)  # the file tab
        settings = tk.Menu(menu)  # the settings tab
        menu.add_cascade(label="Media", menu=media_tab)
        menu.add_cascade(label="Settings", menu=settings)
        # file tab layout
        media_tab.add_command(label="Open File...", command=lambda: self.open_file(player, time_slider))
        # TODO -- add actual functionality for opening multiple files
        media_tab.add_command(label="Open Multiple Files...", command=lambda: self.open_files(player, time_slider))
        media_tab.add_command(label="Open Folder...", command=lambda: self.open_file(player, time_slider))
        media_tab.add_separator()
        media_tab.add_command(label="Exit", command=lambda: self.exit(root))
        # settings tab layout
        settings.add_command(label="General", command=self.open_settings)
        settings.add_command(label="Radio")

        root['bg'] = 'white'
        root.mainloop()

    # open single file
    def open_file(self, player, time_slider):
        filename = fd.askopenfilename()
        path = str(filename)
        # check file legitimacy
        if not os.path.exists(path):
            print('File not found; program terminated')
            sys.exit()
        player.set_path(path)
        player.play_media()
        time_slider.config(to=player.songduration)

    # open multiple files
    def open_files(self, player, time_slider):
        files = fd.askopenfilenames()
        # check file legitimacy
        for filename in files:
            path = str(filename)
            if not os.path.exists(path):
                print('File not found; program terminated')
                sys.exit()
            src = media.load(path, streaming=True)
            player.player.queue(src)
        print(player.player.source)
        player.play()
        # player.player.next_source()

    def open_settings(self):
        settings_app = Settings(tk.Tk())
        settings_app.mainloop()

    # to convert between actual no. seconds and display time
    def conv_time(self, disp_time):
        time_list = disp_time.split(':')
        print(time_list)
        total_sec = (int(time_list[0])*60) + (int(time_list[1])) + (int(time_list[2])/60)
        print(total_sec)
        return total_sec

    def exit(self, root):
        root.destroy()
        sys.exit()


class Settings(tk.Tk):
    def __init__(self, root):
        self.root = root
        root.geometry('260x230+30+30')
        root.title('General Settings')
        root['bg'] = 'white'
        s = ttk.Style()
        # s.configure('TButton', background='white')

        playlist = tk.Button(root, command=self.create_playlist, text='Create playlist', bg='white', borderwidth=1)\
            .place(x=10, y=10)
        equalizer = tk.Button(root, command=self.on_equalizer, text='Equalizer', bg='white', borderwidth=1)\
            .place(x=10, y=40)

        root.mainloop()

    def create_playlist(self):
        return

    def on_equalizer(self):
        return


if __name__ == '__main__':
    app = Main(tk.Tk())
    app.mainloop()
