import os
import pickle
import tkinter as tk
from tkinter import Grid, Widget, filedialog
from tkinter import PhotoImage
from tkinter import font
from pygame import mixer
from PIL import Image, ImageTk


class Player(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = ["Raataan Lambiyan Shershaah 128 Kbps.mp3"]

        self.current = 0
        self.paused = True
        self.played = False

        self.create_frames()
        self.track_Widgets()
        self.tracklist_Widgets()
        self.controls_Widgets()

    def create_frames(self):
        self.track = tk.LabelFrame(self, text='song Track', font=("times new roman", 15, "bold"), bg="grey", fg="white",
                                   bd=5, relief=tk.GROOVE)
        self.track.configure(width=410, height=300)
        self.track.grid(row=0, column=0, padx=10)

        self.tracklist = tk.LabelFrame(self, text=f'playlist-{len(self.playlist)}',
                                       font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5,
                                       relief=tk.GROOVE)
        self.tracklist.configure(width=210, height=400)
        self.tracklist.grid(row=0, column=1, rowspan=2, pady=20)

        self.controls = tk.LabelFrame(self, font=("times new roman", 15, "bold"), bg="white", fg="white", bd=5,
                                      relief=tk.GROOVE)
        self.controls.configure(width=410, height=300)
        self.controls.grid(row=2, column=0, pady=5, padx=10)

    def track_Widgets(self):
        self.canvas = tk.Label(self.track, image=photo)
        self.canvas.configure(width=400, height=240)
        self.canvas.grid(row=0, column=0)

        self.canvas = tk.Label(self.track, font=("times new roman", 15, "bold"), bg="white", fg="dark blue")
        self.canvas['text'] = 'Musicxy MP3 player'
        self.canvas.configure(width=30, height=1)
        self.canvas.grid(row=1, column=0)

    def tracklist_Widgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky='ns')

        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set,
                               selectbackground='sky blue')

        self.enumerate_songs()
        self.list.configure(height=22)
        self.list.bind('<Double-1>', self.play_songs)
        self.scrollbar.configure(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def controls_Widgets(self):
        self.loadSongs = tk.Button(self.controls, bg='green', fg='white', font=10)
        self.loadSongs['text'] = 'load Songs'
        self.loadSongs['command'] = self.retrieve_songs
        self.loadSongs.grid(row=0, column=0, padx=10)

        self.previous = tk.Button(self.controls, image=prev)
        self.previous.configure(width=50, height=30)
        self.previous['command'] = self.prev_songs
        self.previous.grid(row=0, column=1, padx=5)

        self.pauser = tk.Button(self.controls, image=pause)
        self.pauser.configure(width=50, height=30)
        self.pauser['command'] = self.pause_songs
        self.pauser.grid(row=0, column=2, padx=5)

        self.nexter = tk.Button(self.controls, image=next)
        self.nexter.configure(width=50, height=30)
        self.nexter['command'] = self.next_songs
        self.nexter.grid(row=0, column=3, padx=5)

        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.controls, from_=0, to=10, orient=tk.HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(8)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0, column=4, padx=5)

    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '' + file).replace('\\', '/')
                    self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)

        self.playlist = self.songlist
        self.tracklist['text'] = f'playlist-{len(self.playlist)}'
        self.list.delete(0, tk.END)
        self.enumerate_songs()

    def prev_songs(self):
        pass

    def pause_songs(self):
        pass

    def play_songs(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg='white')

        mixer.music.load(self.playlist[self.current])
        mixer.music.play()

    def next_songs(self):
        pass

    def change_volume(self, event=None):
        self.v = self.volume.get()
        print(self.v)


root = tk.Tk()
root.geometry('600x400')
root.wm_title('MUSIC PLAYER')

image = Image.open("img14.jpg")
photo = ImageTk.PhotoImage(image)

image2 = Image.open("prevbutton2.jpg")
prev = ImageTk.PhotoImage(image2)

image3 = Image.open("pausebutton2.jpg")
pause = ImageTk.PhotoImage(image3)

image4 = Image.open("nextbutton2.jpg")
next = ImageTk.PhotoImage(image4)
# play=PhotoImage(file='C:\Users\krishna\Desktop\sublimetext\vscode\.vscode\playbutton.png')
# pause=PhotoImage(file='C:\Users\krishna\Desktop\sublimetext\vscode\.vscode\pausebutton.png')
# next=PhotoImage(file='C:\Users\krishna\Desktop\sublimetext\vscode\.vscode\nextbutton.png')
app = Player(master=root)
app.mainloop()