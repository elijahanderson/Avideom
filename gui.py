import os
import tkinter as tk
import tkinter.filedialog as fd
import sys
# personal imports
import backend


def open_file(player):
    filename = fd.askopenfilename()
    path = str(filename)
    # check file legitimacy
    if not os.path.exists(path):
        print('File not found; program terminated')
        sys.exit()
    player.set_path(path)
    player.play_song()


def main():
    player = backend.MediaPlayer(0, 100, 1.5)

    # -------------------------------------------------------------------
    # setting up GUI...
    root = tk.Tk()
    root.geometry('260x200+30+30')

    msg = 'Avideom'
    w1 = tk.Label(root, text=msg, justify=tk.LEFT, padx=10).place(x=90, y=30)

    # some standard media player functionalities
    play = tk.PhotoImage(file='bitmaps/player_play.png')
    w2 = tk.Button(root, image=play, command=player.play).place(x=10, y=150)
    pause = tk.PhotoImage(file='bitmaps/player_pause.png')
    w3 = tk.Button(root, image=pause, command=player.pause).place(x=60, y=150)
    stop = tk.PhotoImage(file='bitmaps/player_stop.png')
    w4 = tk.Button(root, image=stop, command=player.stop).place(x=110, y=150)
    ff = tk.PhotoImage(file='bitmaps/player_ff.png')
    w5 = tk.Button(root, image=ff, command=player.fast_forward).place(x=160, y=150)
    rev = tk.PhotoImage(file='bitmaps/player_rev.png')
    w6 = tk.Button(root, image=rev, command=player.rewind).place(x=210, y=150)
    vol = tk.DoubleVar()
    # using lambda here so I can pass in parameters
    w7 = tk.Scale(root, from_=0, to=100, variable=vol, command=lambda x: player.set_vol(vol.get())).place(x=10, y=30)

    # creating the menu
    menu = tk.Menu(root)
    root.config(menu=menu)
    file_tab = tk.Menu(menu)  # the file tab
    settings = tk.Menu(menu)  # the settings tab
    menu.add_cascade(label="File", menu=file_tab)
    menu.add_cascade(label="Settings", menu=settings)
    # file tab layout
    file_tab.add_command(label="Open...", command=lambda: open_file(player))  # , command=....
    file_tab.add_separator()
    file_tab.add_command(label="Exit", command=root.quit)
    # settings tab layout
    settings.add_command(label="General")
    settings.add_command(label="Radio")

    root.mainloop()


if __name__ == '__main__':
    main()
