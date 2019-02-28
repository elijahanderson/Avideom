import os
import tkinter as tk
import tkinter.filedialog as fd
import sys
from tkinter import ttk
# personal imports
import backend


def open_file(player, time_slider):
    filename = fd.askopenfilename()
    path = str(filename)
    # check file legitimacy
    if not os.path.exists(path):
        print('File not found; program terminated')
        sys.exit()
    player.set_path(path)
    player.play_song()
    print(player.songduration)
    time_slider.config(to=player.songduration)


# to convert between actual no. seconds and display time
def conv_time(disp_time):
    time_list = disp_time.split(':')
    print(time_list)
    total_sec = (int(time_list[0])*60) + (int(time_list[1])) + (int(time_list[2])/60)
    print(total_sec)
    return total_sec


def main():
    player = backend.MediaPlayer(0, 100, 1.5)

    # -------------------------------------------------------------------
    # setting up GUI...
    root = tk.Tk()
    root.geometry('260x230+30+30')
    root.title('Avideom')
    s = ttk.Style()
    s.configure('TScale', background='white', sliderlength=10)

    # some standard media player functionalities
    play = tk.PhotoImage(file='bitmaps/player_play.png')
    w2 = tk.Button(root, image=play, command=player.play, borderwidth=0).place(x=10, y=150)
    pause = tk.PhotoImage(file='bitmaps/player_pause.png')
    w3 = tk.Button(root, image=pause, command=player.pause, borderwidth=0).place(x=60, y=150)
    stop = tk.PhotoImage(file='bitmaps/player_stop.png')
    w4 = tk.Button(root, image=stop, command=player.stop, borderwidth=0).place(x=110, y=150)
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
    file_tab = tk.Menu(menu)  # the file tab
    settings = tk.Menu(menu)  # the settings tab
    menu.add_cascade(label="File", menu=file_tab)
    menu.add_cascade(label="Settings", menu=settings)
    # file tab layout
    file_tab.add_command(label="Open...", command=lambda: open_file(player, time_slider))  # , command=....
    file_tab.add_separator()
    file_tab.add_command(label="Exit", command=root.quit)
    # settings tab layout
    settings.add_command(label="General")
    settings.add_command(label="Radio")

    root['bg'] = 'white'
    root.mainloop()


if __name__ == '__main__':
    main()
