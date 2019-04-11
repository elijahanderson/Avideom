import os
import pyglet.media as media
import shutil
import sys
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import time
from random import shuffle
from tkinter import ttk
from tkinter import simpledialog
import vlc
# personal imports
import backend

# CHANGES FOR CHECKPOINT 3:
#   - implement hovering tool tips [x]
#   - display song title and artist on GUI [x]
#   - implement radio streaming abilities [sort of]
#   - add hotkeys [x]
#   - add help menu [x]

# root directory of Avideom
AVIDEOM_DIR = os.path.dirname(os.path.abspath(__file__))


class Main(tk.Tk):
    def __init__(self, root):
        # the media player backend
        player = backend.MediaPlayer(0, 100, 1.5)

        # -------------------------------------------------------------------

        # setting up GUI...
        self.root = root
        root.geometry('260x230+30+30')
        root.title('Avideom')
        root['bg'] = 'white'
        root.protocol('WM_DELETE_WINDOW', lambda: self.on_close(root, player))
        s = ttk.Style()
        s.configure('TScale', background='white', sliderlength=10)

        ################################################
        # [some standard media player functionalities] #
        ################################################

        # SONG & ARTIST DISPLAY
        display = tk.StringVar()
        display.set('Now playing...')
        self.l1 = tk.Label(root, textvariable=display, bg='white')
        self.l1.place(x=130, y=50, anchor='center')

        # PLAY
        play = tk.PhotoImage(file='bitmaps/player_play.png')
        w2 = tk.Button(root, image=play, command=player.play, borderwidth=0)
        w2.place(x=10, y=150)
        w2tt = CreateToolTip(w2, 'Play')

        # PAUSE
        pause = tk.PhotoImage(file='bitmaps/player_pause.png')
        w3 = tk.Button(root, image=pause, command=player.pause, borderwidth=0)
        w3.place(x=60, y=150)
        w3tt = CreateToolTip(w3, 'Pause')

        # NEXT SOURCE
        next_btn = tk.PhotoImage(file='bitmaps/player_next.png')
        # TODO -- put command in its own function and wrap a try-catch loop around it
        # IndexError when no sources queued up
        w4 = tk.Button(root, image=next_btn, command=lambda: self.next_source(player, display), borderwidth=0)
        w4.place(x=110, y=150)
        w4tt = CreateToolTip(w4, 'Skip')

        # FAST FORWARD
        ff = tk.PhotoImage(file='bitmaps/player_ff.png')
        w5 = tk.Button(root, image=ff, command=player.fast_forward, borderwidth=0)
        w5.place(x=160, y=150)
        w5tt = CreateToolTip(w5, 'Fast foward')

        # REVERSE
        rev = tk.PhotoImage(file='bitmaps/player_rev.png')
        w6 = tk.Button(root, image=rev, command=player.rewind, borderwidth=0)
        w6.place(x=210, y=150)
        w6tt = CreateToolTip(w6, 'Reverse')

        # SHUFFLE AND PLAY
        shuffle_btn = tk.PhotoImage(file='bitmaps/shuffle.png')
        w7 = tk.Button(root, image=shuffle_btn, command=lambda: self.shuffle(player), borderwidth=0)
        w7.place(x=210, y=100)
        w7tt = CreateToolTip(w7, 'Shuffle and play playlist')

        # VOLUME SLIDER -- using lambda is used to pass parameters without running the fnc upon app start
        vol = tk.DoubleVar()
        volume_slider = ttk.Scale(root, from_=0, to=100, variable=vol, orient='vertical',
                                  command=lambda x: player.set_vol(vol.get())).place(x=10, y=30)

        # TIME SLIDER
        vtime = tk.IntVar()
        # TODO -- dragging slider changes player's songtime and updates song duration, but doesn't display curr time
        time_slider = ttk.Scale(root, from_=0, to=player.songduration, orient='horizontal', length=240,
                                variable=vtime,
                                command=lambda x: player.player.seek(vtime.get()))
        time_slider.place(x=10, y=190)

        # MENU CREATION
        menu = tk.Menu(root)
        root.config(menu=menu)
        media_tab = tk.Menu(menu)  # the media tab
        settings = tk.Menu(menu)  # the settings tab
        help_tab = tk.Menu(menu)
        radio = tk.Menu(menu)
        menu.add_cascade(label="Media", menu=media_tab)
        menu.add_cascade(label="Settings", menu=settings)
        menu.add_cascade(label='Radio', menu=radio)
        menu.add_cascade(label='Help', menu=help_tab)

        # file tab layout
        media_tab.add_command(label="Open File...", command=lambda: self.open_file(player, time_slider, display))
        media_tab.add_command(label="Open Multiple Files...", command=lambda: self.open_files(player, time_slider, display))
        media_tab.add_command(label="Open Playlist...", command=lambda: self.open_playlist(player, time_slider, display))
        media_tab.add_separator()
        media_tab.add_command(label="Exit", command=lambda: self.on_close(root))

        # settings tab layout
        settings.add_command(label="Open Settings", command=self.open_settings)

        # radio tab layout
        radio.add_command(label="Launch Radio", command=self.open_radio)

        # help tab layout
        help_tab.add_command(label='Hotkeys', command=self.open_hotkeys)
        help_tab.add_command(label='About Avideom', command=self.open_about)

        # HOTKEY BINDING
        root.bind('<space>', player.play)
        root.bind('p', player.pause)
        root.bind('<Right>', lambda event: self.next_source(player, display))
        root.bind('<Control-Right>', player.fast_forward)
        root.bind('<Control-Left>', player.rewind)
        root.bind('<Control-s>', lambda event: self.shuffle(player))
        root.bind('<Alt-s>', self.open_settings)
        root.bind('<Alt-r>', self.open_radio)
        root.bind('<Alt-o>', lambda event: self.open_file(player, time_slider, display))
        root.bind('<Alt-p>', lambda event: self.open_playlist(player, time_slider, display))
        root.bind('<Alt-m>', lambda event: self.open_files(player, time_slider, display))

        # self.change_display(display, player.player)
        root.mainloop()

    # shuffle and play a playlist
    def shuffle(self, player, event=None):
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

    # open and load single file
    def open_file(self, player, time_slider, display, event=None):
        filename = fd.askopenfilename()
        path = str(filename)
        # check file legitimacy
        if not os.path.exists(path):
            print('File not found; program terminated')
            sys.exit()
        player.set_path(path)
        player.play_media()
        time_slider.config(to=player.songduration)
        self.change_display(display, player)

    # open and load multiple files
    def open_files(self, player, time_slider, display):
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
        self.change_display(display, player)

    # open and load a playlist
    def open_playlist(self, player, time_slider, display):
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
        self.change_display(display, player)

    # launch the settings window
    def open_settings(self, event=None):
        settings_app = Settings(tk.Tk())
        settings_app.mainloop()

    # to convert between actual no. seconds and display time
    def conv_time(self, disp_time):
        time_list = disp_time.split(':')
        print(time_list)
        total_sec = (int(time_list[0])*60) + (int(time_list[1])) + (int(time_list[2])/60)
        print(total_sec)
        return total_sec

    # exit Avideom
    def on_close(self, root, player):
        player.pause()
        root.destroy()
        sys.exit()

    # change song & artist display
    def change_display(self, label, player):
        src = player.player.source
        title = src.info.title.decode('utf-8')
        artist = src.info.author.decode('utf-8')
        if title == '':
            title = player.path.split('/')[-1][:-4]
        artist = '[Artist not found]' if artist == '' else artist
        nstr = title + '\nby ' + artist
        label.set(nstr)
        self.root.update()
        return

    # play the next source and change the song display
    def next_source(self, player, label, event=None):
        player.player.next_source()
        self.change_display(label, player)
        return

    def open_radio(self, event=None):
        radio_app = Radio(tk.Tk())
        radio_app.mainloop()
        return

    def open_about(self):
        about_app = About(tk.Tk())
        about_app.mainloop()
        return

    def open_hotkeys(self):
        hk_app = Hotkeys(tk.Tk())
        hk_app.mainloop()
        return


