import os
import pyglet.media as media
import shutil
import tkinter as tk
import tkinter.filedialog as fd
import time
import sys
from random import shuffle
from tkinter import ttk
from tkinter import simpledialog
# personal imports
import backend

# root directory of Avideom
AVIDEOM_DIR = os.path.dirname(os.path.abspath(__file__))

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
        w2 = tk.Button(root, image=play, command=player.play, borderwidth=0)
        w2.place(x=10, y=150)
        w2tt = CreateToolTip(w2, 'Play')
        pause = tk.PhotoImage(file='bitmaps/player_pause.png')
        w3 = tk.Button(root, image=pause, command=player.pause, borderwidth=0)
        w3.place(x=60, y=150)
        w3tt = CreateToolTip(w3, 'Pause')
        next = tk.PhotoImage(file='bitmaps/player_next.png')
        # TODO -- put command in its own function and wrap a try-catch loop around it
        # IndexError when no sources queued up
        w4 = tk.Button(root, image=next, command=player.player.next_source, borderwidth=0)
        w4.place(x=110, y=150)
        w4tt = CreateToolTip(w4, 'Skip')
        ff = tk.PhotoImage(file='bitmaps/player_ff.png')
        w5 = tk.Button(root, image=ff, command=player.fast_forward, borderwidth=0)
        w5.place(x=160, y=150)
        w5tt = CreateToolTip(w5, 'Fast foward')
        rev = tk.PhotoImage(file='bitmaps/player_rev.png')
        w6 = tk.Button(root, image=rev, command=player.rewind, borderwidth=0)
        w6.place(x=210, y=150)
        w6tt = CreateToolTip(w6, 'Reverse')
        shuffle = tk.PhotoImage(file='bitmaps/shuffle.png')
        w7 = tk.Button(root, image=shuffle, command=lambda: self.shuffle(player), borderwidth=0)
        w7.place(x=210, y=100)
        w7tt = CreateToolTip(w7, 'Shuffle and play playlist')

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
        media_tab.add_command(label="Open Multiple Files...", command=lambda: self.open_files(player, time_slider))
        media_tab.add_command(label="Open Playlist...", command=lambda: self.open_playlist(player, time_slider))
        media_tab.add_separator()
        media_tab.add_command(label="Exit", command=lambda: self.exit(root))
        # settings tab layout
        settings.add_command(label="General", command=self.open_settings)
        settings.add_command(label="Radio")

        root['bg'] = 'white'
        root.mainloop()

    # shuffle and play a playlist
    def shuffle(self, player):
        folder = fd.askdirectory()
        for root, dirs, files in os.walk(folder):
            print(files)
            shuffle(files)
            print(files)
            for filename in files:
                path = os.path.join(root, str(filename))
                if not os.path.exists(path):
                    print('File not found; program terminated')
                    sys.exit()
                src = media.load(path, streaming=True)
                player.player.queue(src)
        player.play()

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
        player.play()
        # player.player.next_source()

    # open a playlist (a folder)
    def open_playlist(self, player, time_slider):
        folder = fd.askdirectory()
        for root, dirs, files in os.walk(folder):
            for filename in files:
                path = os.path.join(root, str(filename))
                if not os.path.exists(path):
                    print('File not found; program terminated')
                    sys.exit()
                src = media.load(path, streaming=True)
                player.player.queue(src)
        player.play()

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


# Popup window for playlist creation
class PopupEntry(tk.Tk):
    def __init__(self, root):
        top = self.top = tk.Toplevel(root)
        self.value = ''
        self.root = root
        self.l = tk.Label(top, text='Enter playlist name:')
        self.l.pack()
        self.e = tk.Entry(top)
        self.e.pack()
        self.b = tk.Button(top, text='Ok', command=self.destroy)
        self.b.pack()

    def destroy(self):
        self.value = self.e.get()
        self.top.destroy()


# TODO -- come up with more settings for user to edit
#       TODO -- create 'Edit Playlist' button
class Settings(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.playlist_name = ''
        root.geometry('260x230+30+30')
        root.title('General Settings')
        root['bg'] = 'white'

        create_playlist = tk.Button(root, command=self.create_playlist, text='Create playlist', bg='white', borderwidth=1)\
            .place(x=10, y=10)
        edit_playlist = tk.Button(root, command=self.edit_playlist, text='Edit Playlist', bg='white', borderwidth=1)\
            .place(x=10, y=40)
        equalizer = tk.Button(root, command=self.on_equalizer, text='Equalizer', bg='white', borderwidth=1)\
            .place(x=10, y=70)

        root.mainloop()

    def create_playlist(self):
        self.playlist_name = simpledialog.askstring('Avideom', 'Enter playlist name:')
        # TODO -- if user cancels dialog, exit out to main app
        files = fd.askopenfilenames()
        proj_path = AVIDEOM_DIR + '/playlists/' + self.playlist_name
        if not os.path.exists(proj_path):
            os.makedirs(proj_path)
        for filename in files:
            path = str(filename)
            # check legitimacy
            if not os.path.exists(path):
                print('File not found; program terminated')
                sys.exit()
            shutil.copy2(filename, proj_path)
        return

    def edit_playlist(self):
        try:
            edit_app = PlaylistEdit(tk.Tk())
            edit_app.mainloop()
        except RecursionError:
            print()
        return

    def on_equalizer(self):
        return

    def set_playlist_name(self, pname):
        self.playlist_name = pname


# Window for editing playlists
class PlaylistEdit(tk.Tk):
    def __init__(self, root):
        self.root = root
        root.title('Edit Playlist')
        root.geometry('260x230+30+30')
        root['bg'] = 'white'
        s = ttk.Style()
        s.configure('TOptionMenu', background='white')
        playlists = os.listdir(AVIDEOM_DIR + '/playlists/')

        self.var = tk.StringVar()
        self.var.set(playlists[0])
        self.var.trace('w', self.change_dropdown)

        w = tk.OptionMenu(root, self.var, *playlists)
        tk.Label(root, text='Choose playlist', bg='white').place(x=50, y=10)
        w.place(x=50, y=30)

        edit_btn = tk.Button(root, text='Edit', bg='white', borderwidth=1, command=lambda: self.on_edit(self.var.get()))
        edit_btn.place(x=50, y=60)

    def change_dropdown(self, *args):
        print(self.var.get())

    def on_edit(self, playlist):
        try:
            edit_app = PlaylistEdit2(tk.Tk(), playlist)
            edit_app.mainloop()
        except RecursionError:
            print()


class PlaylistEdit2(tk.Tk):
    def __init__(self, root, playlist):
        self.root = root
        root.title(playlist)
        root.geometry('260x230+30+30')
        root['bg'] = 'white'

        songlist = os.listdir(AVIDEOM_DIR + '/playlists/' + playlist)
        print(songlist)


# Create a tooltip for any given widget
# From https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        time.sleep(1)
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background='cyan', relief='solid', borderwidth=0,
                       font=("calibri", "10", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


if __name__ == '__main__':
    app = Main(tk.Tk())
    app.mainloop()
