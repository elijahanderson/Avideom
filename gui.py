import os
import tkinter as tk
import sys
# personal imports
import backend


def main():
    filename = input('Enter file name: ')
    path = 'test_files/' + filename
    # check file legitimacy
    if not os.path.exists(path):
        print('File not found; program terminated')
        sys.exit()
    player = backend.MediaPlayer(path, 0, 100, 1.5)
    player.play_song()

    # -------------------------------------------------------------------
    # setting up GUI...
    root = tk.Tk()

    msg = 'Avideom'
    w1 = tk.Label(root, text=msg, justify=tk.LEFT, padx=10).pack(side='left')

    play = tk.PhotoImage(file='bitmaps/player_play.png')
    w2 = tk.Button(root, image=play, command=player.play).pack(side='bottom')
    pause = tk.PhotoImage(file='bitmaps/player_pause.png')
    w3 = tk.Button(root, image=pause, command=player.pause).pack(side='bottom')
    stop = tk.PhotoImage(file='bitmaps/player_stop.png')
    w4 = tk.Button(root, image=stop, command=player.stop).pack(side='bottom')
    ff = tk.PhotoImage(file='bitmaps/player_ff.png')
    w5 = tk.Button(root, image=ff).pack(side='bottom')
    rev = tk.PhotoImage(file='bitmaps/player_rev.png')
    w6 = tk.Button(root, image=rev).pack(side='bottom')

    root.mainloop()


if __name__ == '__main__':
    main()