class Radio(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.url = ''
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player_vlc = self.instance.media_player_new()
        self.media = self.instance.media_new(self.url)

        self.root.geometry('50x100+30+30')
        self.root.title('Radio')
        self.root['bg'] = 'white'
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)

        b1 = tk.Button(self.root, text='Pop', bg='white', borderwidth=1, command=self.stream_pop)
        b1.place(x=10, y=10)
        b2 = tk.Button(self.root, text='Classic Rock', bg='white', borderwidth=1, command=self.stream_cr)
        b2.place(x=10, y=40)
        b3 = tk.Button(self.root, text='Sleep', bg='white', borderwidth=1, command=self.stream_s)
        b3.place(x=10, y=70)

        # play_img = tk.PhotoImage(file='bitmaps/player_play.png')
        # b4 = tk.Button(root, image=play_img, command=self.rplay, borderwidth=0)
        # b4.place(x=60, y=150)
        # pause = tk.PhotoImage(file='bitmaps/player_pause.png')
        # b5 = tk.Button(root, image=pause, command=self.rpause, borderwidth=0)
        # b5.place(x=120, y=150)

        self.root.mainloop()

    def stream_pop(self):
        self.url = 'http://ic7.101.ru:8000/c15_5'
        self.rplay()

    def stream_cr(self):
        self.url = 'http://ic7.101.ru:8000/c15_1'
        self.rplay()

    def stream_s(self):
        self.url = 'http://ic7.101.ru:8000/c15_3'
        self.rplay()

    def rplay(self):
        self.media = self.instance.media_new(self.url)
        self.media.get_mrl()
        self.player_vlc.set_media(self.media)
        self.player_vlc.play()

    def rpause(self):
        self.player_vlc.pause()

    def rstop(self):
        self.player_vlc.stop()

    def on_close(self):
        self.rstop()
        self.root.destroy()


