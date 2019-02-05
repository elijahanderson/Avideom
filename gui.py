import tkinter as tk
import backend

root = tk.Tk()

msg = 'Avideom'
w1 = tk.Label(root, text=msg, justify=tk.LEFT, padx=10).pack(side='left')

play = tk.PhotoImage(file='bitmaps/player_play.png')
w2 = tk.Button(root, image=play, command=backend.backend).pack(side='bottom')
pause = tk.PhotoImage(file='bitmaps/player_pause.png')
w3 = tk.Label(root, image=pause).pack(side='bottom')
stop = tk.PhotoImage(file='bitmaps/player_stop.png')
w4 = tk.Label(root, image=stop).pack(side='bottom')
prev = tk.PhotoImage(file='bitmaps/player_prev.png')
w5 = tk.Label(root, image=prev).pack(side='bottom')
next = tk.PhotoImage(file='bitmaps/player_next.png')
w6 = tk.Label(root, image=next).pack(side='bottom')

root.mainloop()
