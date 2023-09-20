import os
import sys
from pytube import YouTube
import threading
import tkinter as tk
from tkinter import Label, Entry, Button, filedialog, messagebox

class DownloaderThread(threading.Thread):
    def __init__(self, links, output_folder, app):
        super().__init__()
        self.links = links
        self.output_folder = output_folder
        self.app = app

    def run(self):
        for link in self.links:
            self.app.update_progress(f"Downloading {link}...")
            download_mp3(link, self.output_folder)
        self.app.update_progress("Download completed!")

def download_mp3(link, output_folder):
    try:
        yt = YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            audio_stream.download(output_folder)
            os.rename(os.path.join(output_folder, f"{yt.title}.mp4"), os.path.join(output_folder, f"{yt.title}.mp3"))
    except Exception as e:
        print(f"Error: {e}")

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3 Downloader")
        self.root.geometry("800x500")
        self.center_window()

        self.link_label = Label(root, text="Enter YouTube Link(s) or Open Text File:", font=("Arial", 16))
        self.link_input = Entry(root, font=("Arial", 14))
        self.file_button = Button(root, text="Open Text File", font=("Arial", 14), command=self.open_text_file)
        self.output_label = Label(root, text="Select Output Folder:", font=("Arial", 16))
        self.output_folder_button = Button(root, text="Choose Folder", font=("Arial", 14), command=self.choose_output_folder)
        self.download_button = Button(root, text="Download", font=("Arial", 18, "bold"), command=self.start_download)
        self.progress_label = Label(root, text="", font=("Arial", 14))

        self.link_label.pack(pady=10)
        self.link_input.pack(pady=10)
        self.file_button.pack(pady=10)
        self.output_label.pack(pady=10)
        self.output_folder_button.pack(pady=10)
        self.download_button.pack(pady=20)
        self.progress_label.pack()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - 800) / 2)
        y = int((screen_height - 500) / 2)
        self.root.geometry(f"800x500+{x}+{y}")

    def open_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                links = file.read().splitlines()
                self.link_input.insert(0, "\n".join(links))

    def choose_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.output_label.config(text=f"Output Folder: {folder}")

    def start_download(self):
        links = self.link_input.get().splitlines()
        if links:
            if hasattr(self, "output_folder"):
                self.progress_label.config(text="Downloading...")
                downloader_thread = DownloaderThread(links, self.output_folder, self)
                downloader_thread.start()
            else:
                self.progress_label.config(text="Please select the output folder.")
        else:
            self.progress_label.config(text="Please enter valid YouTube link(s) or open a text file.")

    def update_progress(self, message):
        self.progress_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