class About(tk.Tk):
    def __init__(self, root):
        self.root = root
        root.geometry('530x330+30+30')
        root.title('About Avideom')
        root['bg'] = 'white'
        self.display = tk.Text(root, bg='white')
        self.display.insert('insert', 'Avideom is an open-source desktop media player application\n'
                                                       'created as my senior project.\n\n'
                                                       'This project consists of the implementation of an open-source\n'
                                                       'desktop media player application. Avideom is able to play both\n'
                                                       'audio and video media files (such as .mp3, .wav, .mp4, .mov,\n'
                                                       'etc.) directly from the user’s files. It is designed as a \n'
                                                       'better alternative to the Windows Media Player, the default\n'
                                                       'media player application on Windows operating systems.\n\n'
                                                       'Once a user runs Avideom, he or she can select any audio '
                                                       '\nor video file with a recognized file extension and it will '
                                                       '\nplay the corresponding media. Avideom features a clean and\n'
                                                       'intuitive GUI and all standard media player functions\n'
                                                       '(pause, play, skip, volume control, etc.), and potentially\n'
                                                       'bonus features such as visualizations, an EQ tuner, or\n'
                                                       'different playback speeds. Avideom uses the Python programming '
                                                       '\nlanguage as well as a number of its libraries to accomplish\n'
                                                       'the above tasks. It can be downloaded for free online.')
        self.display.place(x=10, y=10)
        root.mainloop()


class Hotkeys(tk.Tk):
    def __init__(self, root):
        self.root = root
        root.geometry('230x200+30+30')
        root.title('Hotkeys')
        root['bg'] = 'white'

        self.display = tk.Listbox(root, bg='white', width=35, selectbackground='gray')
        self.display.insert(1, 'Play.............<Space>')
        self.display.insert(7, 'Settings.........<Alt+S>')
        self.display.insert(8, 'Open File........<Alt+O>')
        self.display.insert(9, 'Open Files.......<Alt+M>')
        self.display.insert(10, 'Open Playlist....<Alt+P>')
        self.display.insert(6, 'Skip.............<Right Arrow>')
        self.display.insert(2, 'Pause............<P>')
        self.display.insert(3, 'Fast Forward.....<Crtl+Right Arrow>')
        self.display.insert(4, 'Reverse..........<Crtl+Left Arrow>')
        self.display.insert(5, 'Shuffle..........<Ctrl+S>')
        self.display.place(x=10, y=10)

        root.mainloop()


