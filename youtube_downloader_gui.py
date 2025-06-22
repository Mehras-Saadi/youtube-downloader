import os
import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
from tkinter import ttk
import json
import threading


def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    return {"proxy": "", "save_path": os.getcwd()}

def save_settings(proxy, path):
    with open("settings.json", "w") as f:
        json.dump({"proxy": proxy, "save_path": path}, f)

settings = load_settings()


def set_proxy(proxy_url):
    if proxy_url:
        os.environ["HTTP_PROXY"] = proxy_url
        os.environ["HTTPS_PROXY"] = proxy_url


def choose_directory():
    path = filedialog.askdirectory()
    if path:
        download_path.set(path)
        save_settings(proxy_entry.get().strip(), path)


def threaded_download():
    thread = threading.Thread(target=download)
    thread.start()


def download():
    link = url_entry.get().strip()
    proxy = proxy_entry.get().strip()
    mode = var.get()
    save_path = download_path.get()

    if not link:
        messagebox.showwarning("Warning", "Please enter a YouTube link.")
        return

    try:
        set_proxy(proxy)
        yt = YouTube(link, on_progress_callback=on_progress)
        title = yt.title
        status_label.config(text=f"Downloading: {title}")

        if mode == "video":
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.filter(only_audio=True).first()

        progress_bar["value"] = 0
        root.update_idletasks()

        stream.download(output_path=save_path, filename=yt.title + (".mp3" if mode == "audio" else ""))
        messagebox.showinfo("Success", f"Downloaded: {yt.title}")
        status_label.config(text="✅ Done.")
        save_settings(proxy, save_path)

    except Exception as e:
        status_label.config(text="❌ Error occurred.")
        messagebox.showerror("Error", f"Lotfan az Filter Shekan estefade konid.\nYa Proxy dorost vared konid.\n\n{str(e)}")

# ---------- Download Progress ----------
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    downloaded = total_size - bytes_remaining
    percent = (downloaded / total_size) * 100
    progress_bar["value"] = percent
    root.update_idletasks()

# ---------- GUI ----------
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("520x300")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')
style.configure("Rounded.TButton", foreground="white", background="#A04CAF", padding=10, relief="flat")
style.map("Rounded.TButton", background=[('active', "#8E3862"), ('!active', "#423BC2")])



main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

tk.Label(main_frame, text="🎥 YouTube Link:").grid(row=0, column=0, sticky="w", pady=(0, 8), padx=(0, 8))
url_entry = tk.Entry(main_frame, width=55)
url_entry.grid(row=0, column=1, pady=(0, 8), sticky="w")

tk.Label(main_frame, text="🌐 Proxy (optional):").grid(row=1, column=0, sticky="w", pady=(0, 8), padx=(0, 8))
proxy_entry = tk.Entry(main_frame, width=55)
proxy_entry.insert(0, settings.get("proxy", ""))
proxy_entry.grid(row=1, column=1, pady=(0, 8), sticky="w")

tk.Label(main_frame, text="💾 Download Folder:").grid(row=2, column=0, sticky="w", pady=(0, 8), padx=(0, 8))
download_path = tk.StringVar(value=settings.get("save_path", os.getcwd()))
tk.Entry(main_frame, textvariable=download_path, width=40).grid(row=2, column=1, sticky="w", pady=(0, 8))
tk.Button(main_frame, text="Browse", command=choose_directory).grid(row=2, column=1, sticky="e", padx=(0, 5), pady=(0, 8))

tk.Label(main_frame, text="🎧 Download Type:").grid(row=3, column=0, sticky="w", pady=(0, 8), padx=(0, 8))
var = tk.StringVar(value="video")
radio_frame = tk.Frame(main_frame, bg="#162447")
radio_frame.grid(row=3, column=1, sticky="w", pady=(0, 8))
tk.Radiobutton(
    radio_frame, text="Video", variable=var, value="video",
    bg="#162447", fg="white", selectcolor="#423BC2", activebackground="#162447", activeforeground="white"
).pack(side="left", padx=10)
tk.Radiobutton(
    radio_frame, text="Audio (MP3)", variable=var, value="audio",
    bg="#162447", fg="white", selectcolor="#423BC2", activebackground="#162447", activeforeground="white"
).pack(side="left", padx=10)

ttk.Button(main_frame, text="Download", command=threaded_download, style="Rounded.TButton").grid(
    row=4, column=0, columnspan=2, pady=(30, 15)
)


progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=450, mode="determinate")
progress_bar.grid(row=5, column=0, columnspan=2, pady=20)

status_label = tk.Label(main_frame, text="", fg="blue")
status_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=20)




root.configure(bg="#162447")
main_frame.configure(bg="#162447")
for widget in main_frame.winfo_children():
    if isinstance(widget, (tk.Label, tk.Entry, tk.Button, tk.Frame)):
        try:
            widget.configure(bg="#162447", fg="white")
        except:
            pass
    if isinstance(widget, tk.Entry):
        widget.configure(insertbackground="white")
    if isinstance(widget, tk.Frame):
        for subwidget in widget.winfo_children():
            try:
                subwidget.configure(bg="#162447", fg="white", selectcolor="#162447")
            except:
                pass
root.mainloop()