# settings window to allow user to edit various app settings
# TODO -- come up with more settings for user to edit
# ---- option to edit jump distance for FF/rev
class Settings(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.playlist_name = ''
        root.geometry('260x100+30+30')
        root.title('General Settings')
        root['bg'] = 'white'

        create_playlist = tk.Button(root, command=self.create_playlist, text='Create playlist', bg='white', borderwidth=1)\
            .place(x=10, y=10)
        edit_playlist = tk.Button(root, command=self.edit_playlist, text='Edit Playlist', bg='white', borderwidth=1)\
            .place(x=10, y=40)
        equalizer = tk.Button(root, command=self.on_equalizer, text='Equalizer', bg='white', borderwidth=1)\
            .place(x=10, y=70)

        root.mainloop()

    # create and store a playlist in /playlists
    def create_playlist(self):
        # ask for name -- display error and exit settings if playlist name already exists
        self.playlist_name = simpledialog.askstring('Avideom', 'Enter playlist name:')
        if self.playlist_name is not None:
            proj_path = AVIDEOM_DIR + '/playlists/' + self.playlist_name
            if not os.path.exists(proj_path):
                os.makedirs(proj_path)
            else:
                mb.showinfo('Error', 'This playlist name already exists -- please try a different name.')
                self.root.destroy()
                return

            # creation and storage
            files = fd.askopenfilenames()
            for filename in files:
                path = str(filename)
                # check legitimacy
                if not os.path.exists(path):
                    print('File not found; program terminated')
                    sys.exit()
                shutil.copy2(filename, proj_path)
            self.root.destroy()
        return

    # launch window for editing playlists
    def edit_playlist(self):
        try:
            edit_app = PlaylistEdit(tk.Tk())
            edit_app.mainloop()
        except RecursionError:
            print()
        return

    # TODO
    def on_equalizer(self):
        return

    # change playlist name
    def set_playlist_name(self, pname):
        self.playlist_name = pname


# Window for editing playlists
# TODO -- add option to change playlist name
class PlaylistEdit(tk.Tk):
    def __init__(self, root):
        self.root = root
        root.title('Edit Playlist')
        root.geometry('260x120+10+10')
        root['bg'] = 'white'
        s = ttk.Style()
        s.configure('TOptionMenu', background='white')
        playlists = os.listdir(AVIDEOM_DIR + '/playlists/')

        # to have a default value display for the dropdown
        var = tk.StringVar(root)
        var.set(playlists[0])
        var.trace('w', self.change_dropdown)

        # dropdown menu to select a playlist to edit
        w = ttk.OptionMenu(root, var, playlists[0], *playlists)
        tk.Label(root, text='Choose playlist to edit:', bg='white').place(x=10, y=10)
        w.place(x=10, y=30)

        edit_btn = tk.Button(root, text='Edit', bg='white', borderwidth=1, command=lambda: self.on_edit(var.get()))
        edit_btn.place(x=10, y=60)

        dlt_btn = tk.Button(root, text='Delete', bg='white', borderwidth=1, command=lambda: self.on_delete(var.get()))
        dlt_btn.place(x=10, y=90)

    # for some reason, the window does not work without this function
    def change_dropdown(self, *args):
        return

    # launch the second playlist editing menu
    def on_edit(self, playlist):
        try:
            edit_app = PlaylistEdit2(tk.Tk(), playlist)
            edit_app.mainloop()
        except RecursionError:
            print()

    # delete the selected playlist
    def on_delete(self, playlist):
        path = AVIDEOM_DIR + '/playlists/' + playlist
        shutil.rmtree(path)


# a second window for editing a specific playlist
class PlaylistEdit2(tk.Tk):
    def __init__(self, root, playlist):
        self.root = root
        self.playlist_path = AVIDEOM_DIR + '/playlists/' + playlist
        var = tk.StringVar(root)
        root.title(playlist)
        root.geometry('260x120+10+10')
        root['bg'] = 'white'

        songlist = os.listdir(self.playlist_path)
        var.set(songlist[0])
        var.trace('w', self.change_dropdown)
        w = ttk.OptionMenu(root, var, songlist[0], *songlist)
        w.place(x=10, y=30)

        tk.Label(root, text='Choose song to edit:', bg='white').place(x=10, y=10)
        add = tk.Button(root, text='Add song', bg='white', borderwidth=1, command=self.add_song).place(x=10, y=60)
        dlt = tk.Button(root, text='Delete song', bg='white', borderwidth=1,
                        command=lambda: self.del_song(var.get())).place(x=10, y=90)

    # add selected song to playlist
    def add_song(self):
        filename = fd.askopenfilename()
        path = str(filename)
        # check file legitimacy
        if not os.path.exists(path):
            print('File not found; program terminated')
            sys.exit()
        shutil.copy2(path, self.playlist_path)

    # delete selected song from playlist
    def del_song(self, song):
        os.remove(self.playlist_path + '/' + song)

    # still not sure why this is required
    def change_dropdown(self, *args):
        return


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
